#!/usr/bin/env python3

"""
The methods are taken from => https://github.com/anilbatra2185/road_connectivity

MIT License
==========================================================================

Copyright (c) 2020 Anil Batra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import math

import numpy as np
from skimage.morphology import skeletonize

from .graph_utils import segmets_to_linestrings, simplify_graph, unique
from .sknw import build_sknw


def getKeypoints(mask, is_gaussian=True, thresh=0.8, is_skeleton=False, smooth_dist=4):
    """
    Generate keypoints for binary prediction mask.

    @param mask: Binary road probability mask
    @param gaussian: Flag to check if the given mask is gaussian/probability mask
                    from prediction
    @param thresh: Probability threshold used to cnvert the mask to binary 0/1 mask.
                   It is used to convert the gaussian mask with required road width
    @param is_skeleton: Flag to perform opencv skeletonization on the binarized
                        road mask
    @param smooth_dist: Tolerance parameter used to smooth the graph using
                        RDP algorithm

    @return: return ndarray of road keypoints
    """
    if np.max(np.unique(mask)) > 1:
        mask /= 255.0

    if is_gaussian:
        mask[mask < thresh] = 0
        mask[mask >= thresh] = 1

    h, w = mask.shape
    if is_skeleton:
        ske = mask
    else:
        ske = skeletonize(mask).astype(np.uint16)
    graph = build_sknw(ske, multi=True)

    segments = simplify_graph(graph, smooth_dist)
    linestrings_1 = segmets_to_linestrings(segments)
    linestrings = unique(linestrings_1)

    keypoints = []
    for line in linestrings:
        linestring = line.rstrip("\n").split("LINESTRING ")[-1]
        points_str = linestring.lstrip("(").rstrip(")").split(", ")
        # If there is no road present
        if "EMPTY" in points_str:
            return keypoints
        points = []
        for pt_st in points_str:
            x, y = pt_st.split(" ")
            x, y = float(x), float(y)
            points.append([x, y])

            x1, y1 = points[0]
            x2, y2 = points[-1]
            zero_dist1 = math.sqrt((x1) ** 2 + (y1) ** 2)
            zero_dist2 = math.sqrt((x2) ** 2 + (y2) ** 2)

            if zero_dist2 > zero_dist1:
                keypoints.append(points[::-1])
            else:
                keypoints.append(points)
    return keypoints


def getVectorMapsAngles(shape, keypoints, theta=5, bin_size=10):
    """
    Convert Road keypoints obtained from road mask to orientation angle mask.
    Reference: Section 3.1
        https://anilbatra2185.github.io/papers/RoadConnectivityCVPR2019.pdf

    @param shape: Road Label/PIL image shape i.e. H x W
    @param keypoints: road keypoints generated from Road mask using
                        function getKeypoints()
    @param theta: thickness width for orientation vectors, it is similar to
                    thicknes of road width with which mask is generated.
    @param bin_size: Bin size to quantize the Orientation angles.

    @return: Retun ndarray of shape H x W, containing orientation angles per pixel.
    """

    im_h, im_w = shape
    vecmap = np.zeros((im_h, im_w, 2), dtype=np.float32)
    vecmap_angles = np.zeros((im_h, im_w), dtype=np.float32)
    vecmap_angles.fill(360)
    height, width, channel = vecmap.shape
    for j in range(len(keypoints)):
        for i in range(1, len(keypoints[j])):
            a = keypoints[j][i - 1]
            b = keypoints[j][i]
            ax, ay = a[0], a[1]
            bx, by = b[0], b[1]
            bax = bx - ax
            bay = by - ay
            norm = math.sqrt(1.0 * bax * bax + bay * bay) + 1e-9
            bax /= norm
            bay /= norm

            min_w = max(int(round(min(ax, bx) - theta)), 0)
            max_w = min(int(round(max(ax, bx) + theta)), width)
            min_h = max(int(round(min(ay, by) - theta)), 0)
            max_h = min(int(round(max(ay, by) + theta)), height)

            for h in range(min_h, max_h):
                for w in range(min_w, max_w):
                    px = w - ax
                    py = h - ay
                    dis = abs(bax * py - bay * px)
                    if dis <= theta:
                        vecmap[h, w, 0] = bax
                        vecmap[h, w, 1] = bay
                        _theta = math.degrees(math.atan2(bay, bax))
                        vecmap_angles[h, w] = (_theta + 360) % 360

    vecmap_angles = (vecmap_angles / bin_size).astype(int)
    return vecmap, vecmap_angles


def convertAngles2VecMap(shape, vecmapAngles, bin_size=10.0):
    """
    Helper method to convert Orientation angles mask to Orientation vectors.

    @params shape: Road mask shape i.e. H x W
    @params vecmapAngles: Orientation agles mask of shape H x W
    @param bin_size: Bin size to quantize the Orientation angles.

    @return: ndarray of shape H x W x 2, containing x and y values of vector
    """

    h, w = shape
    vecmap = np.zeros((h, w, 2), dtype=np.float)
    max_angle_bin = 360.0 / bin_size

    for h1 in range(h):
        for w1 in range(w):
            angle = vecmapAngles[h1, w1]
            if angle < max_angle_bin:
                angle *= bin_size
                if angle >= 180.0:
                    angle -= 360.0
                vecmap[h1, w1, 0] = math.cos(math.radians(angle))
                vecmap[h1, w1, 1] = math.sin(math.radians(angle))

    return vecmap


def convertVecMap2Angles(shape, vecmap, bin_size=10):
    """
    Helper method to convert Orientation vectors to Orientation angles.

    @params shape: Road mask shape i.e. H x W
    @params vecmap: Orientation vectors of shape H x W x 2

    @return: ndarray of shape H x W, containing orientation angles per pixel.
    """

    im_h, im_w = shape
    angles = np.zeros((im_h, im_w), dtype=np.float)
    angles.fill(360)

    for h in range(im_h):
        for w in range(im_w):
            x = vecmap[h, w, 0]
            y = vecmap[h, w, 1]
            angles[h, w] = (math.degrees(math.atan2(y, x)) + 360) % 360

    angles = (angles / bin_size).astype(int)
    return angles
