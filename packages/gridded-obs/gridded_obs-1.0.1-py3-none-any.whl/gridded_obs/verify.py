
import dask
@dask.delayed
def dask_verify_date_lt(*args, **kwargs):
    return verify_date_lt(*args, **kwargs)


def verify_date_lt(params, validity_date, leadtime):
    """ compute verifications scores between two gridded products
    
    """

    import os
    import datetime
    import warnings
    import gc
    import sqlite3
    from scipy import stats

    import gridded_obs.lmin_from_fss
    import numpy as np
    #import gridded_obs.plot.compare_fields

    leadtime_minutes = np.int(leadtime.days*1440. + leadtime.seconds/60.)


    #read reference field
    reference_dict = params.reference_reader.get_data(validity_date, leadtime)
    if (reference_dict is None):
        warnings.warn('Reference dataset unavailable for: ' + str(validity_date) + ' + ' + str(leadtime))

    #read quantity being verified 
    verified_dict  =  params.verified_reader.get_data(validity_date, leadtime)
    if (verified_dict is None):
        warnings.warn('Verified dataset unavailable for: ' + str(validity_date) + ' + ' + str(leadtime))

    #compute different verification scores
    if (reference_dict is not None) and (verified_dict is not None):

        for this_domain in params.verif_domains:

            imin,jmin,imax,jmax = params.domain_dict[this_domain]
            #keep only data points in the verification domain
            verif_latitudes    =      reference_dict['lats'][imin:imax,jmin:jmax]
            verif_longitudes   =      reference_dict['lons'][imin:imax,jmin:jmax]
            verif_reference_pr =    reference_dict['values'][imin:imax,jmin:jmax]
            verif_reference_qi = reference_dict['qi_values'][imin:imax,jmin:jmax]
            verif_verified_pr  =     verified_dict['values'][imin:imax,jmin:jmax]
            #quality index < min_qi set to zero
            verif_reference_qi   = np.where(verif_reference_qi < params.min_qi,  0., verif_reference_qi)

            ##TODO REMOVE!!! just for testing
            #verif_reference_qi   = np.where(verif_reference_qi < params.min_qi,  0., 1.)

            #list of points to be used fro corr coeff calculations 
            good_pts = (verif_reference_qi > params.min_qi).nonzero()


            #
            #
            #open sqlite file
            conn = params.sql_handler.connect(must_exist=True)
            c = conn.cursor()

            #id element for the domain being verified
            domain_id = params.sql_handler.domain_id_dict[this_domain]

            #
            #
            # histograms

            #id reference data
            #a new row in sql table is created if it does not already exists
            elem_id, already_existed = params.sql_handler.get_element_id(c, table_name='hist_reference', 
                                                                            domain_id=domain_id, 
                                                                            leadtime_minutes=leadtime_minutes)
            if params.complete_mode == 'complete' and already_existed:
                #in complete mode, we skip element if it already exists
                pass
            else:
                reference_hist, _ = np.histogram(verif_reference_pr, bins=params.hist_bin_edges, weights=verif_reference_qi)
                params.sql_handler.insert_hist(c, 'hist_reference', elem_id, reference_hist, params)
                conn.commit()

            #if of verified data
            #a new row in sql table is created if it does not already exists
            elem_id, already_existed = params.sql_handler.get_element_id(c, table_name='hist_verified', 
                                                                            domain_id=domain_id, 
                                                                            leadtime_minutes=leadtime_minutes)
            if params.complete_mode == 'complete' and already_existed:
                #in complete mode, we skip element if it already exists
                pass
            else:
                verified_hist, _ = np.histogram(verif_verified_pr, bins=params.hist_bin_edges, weights=verif_reference_qi)
                params.sql_handler.insert_hist(c, 'hist_verified', elem_id, verified_hist, params)
                conn.commit()

            conn.close()
            #


            for this_threshold in params.thresholds:

                #id element for the threshold being veridied
                threshold_id = params.sql_handler.threshold_id_dict[str(this_threshold)]

                #a new row in sql table is created if it does not already exists
                conn = params.sql_handler.connect(must_exist=True)
                c = conn.cursor()
                elem_id, already_existed = params.sql_handler.get_element_id(c, table_name='stats', 
                                                                                domain_id=domain_id, 
                                                                                threshold_id=threshold_id, 
                                                                                leadtime_minutes=leadtime_minutes)
                conn.commit()
                conn.close()

                if params.complete_mode == 'complete' and already_existed:
                    #in complete mode, we skip element if it already exists
                    pass
                else:

                    print("verifying date: ", validity_date, "leadtime:", leadtime_minutes, "threshold: ", this_threshold)

                    #apply threshold on quantity
                    reference_true = np.where(verif_reference_pr >= this_threshold, 1., 0.)
                    verified_true  = np.where(verif_verified_pr  >= this_threshold, 1., 0.)

                    #
                    #
                    # contingency table ; data pointa are weighted by quality index
                    x = np.sum(verif_reference_qi * np.logical_and(np.isclose(verified_true,1.), np.isclose(reference_true,1.)))
                    y = np.sum(verif_reference_qi * np.logical_and(np.isclose(verified_true,0.), np.isclose(reference_true,1.)))
                    z = np.sum(verif_reference_qi * np.logical_and(np.isclose(verified_true,1.), np.isclose(reference_true,0.)))
                    w = np.sum(verif_reference_qi * np.logical_and(np.isclose(verified_true,0.), np.isclose(reference_true,0.)))

                    #
                    #
                    # pearson's correlation coefficient
                    reference_pts_for_corr = np.where(verif_reference_pr > this_threshold, verif_reference_pr, 0.)[good_pts]
                    verified_pts_for_corr  = np.where(verif_verified_pr  > this_threshold, verif_verified_pr,  0.)[good_pts]
                    corr_coeff, _ = stats.pearsonr(reference_pts_for_corr, verified_pts_for_corr)

                    #
                    #
                    #minimum length scale for significant results using FSS in circular areas
                    lmin_value = gridded_obs.lmin_from_fss(reference_true, verif_reference_qi, verified_true, 'fft',
                                                           params.lmin_range, grid_dx=params.grid_dx)
                    #for debugging
                    #if lmin_value is None:
                    #    #plot image
                    #    compare_fields.plot_img(reference_true, verif_reference_qi, verified_true, 
                    #                            verif_latitudes,   verif_longitudes,
                    #                            this_threshold, 
                    #                            params.figure_dir, validity_date, leadtime, radius=lmin_value)


                    #
                    #
                    #oper sql file for writting
                    conn = params.sql_handler.connect(must_exist=True)
                    c = conn.cursor()

                    #write x,y,z,w
                    cmd = '''update stats set x = ? , y = ? , z = ? , w = ?  where (id = '''+str(elem_id)+'''); '''
                    c.execute(cmd,(int(x),int(y),int(z),int(w)))

                    #write correlation coefficient
                    cmd = '''update stats set corr_coeff = ? where (id = '''+str(elem_id)+'''); '''
                    c.execute(cmd,(corr_coeff,))

                    #write lmin
                    if lmin_value is not None:
                        cmd = '''update stats set lmin = ? where (id = '''+str(elem_id)+'''); '''
                        c.execute(cmd,(lmin_value,))
                
                    conn.commit()
                    conn.close()


    else:
        #one (or both) of reference or verified fields not found
        pass


    #collect garbage that may accumulate
    gc.collect()

    #return something to maks dask happy
    return np.array([0.],dtype=np.float)



def forecast_loop(params):

    """
    When verifying data, one must loop over:

        - Validity date (T0)
        - Forecast lead time  (only applicable to forecasts, will be 0 when verifying an observation dataset against another)
        - members (only applicable to ensembles)
        - Thresholds
        - Verification domains

    This function is designed for verifying deterministic forecasts

    It loops over Validity dates while leadtimes for a given date are computed in parallel.

    args:
        - params see description in main

    """
    import os
    import time
    import datetime
    import numpy as np
    import dask.distributed
    import dask
    import dask.array as da
    #local
    import gridded_obs.sql 
    import gridded_obs.common


    #list of dates over which to iterate
    date_list = gridded_obs.common.make_date_list(params)

    #list of leadtimes (datetime.timedelta) that will be verified in parallel
    leadtime_list = gridded_obs.common.make_leadtime_list(params)


    #iterate over forecast validity dates
    for date in date_list:

        #for deterministic forecast verification, there is one sqlite file per date verified
        #initialize sqlite file and object to interact with it
        params.sql_handler = gridded_obs.sql.Handler(date, params, params.reference_reader.name, params.verified_reader.name)
        params.sql_handler.init_sqlite_file(params)

        if params.n_cpus == 1:
            #serial execution
            for leadtime in leadtime_list:
                out = verify_date_lt(params, date, leadtime)
        else:
            #parallel executions
            with dask.distributed.Client(processes=True, threads_per_worker=1, n_workers=params.n_cpus, silence_logs=40) as client:

                # sample output so dask knows what to expect only shape and type matters here
                sample = np.array([0],dtype=np.float)  
                #list of desired outputs
                delayed_params = dask.delayed(params)
                res_list = [da.from_delayed(dask_verify_date_lt(delayed_params, date, leadtime), sample.shape, sample.dtype) for leadtime in leadtime_list]
                res_array = da.stack(res_list,axis=1)
                # expected result
                res = res_array.sum()
                # Computation is performed here
                t1 = time.time()
                total = res.compute()
                t2 = time.time()
                print("date: ", date, 'completed in: ', t2-t1, 'seconds')


def verify():

    """launch verification


    Verification is performed between a "reference" and a "verified" datasets

    All arguments prefixed with '--reference_' will be passed directly to reader that must read the referece dataset
             "                  '--verified_'                     "

    gridded_obs does not care about what kind of data is being verified. 
    It is the user's responsability to make sure that the reference and verified readers 
    return quantities that are comparable (eg. with the same units).

    """

    import argparse
    import datetime
    import numpy as np
    import dask.distributed
    #local 
    import gridded_obs.readers 
    import gridded_obs.common

    #arguments for the verification
    parser = argparse.ArgumentParser(description="general variables necessary to all verifications", 
                                     prefix_chars='-+', formatter_class=argparse.RawDescriptionHelpFormatter)


    parser.add_argument("--date_0"  ,     type=lambda d: datetime.datetime.strptime(d, '%Y%m%d%H'),   
                                          required=True,  help=("[yyyymmddhh] (inclusive) first date being verified"))

    parser.add_argument("--date_f"  ,     type=lambda d: datetime.datetime.strptime(d, '%Y%m%d%H'),   
                                          required=False, help=("[yyyymmddhh] (inclusive) last date being verified"), 
                                          default=None)

    parser.add_argument("--delta_date",            type=float, required=False,  help="[minutes] interval between dates being verified",
                                                   default=None)

    parser.add_argument("--leadtime_0" ,           type=float, required=False,  help="[minutes] (inclusive) first leadtime to verify ",
                                                   default=0)
    parser.add_argument("--leadtime_f" ,           type=float, required=False,  help="[minutes] (inclusive) last  leadtime to verify ",
                                                   default=0)
    parser.add_argument("--delta_leadtime",        type=float, required=False, help="[minutes] interval between lead times being verified",
                                                   default=None)
    parser.add_argument("--grid_dx"    ,           type=float, required=True,  help="[km] size of grid tile")
    #output locations
    parser.add_argument("--outname_file_struc",    type=str,   required=False,  help="File structure for output name; use '%reference_name' and '%verified_name' ", 
                                                   default='%verified_name_vs_%reference_name__%Y%m%d%H.sqlite3')
    parser.add_argument("--score_dir" ,            type=str,   required=True,  help="directory where scores will be saved for aggregation later")
    parser.add_argument("--figure_dir" ,           type=str,   required=True,  help="directory where figures will be saved")
    #parameters governing the verification itself
    parser.add_argument("--img_dt",                type=float, required=True,  help="[minutes] frequency at which figures will be generated")
    parser.add_argument("--verif_domains",nargs="+",type=str,  required=True,  help="[imin,jmin,imax,jmax] bottom-left and top-right verificatoin domain ")
    parser.add_argument("--thresholds",  nargs="+",type=float, required=True,  help="list of thresholds to verify")
    parser.add_argument("--k_nbins",               type=int,   required=True,  help="Number of bins for DCT spectra")
    parser.add_argument("--min_qi",                type=float, required=True,  help="Minimum quality index to consider for all verification")
    parser.add_argument("--hist_nbins",            type=int,   required=True,  help="Number of bins for histograms")
    parser.add_argument("--hist_min",              type=float, required=True,  help="[in unit being verified] minimum value for histograms ")
    parser.add_argument("--hist_max",              type=float, required=True,  help="[in unit being verified] maximum value for histograms ")
    parser.add_argument("--hist_log_scale",        type=str,   required=True,  help="set to True to use logscale in histograms ")
    parser.add_argument("--lmin_range",  nargs="+",type=float, required=False, help="minimum and maximum [km] radius for searching lmin ")
    parser.add_argument("--n_cpus",                type=int,   required=True,  help="number of cpus for parallel execution set to 1 for serial execution")
    parser.add_argument("--complete_mode",         type=str,   required=False, default='clobber', help="'complete' or 'clobber' existing sql files")

    #parse arguments
    (params, unknown_args) = parser.parse_known_args()


    #convert strings to bool for certain variables
    params.hist_log_scale = gridded_obs.common.str2bool(params.hist_log_scale)

    #compute edges of histograms
    if params.hist_log_scale:
        params.hist_bin_edges = np.geomspace(params.hist_min, params.hist_max, num=params.hist_nbins+1, endpoint=True)
    else:
        params.hist_bin_edges =  np.linspace(params.hist_min, params.hist_max, num=params.hist_nbins+1, endpoint=True)

    #---------------------------------------------------------------------------


    #TODO 
    #find out a way to pass multiple domains through arguments
    domain_dict = {'all':   [None, None, None, None], 
                   'radars':[200,  50,   2300, 700] }
    params.domain_dict = domain_dict


    #initialize readers for reference data and verified data
    params.reference_reader = gridded_obs.readers.reader_init('reference', unknown_args)
    params.verified_reader  = gridded_obs.readers.reader_init('verified',  unknown_args)


    ##initialize dask client if parallel execution is desired
    #params.dask_client_exists = False
    #if params.n_cpus > 1 :
    #    client = dask.distributed.Client(processes=True, threads_per_worker=1, n_workers=params.n_cpus, silence_logs=40)
    #    params.dask_client_exists = True

    #make sure delta_date is specified
    if params.date_f is not None:
        if params.delta_date is None:
            raise ValueError('argument "delta_date" must be specified when date_f is specified')


    #launch verification
    forecast_loop(params)



if __name__ =='__main__':
    verify()
