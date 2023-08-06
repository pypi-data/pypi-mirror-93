#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-ANN.
# @File         : utils
# @Time         : 2019-12-06 16:59
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
import numpy as np
import pandas as pd
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

# 并行加载
from functools import partial


def load_vector(files=Path('./ann_data/').glob('part*')):
    """

    :param files:
    :return: idx2word and vector data
    """
    with ProcessPoolExecutor(5) as pool:
        dfs = pool.map(partial(pd.read_csv, sep=' ', header=None), files)
        df = pd.concat(dfs, ignore_index=True)
    return df.iloc[:, 0].to_dict(), np.array(df.values[:, 1:].tolist(), 'float32')
