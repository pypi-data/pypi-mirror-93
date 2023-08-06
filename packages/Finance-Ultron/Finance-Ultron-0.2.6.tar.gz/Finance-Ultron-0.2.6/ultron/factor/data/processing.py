# -*- coding: utf-8 -*-

from typing import Optional
from typing import List
import numpy as np
from . neutralize import neutralize


def factor_processing(raw_factors: np.ndarray,
                      pre_process: Optional[List]=None,
                      risk_factors: Optional[np.ndarray]=None,
                      post_process: Optional[List]=None,
                      groups=None) -> np.ndarray:

    new_factors = raw_factors

    if pre_process:
        for p in pre_process:
            new_factors = p(new_factors, groups=groups)

    if risk_factors is not None:
        risk_factors = risk_factors[:, risk_factors.sum(axis=0) != 0]
        new_factors = neutralize(risk_factors, new_factors, groups=groups)

    if post_process:
        for p in post_process:
            new_factors = p(new_factors, groups=groups)

    return new_factors
