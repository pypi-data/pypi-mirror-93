# -*- coding: utf-8 -*-

import numpy as np
import numba as nb
from typing import Tuple
from typing import Union
from typing import Dict
from . utilities import groupby


def neutralize(x: np.ndarray,
               y: np.ndarray,
               groups: np.ndarray=None,
               detail: bool=False,
               weights: np.ndarray = None) \
        -> Union[np.ndarray, Tuple[np.ndarray, Dict]]:

    if y.ndim == 1:
        y = y.reshape((-1, 1))

    if weights is None:
        weights = np.ones(len(y), dtype=float)

    output_dict = {}

    if detail:
        exposure = np.zeros(x.shape + (y.shape[1],))
        explained = np.zeros(x.shape + (y.shape[1],))
        output_dict['exposure'] = exposure
        output_dict['explained'] = explained

    if groups is not None:
        res = np.zeros(y.shape)
        index_diff, order = groupby(groups)
        start = 0
        if detail:
            for diff_loc in index_diff:
                curr_idx = order[start:diff_loc + 1]
                curr_x, b = _sub_step(x, y, weights, curr_idx, res)
                exposure[curr_idx, :, :] = b
                explained[curr_idx] = ls_explain(curr_x, b)
                start = diff_loc + 1
        else:
            for diff_loc in index_diff:
                curr_idx = order[start:diff_loc + 1]
                _sub_step(x, y, weights, curr_idx, res)
                start = diff_loc + 1
    else:
        try:
            b = ls_fit(x, y, weights)
        except np.linalg.linalg.LinAlgError:
            b = ls_fit_pinv(x, y, weights)

        res = ls_res(x, y, b)

        if detail:
            explained[:, :, :] = ls_explain(x, b)
            exposure[:] = b

    if output_dict:
        return res, output_dict
    else:
        return res


def _sub_step(x, y, w, curr_idx, res) -> Tuple[np.ndarray, np.ndarray]:
    curr_x, curr_y, curr_w = x[curr_idx], y[curr_idx], w[curr_idx]
    try:
        b = ls_fit(curr_x, curr_y, curr_w)
    except np.linalg.linalg.LinAlgError:
        b = ls_fit_pinv(curr_x, curr_y, curr_w)
    res[curr_idx] = ls_res(curr_x, curr_y, b)
    return curr_x, b


@nb.njit(nogil=True, cache=True)
def ls_fit(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> np.ndarray:
    x_bar = x.T * w
    b = np.linalg.solve(x_bar @ x, x_bar @ y)
    return b


@nb.njit(nogil=True, cache=True)
def ls_fit_pinv(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> np.ndarray:
    x_bar = x.T * w
    b = np.linalg.pinv(x_bar @ x) @ x_bar @ y
    return b


@nb.njit(nogil=True, cache=True)
def ls_res(x: np.ndarray, y: np.ndarray, b: np.ndarray) -> np.ndarray:
    return y - x @ b


@nb.njit(nogil=True, cache=True)
def ls_explain(x: np.ndarray, b: np.ndarray) -> np.ndarray:
    m, n = b.shape
    return b.reshape((1, m, n)) * x.reshape((-1, m, 1))