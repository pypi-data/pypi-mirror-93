# -*- coding: utf-8 -*-
"""
Created on Dec 28 10:18 2020

@author: Hanwen Xu

E-mail: xuhw20@mails.tsinghua.edu.cn

New update: process data with unknown content
"""
from RareDecipher.deconvolution import DECONVO,pre_marker_select
import pandas as pd
import collections
import numpy as np


def decipher(ref_path, mix_path, save_path='prop_predict.csv', marker_path='', scale=0.1, delcol_factor=10, iter_num=10, confidence=0.75, w_thresh=10, unknown=False, is_markers=False, is_methylation=False):
    """

    :param ref_path: Path to reference data
    :param mix_path: Path to mixture data
    :param marker_path: Path to markers, if users select to specify certain markers
    :param save_path: save the results in this path
    :param scale: control the convergence of SVR
    :param delcol_factor: control the extent of removing collinearity
    :param iter_num: iterative numbers of outliers detection
    :param confidence: ratio of remained markers in each outlier detection loop
    :param w_thresh: threshold to cut the weights designer
    :param unknown: if there is unknown content
    :param is_markers: if users choose to specify their own markers
    :param is_methylation: if the data type belongs to methylation data
    :return:
    """
    print('---------------------------------------------')
    print('----------WELCOME TO RAREDECIPHER------------')
    print('---------------------------------------------')
    ref = pd.read_csv(ref_path, index_col=0)
    mix = pd.read_csv(mix_path, index_col=0)
    cell_type = ref.columns.values
    samples = mix.columns.values
    prop = collections.OrderedDict()
    prop['cell types'] = cell_type
    if is_markers:
        reference = []
        mixture = []
        markers = pd.read_csv(marker_path, index_col=0)
        markers = markers.index.values
        for i in range(len(markers)):
            reference.append(ref.loc[markers[i]])
            mixture.append(mix.loc[markers[i]])
    else:
        reference, mixture = ref, mix
    reference = np.asarray(reference)
    mixture = np.asarray(mixture)
    if is_methylation:
        reference, mixture = pre_marker_select(reference, mixture)
    print('Data reading finished!')
    print('RareDecipher Engines Start, Please Wait......')
    prop_predict = DECONVO(scale * reference, scale * mixture, delcol_factor=delcol_factor, iter_num=iter_num, confidence=confidence, w_thresh=w_thresh, unknown=unknown)
    print('Deconvo Results Saving!')
    for i in range(len(samples)):
        prop[samples[i]] = []
        for j in range(len(cell_type)):
            prop[samples[i]].append(prop_predict[j, i])
    prop = pd.DataFrame(prop)
    prop.to_csv(save_path, index=False)
    print('Finished!')

