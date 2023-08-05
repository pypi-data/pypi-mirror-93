import torch
import numpy as np
import math
import torch.nn.functional as F


def calculate_intersection(preds, targs, mode): 
    """
    Calculates intersection between preds and targs.
    =====================   ===========================================
    **Argument**            **Description**
    ---------------------   -------------------------------------------
    preds                   Required torch.tensor. 
                            Predictions form a segmentation model.
                            file.
    ---------------------   -------------------------------------------
    targs                   Required torch.tensor. 
                            A batch of ground truth segmentation mask.
    ---------------------   -------------------------------------------
    mode                    Required str.
                            Possible values = 'per_class' or 'mean' 
                            'per_class' = Per class metrics are calculated.
                            'mean, = Mean metrics are calculated.
    -------------------------------------------------------------------
    Returns intersection between preds and targs -> torch.tensor
    """

    if mode == 'per_class': 
        dim = 2
        assert targs.ndim == 3
    if mode == 'mean': 
        dim = 1
        assert targs.ndim == 2

    return (preds * targs).sum(dim=dim)


def calculate_union(preds, targs, intersection, mode): 
    """
    Calculates union between preds and targs.
    =====================   ===========================================
    **Argument**            **Description**
    ---------------------   -------------------------------------------
    preds                   Required torch.tensor. 
                            Predictions form a segmentation model.
                            file.
    ---------------------   -------------------------------------------
    targs                   Required torch.tensor. 
                            A batch of ground truth segmentation mask.
    ---------------------   -------------------------------------------
    intersection            Required torch.tensor. 
                            Intersection between preds and targs
                            calculate_intersection(preds, targs, mode)
    ---------------------   -------------------------------------------
    mode                    Required str.
                            Possible values = 'per_class' or 'mean' 
                            'per_class' = Per class metrics are calculated.
                            'mean, = Mean metrics are calculated.
    -------------------------------------------------------------------
    Returns union between preds and targs -> torch.tensor
    """
    if mode == 'per_class': 
        dim = 2
        assert targs.ndim == 3
    if mode == 'mean': 
        dim = 1
        assert targs.ndim == 2

    return (preds + targs).sum(dim=dim) - intersection

def confusion_matrix(preds, targs, intersection, mode):
    """
    Calculates true positive, false positive and false negetive
    =====================   ===========================================
    **Argument**            **Description**
    ---------------------   -------------------------------------------
    preds                   Required torch.tensor. 
                            Predictions form a segmentation model.
                            file.
    ---------------------   -------------------------------------------
    targs                   Required torch.tensor. 
                            A batch of ground truth segmentation mask.
    ---------------------   -------------------------------------------
    mode                    Required str.
                            Possible values = 'per_class' or 'mean' 
                            'per_class' = Per class metrics are calculated.
                            'mean, = Mean metrics are calculated.
    -------------------------------------------------------------------
    Returns true positive, false positive and false negetive -> torch.tensor, torch.tensor, torch.tensor
    """

    if mode == 'per_class': 
        dim = 2
        assert targs.ndim == 3
    if mode == 'mean': 
        dim = 1
        assert targs.ndim == 2

    TP = intersection                                #true positive
    FP = preds.sum(dim=dim) - intersection           #flase positive
    FN = targs.sum(dim=dim) - intersection           #false negetive

    return TP, FP, FN

def calculate_precision(TP, FP, eps=1e-08):
    return TP / (TP + FP + eps)

def calculate_recall(TP, FN, eps=1e-08):
    return TP / (TP + FN + eps)

def calculate_f1(precision, recall, eps=1e-08):
    return 2 * (precision * recall) / (precision + recall + eps)

def prepare_output_for_metrics(preds, targs, ignore_classes, mode):
    """
    This function modifies the shape of targs(ground truth segmentation mask) 
    to match with preds(predicted output) 
    =====================   ===========================================
    **Argument**            **Description**
    ---------------------   -------------------------------------------
    preds                   Required torch.tensor. 
                            Predictions form a segmentation model.
                            file.
    ---------------------   -------------------------------------------
    targs                   Required torch.tensor. 
                            A batch of ground truth segmentation mask.
    ---------------------   -------------------------------------------
    mode                    Required str.
                            Possible values = 'per_class' or 'mean' 
                            'per_class' = Per class metrics are calculated.
                            'mean, = Mean metrics are calculated.
    -------------------------------------------------------------------
    Returns modeified preds and targs 
    """

    from arcgis.learn._utils.segmentation_loss_functions import  expand_outputs
    num = preds.size(0)
    classes = preds.size(1)
    keep_classes = [v for v in range(classes) if v not in ignore_classes]
    encoded_targs = expand_outputs(preds, targs)
    preds = preds.argmax(dim=1)
    preds = F.one_hot(preds, classes).permute(0, 3, 1, 2)
    if mode == 'per_class':
        preds = preds.contiguous().float().view(num, classes, -1)[:, keep_classes, :]
        encoded_targs = encoded_targs.float().view(num, classes, -1)[:, keep_classes, :]
    if mode == 'mean':
        preds = preds.contiguous().float().view(num, classes, -1)[:, keep_classes, :].view(num,-1)
        encoded_targs = encoded_targs.float().view(num, classes, -1)[:, keep_classes, :].view(num,-1)
    return  preds, encoded_targs

def calculate_metrics(preds, targs, mode,  ignore_classes=[]):
    """
    Calculates precision, recall and f1 scores.
    """
    # import pdb; pdb.set_trace();
    preds, targs = prepare_output_for_metrics(preds, targs, ignore_classes, mode)
    intersection = calculate_intersection(preds, targs, mode)
    union = calculate_union(preds, targs, intersection, mode)
    TP, FP, FN = confusion_matrix(preds, targs, intersection, mode) 
    precision = calculate_precision(TP, FP, eps=1e-08)
    recall = calculate_recall(TP, FN, eps=1e-08)
    f1 = calculate_f1(precision, recall, eps=1e-08)
    return precision, recall, f1


def post_process_CD(preds, y, n_classes):
    from .change_detection_data import post_process, post_process_y
    preds = post_process(preds)
    y[y == 1] = 0
    y[y == -1] = 1
    preds = preds.squeeze(1)
    preds = F.one_hot(preds, n_classes).permute(0, 3, 1, 2)
    return preds, y


def per_class_metrics(self,
                      ignore_classes=[], 
                      **kwargs):
    """
    Computes per class precision, recall and f1 scores 
    """
    import pandas as pd
    dl = kwargs.get('dl', None)
    postprocess_type = kwargs.get('postprocess_type', None)
    ignore_mapped_class = kwargs.get('ignore_mapped_class', ignore_classes)
    keep_classes = [c for i,c in  enumerate(self._data.classes) if i not in ignore_mapped_class]
    model = self.learn.model.eval()
    precision_list = []
    recall_list = []
    f1_list = []
    for batch in self._data.valid_dl if dl is None else dl:
        x, y = batch
        y = y.to('cpu')
        with torch.no_grad():
            if type(x) is list or type(x) is tuple:
                predictions = model(*x).detach().to('cpu')
            else:
                predictions = model(x).detach().to('cpu')
            if postprocess_type == 'CD':
                predictions, y = post_process_CD(predictions, 
                                                 y, 
                                                 n_classes=len(self._data.classes))

            precision, recall, f1 = calculate_metrics(predictions, 
                                                      y, 
                                                      mode='per_class', 
                                                      ignore_classes=ignore_mapped_class)
            precision_list.append(precision.mean(0))
            recall_list.append(recall.mean(0))
            f1_list.append(f1.mean(0))

    precision=torch.stack(tuple(precision_list)).mean(0)  
    recall=torch.stack(tuple(recall_list)).mean(0)   
    f1=torch.stack(tuple(f1_list)).mean(0)     

    columns = keep_classes
    df= pd.DataFrame(columns=columns)
    df.loc['precision'] = precision.tolist()
    df.loc['recall'] = recall.tolist()
    df.loc['f1'] = f1.tolist()
    return df


def show_batch_classified_tiles(self, rows=3, alpha=0.7, **kwargs):
    import matplotlib.pyplot as plt
    from .._utils.common import kwarg_fill_none, get_nbatches, find_data_loader, get_top_padding, get_symbology_bands, dynamic_range_adjustment, denorm_x, image_tensor_checks_plotting

    imsize = kwarg_fill_none(kwargs, 'imsize', 5)
    nrows = rows
    ncols = kwarg_fill_none(kwargs, 'ncols', 3)
    imsize = kwarg_fill_none(kwargs, 'imsize', 5)
    statistics_type = kwarg_fill_none(kwargs, 'statistics_type', 'dataset') # Accepted Values `dataset`, `DRA`
        
    n_items = kwargs.get('n_items', nrows*ncols)
    n_items = min(n_items, len(self.x))
    nrows = math.ceil(n_items/ncols)

    top = kwargs.get('top', None)
    title_font_size=16
    if top is None:
        top = get_top_padding(
            title_font_size=title_font_size, 
            nrows=nrows, 
            imsize=imsize
            )

    # Get n batches
    type_data_loader = kwarg_fill_none(kwargs, 'data_loader', 'training') # options : traininig, validation, testing
    data_loader = find_data_loader(type_data_loader, self)
    x_batch, y_batch = get_nbatches(data_loader, math.ceil(n_items/self.batch_size))
    symbology_x_batch = x_batch = torch.cat(x_batch)
    y_batch = torch.cat(y_batch)


    symbology_bands = [0, 1, 2]
    if self._is_multispectral:
        # Get RGB Bands for plotting
        rgb_bands = kwarg_fill_none(kwargs, 'rgb_bands', self._symbology_rgb_bands)

        # Get Symbology bands
        symbology_bands = get_symbology_bands(rgb_bands, self._extract_bands, self._bands)

    # Denormalize X
    x_batch = denorm_x(x_batch, self)

    # Extract RGB Bands for plotting
    symbology_x_batch = x_batch[:, symbology_bands]

    # Apply Image Strecthing
    if statistics_type == 'DRA':
        symbology_x_batch = dynamic_range_adjustment(symbology_x_batch)

    symbology_x_batch = image_tensor_checks_plotting(symbology_x_batch)

    # Get color Array
    color_array = self._multispectral_color_array
    color_array[1:, 3] = alpha

    # Plot now
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*imsize, nrows*imsize))
    idx = 0
    for r in range(nrows):
        for c in range(ncols):
            axi = axs
            if nrows == 1:
                axi = axi
            else:
                axi = axi[r]
            if ncols == 1:
                axi = axi
            else:
                axi = axi[c]
            axi.axis('off')
            if idx < symbology_x_batch.shape[0]:
                axi.imshow(symbology_x_batch[idx].cpu().numpy())
                y_rgb = color_array[y_batch[idx][0]].cpu().numpy()
                axi.imshow(y_rgb, alpha=alpha)
            idx+=1

