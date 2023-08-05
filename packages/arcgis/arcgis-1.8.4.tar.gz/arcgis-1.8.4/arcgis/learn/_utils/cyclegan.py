from fastai.vision import ItemBase, ItemList, Tensor, ImageList, Tuple, Path, get_transforms, random, open_image, Image, math, plt, torch, Learner, partial, optim, ifnone
from fastai.data_block import get_files as gf
from .._utils.common import ArcGISImageList, ArcGISMSImage
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
import torch
from scipy import linalg
from torch.nn.functional import adaptive_avg_pool2d
import numpy as np
import os
import json
import mimetypes

class ImageTuple(ItemBase):
    def __init__(self, img1, img2):
        self.img1,self.img2 = img1,img2
        self.obj,self.data = (img1,img2),[-1+2*img1.data,-1+2*img2.data]
        self.data2 = [-1+2*img2.data,-1+2*img1.data]
        self.shape = img1.shape
    
    def apply_tfms(self, tfms, **kwargs):
        self.img1 = self.img1.apply_tfms(tfms, **kwargs)
        self.img2 = self.img2.apply_tfms(tfms, **kwargs)
        return self
    
    def to_one(self): return ArcGISMSImage(0.5+torch.cat(self.data,2)/2)
    def to_one_pred(self): return ArcGISMSImage(0.5+torch.cat(self.data2,2)/2)
    
    def __repr__(self):
         return f'{self.__class__.__name__}{(self.img1.shape, self.img2.shape)}'

class TargetTupleList(ItemList):
    def reconstruct(self, t:Tensor): 
        if len(t.size()) == 0: return t
        return ImageTuple(ArcGISMSImage(t[0]/2+0.5),ArcGISMSImage(t[1]/2+0.5))

class ImageTupleList(ImageList):
    _label_cls=TargetTupleList
    def __init__(self, items, itemsB=None, **kwargs):
        self.itemsB = itemsB
        super().__init__(items, **kwargs)
    
    def new(self, items, **kwargs):
        return super().new(items, itemsB=self.itemsB, **kwargs)
    
    def get(self, i):
        img1 = super().get(i)
        fn = self.itemsB[random.randint(0, len(self.itemsB)-1)]
        return ImageTuple(img1, open_image(fn))
    
    def reconstruct(self, t:Tensor): 
        return ImageTuple(Image(t[0]/2+0.5),Image(t[1]/2+0.5))
    
    @classmethod
    def from_folders(cls, path, folderA, folderB, **kwargs):
        itemsB = ImageList.from_folder(path/folderB).items
        res = super().from_folder(path/folderA, itemsB=itemsB, **kwargs)
        res.path = path
        return res
    
    def show_xys(self, xs, ys, figsize:Tuple[int,int]=(12,6), **kwargs):
        "Show the `xs` and `ys` on a figure of `figsize`. `kwargs` are passed to the show method."
        rows = int(math.sqrt(len(xs)))
        fig, axs = plt.subplots(rows,rows,figsize=figsize)
        for i, ax in enumerate(axs.flatten() if rows > 1 else [axs]):
            xs[i].to_one().show(ax=ax, **kwargs)
        plt.tight_layout()

    def show_xyzs(self, xs, ys, zs, figsize:Tuple[int,int]=None, **kwargs):
        """Show `xs` (inputs), `ys` (targets) and `zs` (predictions) on a figure of `figsize`.
        `kwargs` are passed to the show method."""
        figsize = ifnone(figsize, (12,3*len(xs)))
        fig,axs = plt.subplots(len(xs), 2, figsize=figsize)
        fig.suptitle('Ground truth / Predictions', weight='bold', size=14)
        for i,(x,z) in enumerate(zip(xs,zs)):
            x.to_one().show(ax=axs[i,0], **kwargs)
            z.to_one_pred().show(ax=axs[i,1], **kwargs)

_batch_stats_a = None
_batch_stats_b = None

class ImageTupleListMS(ArcGISImageList):
    _label_cls=TargetTupleList
    def __init__(self, items, itemsB=None, **kwargs):
        self.itemsB = itemsB
        super().__init__(items, **kwargs)
    
    def new(self, items, **kwargs):
        return super().new(items, itemsB=self.itemsB, **kwargs)
    
    def get(self, i):    
        img1 = super().get(i)
        fn = self.itemsB[random.randint(0, len(self.itemsB)-1)]
        img2 = ArcGISMSImage.open(fn)
        if img1.shape[0] < img2.shape[0]:
            cont = []
            last_tile = np.expand_dims(img1.data[img1.shape[0]-1,:,:], 0)
            res = abs(img2.shape[0] - img1.shape[0])
            for i in range(res):
                img1 = ArcGISMSImage(torch.tensor(np.concatenate((img1.data, last_tile), axis=0)))
        if img2.shape[0] < img1.shape[0]:
            cont = []
            last_tile = np.expand_dims(img2.data[img2.shape[0]-1,:,:], 0)
            res = abs(img1.shape[0] - img2.shape[0])
            for i in range(res):
                img2 = ArcGISMSImage(torch.tensor(np.concatenate((img2.data, last_tile), axis=0)))
        global _batch_stats_a
        global _batch_stats_b
        img1_scaled = _tensor_scaler_tfm(img1.data, min_values=_batch_stats_a['band_min_values'], max_values=_batch_stats_a['band_max_values'], mode='minmax')
        img2_scaled = _tensor_scaler_tfm(img2.data, min_values=_batch_stats_b['band_min_values'], max_values=_batch_stats_b['band_max_values'], mode='minmax')
        img1_scaled = ArcGISMSImage(img1_scaled)
        img2_scaled = ArcGISMSImage(img2_scaled)
        return ImageTuple(img1_scaled, img2_scaled)
    
    def reconstruct(self, t:Tensor): 
        return ImageTuple(ArcGISMSImage(t[0]/2+0.5),ArcGISMSImage(t[1]/2+0.5))
    
    @classmethod
    def from_folders(cls, path, folderA, folderB, batch_stats_a, batch_stats_b, **kwargs):
        itemsB = ImageList.from_folder(path/folderB).items
        res = super().from_folder(path/folderA, itemsB=itemsB, **kwargs)
        res.path = path
        global _batch_stats_a
        global _batch_stats_b
        _batch_stats_a = batch_stats_a
        _batch_stats_b = batch_stats_b
        return res
    
    def show_xys(self, xs, ys, figsize:Tuple[int,int]=(12,6), **kwargs):
        "Show the `xs` and `ys` on a figure of `figsize`. `kwargs` are passed to the show method."
        
        rows = int(math.sqrt(len(xs)))
        fig, axs = plt.subplots(rows,rows,figsize=figsize)
        for i, ax in enumerate(axs.flatten() if rows > 1 else [axs]):
            xs[i].to_one().show(ax=ax, **kwargs)
        plt.tight_layout()

    def show_xyzs(self, xs, ys, zs, figsize:Tuple[int,int]=None, **kwargs):
        """Show `xs` (inputs), `ys` (targets) and `zs` (predictions) on a figure of `figsize`.
        `kwargs` are passed to the show method."""
        figsize = ifnone(figsize, (12,3*len(xs)))
        fig,axs = plt.subplots(len(xs), 2, figsize=figsize)
        fig.suptitle('Ground truth / Predictions', weight='bold', size=14)
        for i,(x,z) in enumerate(zip(xs,zs)):
            x.to_one().show(ax=axs[i,0], **kwargs)
            z.to_one_pred().show(ax=axs[i,1], **kwargs)

class InceptionV3(nn.Module):  # Code from https://github.com/mseitzer/pytorch-fid
    """Pretrained InceptionV3 network returning feature maps"""

    # Index of default block of inception to return,
    # corresponds to output of final average pooling
    DEFAULT_BLOCK_INDEX = 3

    # Maps feature dimensionality to their output blocks indices
    BLOCK_INDEX_BY_DIM = {
        64: 0,   # First max pooling features
        192: 1,  # Second max pooling featurs
        768: 2,  # Pre-aux classifier features
        2048: 3  # Final average pooling features
    }

    def __init__(self,
                 output_blocks=[DEFAULT_BLOCK_INDEX],
                 resize_input=True,
                 normalize_input=True,
                 requires_grad=False):
        """Build pretrained InceptionV3

        Parameters
        ----------
        output_blocks : list of int
            Indices of blocks to return features of. Possible values are:
                - 0: corresponds to output of first max pooling
                - 1: corresponds to output of second max pooling
                - 2: corresponds to output which is fed to aux classifier
                - 3: corresponds to output of final average pooling
        resize_input : bool
            If true, bilinearly resizes input to width and height 299 before
            feeding input to model. As the network without fully connected
            layers is fully convolutional, it should be able to handle inputs
            of arbitrary size, so resizing might not be strictly needed
        normalize_input : bool
            If true, scales the input from range (0, 1) to the range the
            pretrained Inception network expects, namely (-1, 1)
        requires_grad : bool
            If true, parameters of the model require gradient. Possibly useful
            for finetuning the network
        """
        super(InceptionV3, self).__init__()

        self.resize_input = resize_input
        self.normalize_input = normalize_input
        self.output_blocks = sorted(output_blocks)
        self.last_needed_block = max(output_blocks)

        assert self.last_needed_block <= 3, \
            'Last possible output block index is 3'

        self.blocks = nn.ModuleList()

        inception = models.inception_v3(pretrained=True)

        # Block 0: input to maxpool1
        block0 = [
            inception.Conv2d_1a_3x3,
            inception.Conv2d_2a_3x3,
            inception.Conv2d_2b_3x3,
            nn.MaxPool2d(kernel_size=3, stride=2)
        ]
        self.blocks.append(nn.Sequential(*block0))

        # Block 1: maxpool1 to maxpool2
        if self.last_needed_block >= 1:
            block1 = [
                inception.Conv2d_3b_1x1,
                inception.Conv2d_4a_3x3,
                nn.MaxPool2d(kernel_size=3, stride=2)
            ]
            self.blocks.append(nn.Sequential(*block1))

        # Block 2: maxpool2 to aux classifier
        if self.last_needed_block >= 2:
            block2 = [
                inception.Mixed_5b,
                inception.Mixed_5c,
                inception.Mixed_5d,
                inception.Mixed_6a,
                inception.Mixed_6b,
                inception.Mixed_6c,
                inception.Mixed_6d,
                inception.Mixed_6e,
            ]
            self.blocks.append(nn.Sequential(*block2))

        # Block 3: aux classifier to final avgpool
        if self.last_needed_block >= 3:
            block3 = [
                inception.Mixed_7a,
                inception.Mixed_7b,
                inception.Mixed_7c,
                nn.AdaptiveAvgPool2d(output_size=(1, 1))
            ]
            self.blocks.append(nn.Sequential(*block3))

        for param in self.parameters():
            param.requires_grad = requires_grad

    def forward(self, inp):
        """Get Inception feature maps

        Parameters
        ----------
        inp : torch.autograd.Variable
            Input tensor of shape Bx3xHxW. Values are expected to be in
            range (0, 1)

        Returns
        -------
        List of torch.autograd.Variable, corresponding to the selected output
        block, sorted ascending by index
        """
        outp = []
        x = inp

        if self.resize_input:
            x = F.interpolate(x,
                              size=(299, 299),
                              mode='bilinear',
                              align_corners=False)

        if self.normalize_input:
            x = 2 * x - 1  # Scale from range (0, 1) to range (-1, 1)

        for idx, block in enumerate(self.blocks):
            x = block(x)
            if idx in self.output_blocks:
                outp.append(x)

            if idx == self.last_needed_block:
                break

        return outp


def calculate_frechet_distance(mu1, sigma1, mu2, sigma2, eps=1e-6):
    """Numpy implementation of the Frechet Distance.
    The Frechet distance between two multivariate Gaussians X_1 ~ N(mu_1, C_1)
    and X_2 ~ N(mu_2, C_2) is
            d^2 = ||mu_1 - mu_2||^2 + Tr(C_1 + C_2 - 2*sqrt(C_1*C_2)).

    Stable version by Dougal J. Sutherland.

    Params:
    -- mu1   : Numpy array containing the activations of a layer of the
               inception net (like returned by the function 'get_predictions')
               for generated samples.
    -- mu2   : The sample mean over activations, precalculated on an
               representative data set.
    -- sigma1: The covariance matrix over activations for generated samples.
    -- sigma2: The covariance matrix over activations, precalculated on an
               representative data set.

    Returns:
    --   : The Frechet Distance.
    """

    mu1 = np.atleast_1d(mu1)
    mu2 = np.atleast_1d(mu2)

    sigma1 = np.atleast_2d(sigma1)
    sigma2 = np.atleast_2d(sigma2)

    assert mu1.shape == mu2.shape, \
        'Training and test mean vectors have different lengths'
    assert sigma1.shape == sigma2.shape, \
        'Training and test covariances have different dimensions'

    diff = mu1 - mu2

    # Product might be almost singular
    covmean, _ = linalg.sqrtm(sigma1.dot(sigma2), disp=False)
    if not np.isfinite(covmean).all():
        msg = ('fid calculation produces singular product; '
               'adding %s to diagonal of cov estimates') % eps
        print(msg)
        offset = np.eye(sigma1.shape[0]) * eps
        covmean = linalg.sqrtm((sigma1 + offset).dot(sigma2 + offset))

    # Numerical error might give slight imaginary component
    if np.iscomplexobj(covmean):
        if not np.allclose(np.diagonal(covmean).imag, 0, atol=1e-3):
            m = np.max(np.abs(covmean.imag))
            raise ValueError('Imaginary component {}'.format(m))
        covmean = covmean.real

    tr_covmean = np.trace(covmean)

    return (diff.dot(diff) + np.trace(sigma1) +
            np.trace(sigma2) - 2 * tr_covmean)

def get_activations(batch_size, data_len, batch_list, dims=2048): #cuda
    block_idx = InceptionV3.BLOCK_INDEX_BY_DIM[dims]
    model = InceptionV3([block_idx])
    model.cuda()
    pred_arr = np.empty((data_len, dims))
    model.eval()
    i = 0
    for im in batch_list:
        start = i
        end = i + batch_size
        i = i + batch_size
        pred = model(im.cuda())[0]
        if pred.size(2) != 1 or pred.size(3) != 1:
            pred = adaptive_avg_pool2d(pred, output_size=(1, 1))
        pred_arr[start:end] = pred.cpu().data.numpy().reshape(pred.size(0), -1)
    return pred_arr

def calculate_activation_statistics(batch_size, data_len, batch_list):
    act = get_activations(batch_size, data_len, batch_list)
    mu = np.mean(act, axis=0)
    sigma = np.cov(act, rowvar=False)
    return mu, sigma

def _tensor_scaler_tfm(tensor_batch, min_values, max_values, mode='minmax'):
    from .._data import _tensor_scaler
    x = tensor_batch
    if x.shape[0] > min_values.shape[0]:
        res = x.shape[0] - min_values.shape[0]
        last_val = torch.tensor([min_values[min_values.shape[0]-1]])
        for i in range(res):
            min_values = torch.tensor(np.concatenate((min_values, last_val), axis=0))
    if x.shape[0] > max_values.shape[0]:
        res = x.shape[0] - max_values.shape[0]
        last_val = torch.tensor([max_values[max_values.shape[0]-1]])
        for i in range(res):
            max_values = torch.tensor(np.concatenate((max_values, last_val), axis=0))
    max_values = max_values.view(-1, 1, 1).to(x.device)
    min_values = min_values.view(-1, 1, 1).to(x.device)
    x = _tensor_scaler(x, min_values, max_values, mode, create_view=False)
    return x

def _batch_stats_json(path, img_list, norm_pct, stats_file_name="esri_normalization_stats.json"):
    from .._data import _get_batch_stats
    if len(img_list) < 300:
        norm_pct = 1

    dummy_stats = {
                "batch_stats_for_norm_pct_0" : {
                    "band_min_values":None, 
                    "band_max_values":None, 
                    "band_mean_values":None, 
                    "band_std_values":None, 
                    "scaled_min_values":None, 
                    "scaled_max_values":None, 
                    "scaled_mean_values":None, 
                    "scaled_std_values":None}}

    normstats_json_path = os.path.abspath(path / '..' / stats_file_name)

    if not os.path.exists(normstats_json_path):       
        normstats = dummy_stats
        with open(normstats_json_path, 'w', encoding='utf-8') as f:
            json.dump(normstats, f, ensure_ascii=False, indent=4)
    else:
        with open(normstats_json_path) as f:
                normstats = json.load(f)

    norm_pct_search = f"batch_stats_for_norm_pct_{round(norm_pct*100)}"
    if norm_pct_search in normstats:
        batch_stats = normstats[norm_pct_search]
        for s in batch_stats:
            if batch_stats[s] is not None:
                batch_stats[s] = torch.tensor(batch_stats[s])
    else:
        batch_stats = _get_batch_stats(img_list, norm_pct)
        normstats[norm_pct_search] = dict(batch_stats)
        for s in normstats[norm_pct_search]:
            if normstats[norm_pct_search][s] is not None:
                normstats[norm_pct_search][s] = normstats[norm_pct_search][s].tolist()
        with open(normstats_json_path, 'w', encoding='utf-8') as f:
            json.dump(normstats, f, ensure_ascii=False, indent=4)
    
    return batch_stats


def prepare_data_ms_cyclegan(path, norm_pct, val_split_pct, seed, databunch_kwargs):
    folder_a = 'train_a'
    folder_b = 'train_b'

    img_list_a = ArcGISImageList.from_folder(path/"train_a")
    img_list_b = ArcGISImageList.from_folder(path/"train_b")
    
    batch_stats_a = _batch_stats_json(path, img_list_a, norm_pct, stats_file_name="esri_normalization_stats_a.json")
    batch_stats_b = _batch_stats_json(path, img_list_b, norm_pct, stats_file_name="esri_normalization_stats_b.json")

    data = ImageTupleListMS.from_folders(path, folder_a, folder_b, batch_stats_a, batch_stats_b)\
            .split_by_rand_pct(val_split_pct, seed=seed)\
            .label_empty()\
            .databunch(**databunch_kwargs)

    data._band_min_values = batch_stats_a['band_min_values']
    data._band_max_values = batch_stats_a['band_max_values']
    data._band_mean_values = batch_stats_a['band_mean_values']
    data._band_std_values = batch_stats_a['band_std_values']
    data._scaled_min_values = batch_stats_a['scaled_min_values']
    data._scaled_max_values = batch_stats_a['scaled_max_values']
    data._scaled_mean_values = batch_stats_a['scaled_mean_values']
    data._scaled_std_values = batch_stats_a['scaled_std_values']

    data._band_min_values_b = batch_stats_b['band_min_values']
    data._band_max_values_b = batch_stats_b['band_max_values']
    data._band_mean_values_b = batch_stats_b['band_mean_values']
    data._band_std_values_b = batch_stats_b['band_std_values']
    data._scaled_min_values_b = batch_stats_b['scaled_min_values']
    data._scaled_max_values_b = batch_stats_b['scaled_max_values']
    data._scaled_mean_values_b = batch_stats_b['scaled_mean_values']
    data._scaled_std_values_b = batch_stats_b['scaled_std_values']

    return data

def get_files(*args, **kwargs):
    return sorted(gf(*args, **kwargs))

image_extensions = set(k for k, v in mimetypes.types_map.items()
                       if v.startswith('image/'))