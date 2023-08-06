
"""functions common to verification and aggregation
"""

def make_date_list(params):
    """list of dates over which to iterate
    """

    import datetime
    import numpy as np

    if ((params.date_f == None) or
        (params.date_0 == params.date_f)):
        date_list = [params.date_0]
    else:
        t_diff = (params.date_f-params.date_0) + datetime.timedelta(seconds=1)    #+ 1 second for inclusive end point
        elasped_seconds = t_diff.days*3600.*24. + t_diff.seconds                  #I hate datetime objects...
        delta_date_seconds = params.delta_date*60.
        date_list = [params.date_0 + datetime.timedelta(seconds=x) for x in np.arange(0,elasped_seconds,delta_date_seconds)]

    return date_list

def make_leadtime_list(params):
    """list of leadtimes (datetime.timedelta) that will be verified in parallel
    """

    import datetime
    import numpy as np

    if params.leadtime_0 == params.leadtime_f:
        leadtime_list = [datetime.timedelta(seconds=params.leadtime_0*60.)]
    else:
        leadtime_list = [datetime.timedelta(seconds=lt*60.) for lt in np.arange(params.leadtime_0,params.leadtime_f, params.delta_leadtime)]

    return leadtime_list

def str2bool(v):
    import argparse
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

