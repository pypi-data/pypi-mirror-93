import numpy as np
import bottleneck as _bn
from functools import wraps as _wraps

VERSION_STR = "1.0"

def as_nancall(bnfunc):
    def wrapper(func):
        @_wraps(func)
        def _call_bnfunc(vec, rad, num=1):
            return nancall(bnfunc, vec, rad, num=num)
        return _call_bnfunc
    return wrapper

def nancall(fun, vec, rad, num=1):
    rad = int(round(rad))
    dia = rad*2+1
    if (num == 0) or (rad == 0):
        return vec
    margin = np.empty(rad, dtype=float); margin[:] = np.nan
    vec_ext = np.concatenate([margin, vec, margin])
    vec     = fun(vec_ext, dia, min_count=1, axis=-1)[(dia-1):]
    if num == 1:
        return vec
    else:
        return nancall(fun, vec, rad, num=num-1)

@as_nancall(_bn.move_mean)
def nanmean(vec, rad, num=1):
    pass

@as_nancall(_bn.move_min)
def nanmin(vec, rad, num=1):
    pass

@as_nancall(_bn.move_max)
def nanmax(vec, rad, num=1):
    pass

@as_nancall(_bn.move_std)
def nanstd(vec, rad, num=1):
    pass
