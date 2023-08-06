# -*- coding: utf-8 -*-
import base64
import pickle
import math
import numpy as np
import numba as nb


def map_freq(freq):

    if freq == '1m':
        horizon = 21
    elif freq == '1w':
        horizon = 4
    elif freq == '2w':
        horizon = 9
    elif freq == '3w':
        horizon = 14
    elif freq == '4w':
        horizon = 19
    elif freq == '1d':
        horizon = 0
    elif freq[-1] == "b":
        horizon = int(freq[:-1]) - 1
    else:
        raise ValueError("Unrecognized freq: {0}".format(freq))
    return horizon


def groupby(groups):
    order = groups.argsort()
    t = groups[order]
    index_diff = np.where(np.diff(t))[0]
    return np.concatenate([index_diff, [len(groups)]]), order


@nb.njit(nogil=True, cache=True)
def set_value(mat, used_level, to_fill):
    length, width = used_level.shape
    for i in range(length):
        for j in range(width):
            k = used_level[i, j]
            mat[k, j] = to_fill


@nb.njit(nogil=True, cache=True)
def group_mapping(groups: np.ndarray) -> np.ndarray:
    length = groups.shape[0]
    order = groups.argsort()
    res = np.zeros(length, dtype=order.dtype)

    start = 0
    res[order[0]] = start
    previous = groups[order[0]]

    for i in range(1, length):
        curr_idx = order[i]
        curr_val = groups[curr_idx]
        if curr_val != previous:
            start += 1
            res[curr_idx] = start
        else:
            res[curr_idx] = start
        previous = curr_val
    return res


@nb.njit(nogil=True, cache=True)
def simple_sum(x, axis=0):
    length, width = x.shape

    if axis == 0:
        res = np.zeros(width)
        for i in range(length):
            for j in range(width):
                res[j] += x[i, j]

    elif axis == 1:
        res = np.zeros(length)
        for i in range(length):
            for j in range(width):
                res[i] += x[i, j]
    else:
        raise ValueError("axis value is not supported")
    return res


@nb.njit(nogil=True, cache=True)
def simple_abssum(x, axis=0):

    length, width = x.shape

    if axis == 0:
        res = np.zeros(width)
        for i in range(length):
            for j in range(width):
                res[j] += abs(x[i, j])

    elif axis == 1:
        res = np.zeros(length)
        for i in range(length):
            for j in range(width):
                res[i] += abs(x[i, j])
    else:
        raise ValueError("axis value is not supported")
    return res


@nb.njit(nogil=True, cache=True)
def simple_sqrsum(x, axis=0):
    length, width = x.shape

    if axis == 0:
        res = np.zeros(width)
        for i in range(length):
            for j in range(width):
                res[j] += x[i, j] * x[i, j]

    elif axis == 1:
        res = np.zeros(length)
        for i in range(length):
            for j in range(width):
                res[i] += x[i, j] * x[i, j]
    else:
        raise ValueError("axis value is not supported")

    res = np.sqrt(res)
    return res


@nb.njit(nogil=True, cache=True)
def simple_mean(x, axis=0):
    length, width = x.shape

    if axis == 0:
        res = np.zeros(width)
        for j in range(width):
            for i in range(length):
                res[j] += x[i, j]
            res[j] /= length

    elif axis == 1:
        res = np.zeros(length)
        for i in range(length):
            for j in range(width):
                res[i] += x[i, j]
            res[i] /= width
    else:
        raise ValueError("axis value is not supported")
    return res


@nb.njit(nogil=True, cache=True)
def simple_std(x, axis=0, ddof=1):
    length, width = x.shape

    if axis == 0:
        res = np.zeros(width)
        sum_mat = np.zeros(width)
        for j in range(width):
            for i in range(length):
                res[j] += x[i, j] * x[i, j]
                sum_mat[j] += x[i, j]
            res[j] = math.sqrt((res[j] - sum_mat[j] * sum_mat[j] / length) / (length - ddof))
    elif axis == 1:
        res = np.zeros(length)
        sum_mat = np.zeros(width)
        for i in range(length):
            for j in range(width):
                res[i] += x[i, j] * x[i, j]
                sum_mat[i] += x[i, j]
            res[i] = math.sqrt((res[i] - sum_mat[i] * sum_mat[i] / width) / (width - ddof))
    else:
        raise ValueError("axis value is not supported")
    return res


@nb.njit(nogil=True, cache=True)
def agg_sum(groups, x):
    max_g = groups.max()
    length, width = x.shape
    res = np.zeros((max_g+1, width), dtype=np.float64)

    for i in range(length):
        for j in range(width):
            res[groups[i], j] += x[i, j]
    return res


@nb.njit(nogil=True, cache=True)
def agg_sqrsum(groups, x):
    max_g = groups.max()
    length, width = x.shape
    res = np.zeros((max_g + 1, width), dtype=np.float64)

    for i in range(length):
        for j in range(width):
            res[groups[i], j] += x[i, j] * x[i, j]

    res = np.sqrt(res)
    return res


@nb.njit(nogil=True, cache=True)
def agg_abssum(groups, x):
    max_g = groups.max()
    length, width = x.shape
    res = np.zeros((max_g+1, width), dtype=np.float64)

    for i in range(length):
        for j in range(width):
            res[groups[i], j] += abs(x[i, j])
    return res


@nb.njit(nogil=True, cache=True)
def agg_mean(groups, x):
    max_g = groups.max()
    length, width = x.shape
    res = np.zeros((max_g+1, width), dtype=np.float64)
    bin_count = np.zeros(max_g+1, dtype=np.int32)

    for i in range(length):
        for j in range(width):
            res[groups[i], j] += x[i, j]
        bin_count[groups[i]] += 1

    for i in range(max_g+1):
        curr = bin_count[i]
        for j in range(width):
            res[i, j] /= curr
    return res


@nb.njit(nogil=True, cache=True)
def agg_std(groups, x, ddof=1):
    max_g = groups.max()
    length, width = x.shape
    res = np.zeros((max_g+1, width), dtype=np.float64)
    sumsq = np.zeros((max_g + 1, width), dtype=np.float64)
    bin_count = np.zeros(max_g+1, dtype=np.int32)

    for i in range(length):
        for j in range(width):
            res[groups[i], j] += x[i, j]
            sumsq[groups[i], j] += x[i, j] * x[i, j]
        bin_count[groups[i]] += 1

    for i in range(max_g+1):
        curr = bin_count[i]
        for j in range(width):
            res[i, j] = math.sqrt((sumsq[i, j] - res[i, j] * res[i, j] / curr) / (curr - ddof))
    return res


@nb.njit(nogil=True, cache=True)
def copy_value(groups, source):
    length = groups.shape[0]
    width = source.shape[1]
    destination = np.zeros((length, width))
    for i in range(length):
        k = groups[i]
        for j in range(width):
            destination[i, j] = source[k, j]
    return destination


@nb.njit(nogil=True, cache=True)
def scale_value(groups, source, x, scale):
    length, width = x.shape
    destination = x.copy()
    for i in range(length):
        k = groups[i]
        for j in range(width):
            destination[i, j] /= source[k, j] / scale
    return destination


@nb.njit(nogil=True, cache=True)
def array_index(array, items):
    to_look_length = items.shape[0]
    arr_length = array.shape[0]

    res = np.zeros(to_look_length, dtype=array.dtype)

    for i in range(to_look_length):
        for j in range(arr_length):
            if items[i] == array[j]:
                res[i] = j
                break
    return res


def transform(groups: np.ndarray,
              x: np.ndarray,
              func: str,
              ddof: int=1,
              scale: float=1.) -> np.ndarray:

    if func == 'mean':
        value_data = agg_mean(groups, x)
    elif func == 'std':
        value_data = agg_std(groups, x, ddof=ddof)
    elif func == 'sum':
        value_data = agg_sum(groups, x)
    elif func == 'abssum' or func == 'scale':
        value_data = agg_abssum(groups, x)
    elif func == 'sqrsum' or func == 'project':
        value_data = agg_sqrsum(groups, x)
    else:
        raise ValueError('({0}) is not recognized as valid functor'.format(func))

    if func == 'scale' or func == 'project':
        return scale_value(groups, value_data, x, scale)
    else:
        return copy_value(groups, value_data)


def aggregate(groups, x, func, ddof=1):
    if func == 'mean':
        value_data = agg_mean(groups, x)
    elif func == 'std':
        value_data = agg_std(groups, x, ddof=ddof)
    elif func == 'sum':
        value_data = agg_sum(groups, x)
    elif func == 'abssum' or func == 'scale':
        value_data = agg_abssum(groups, x)
    elif func == 'sqrsum' or func == 'project':
        value_data = agg_sqrsum(groups, x)
    else:
        raise ValueError('({0}) is not recognized as valid functor'.format(func))

    return value_data


def encode(obj: object) -> str:
    encoded = base64.encodebytes(pickle.dumps(obj))
    return encoded.decode('ascii')


def decode(str_repr: str):
    encoded = str_repr.encode('ascii')
    return pickle.loads(base64.decodebytes(encoded))