import numpy as np


def check_masksize(da, spval=1e+15, x='lon', y='lat', z='lev', time='time'):
    """ Check mask size in xarray.dataarray for all time records
    and return False if size is changing """

    check = True
    message = ''
    # xarray fills with NaN that are not convenient to work with
    masked = da.fillna(spval)
    # compute the size of the mask in function of depth and time
    masksize = masked.where(masked == spval).count(dim=[x, y])
    # Check that the size does not change over time
    masksize_3d = masksize.sum(dim=z)
    tendency = masksize_3d.diff(dim=time)
    if tendency.any() != 0:
        check = False
        message = 'PROBLEM: mask size is not constant in time'
        return check, message
    # Check that mask size is increasing with depth
    tendency = masksize.isel({time: 0}).diff(dim=z)
    if tendency.any() < 0:
        check = False
        message = 'PROBLEM: mask size is decreasing with depth'
        return check, message


def check_timeaxis(ds, time='time'):
    """ check the time axis """

    check = True
    message = ''
    tendency = ds[time].diff(dim=time)
    if not np.timedelta64(28, 'D') <= tendency <= np.timedelta64(31, 'D'):
        check = False
        message = 'PROBLEM: records are not correctly spaced'
        return check, message
