#!/bin/bash 


#These system variables are important for preventing crashes when running in parallel (n_cpus > 1)
export XDG_RUNTIME_DIR=/space/hall3/sitestore/eccc/mrd/rpndat/dja001/tmpdir
export MPLBACKEND="agg" 
ulimit -s 128000
#make sure numpy does not use multithreading 
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1   

#type :
#   python gridded_obs.py -h 
#for a complete description of arguments
python -c 'import gridded_obs; gridded_obs.verify()'           \
                      --date_0 '2016070200'                    \
                      --date_f '2016070200'                    \
                      --delta_date 720                         \
                      --leadtime_0 -180                        \
                      --leadtime_f 730                         \
                      --delta_leadtime   10                    \
                      --grid_dx   2.5                          \
                      --score_dir '/space/hall3/sitestore/eccc/mrd/rpndat/dja001/test_new_griddedobs_tmp/'  \
                      --figure_dir '/space/hall3/sitestore/eccc/mrd/rpndat/dja001/test_new_griddedobs_tmp/' \
                      --img_dt  10                             \
                      --verif_domains 'radars'                 \
                      --thresholds  .1 .5 1. 5. 10.            \
                      --k_nbins 100                            \
                      --min_qi  0.2                            \
                      --hist_nbins 100                         \
                      --hist_min 0.01                          \
                      --hist_max 100.                          \
                      --hist_log_scale True                    \
                      --lmin_range 2.5 2000                    \
                      --n_cpus 1                              \
                      --complete_mode 'clobber'               \
                                                               \
                      --reference_reader  'ModelFst'           \
                      --reference_name 'bmosaicsv8'            \
                      --reference_varname 'RDPR'               \
                      --reference_qi_varname 'RDQI'            \
                      --reference_data_dir '/space/hall4/sitestore/eccc/mrd/rpndat/dja001/lhn_input/r_data_h5_v8_smooth_04_median_03_min_natgrid2.5/' \
                      --reference_file_struc '/%Y/%m/%d/%Y%m%d%H%M_mosaic.fst' \
                                                               \
                      --verified_reader 'ModelPrDiff'          \
                      --verified_name 'N2CC837E16'             \
                      --verified_pr_dt 10                      \
                      --verified_data_dir '/space/hall3/sitestore/eccc/mrd/rpndat/dja001/maestro_archives/DJA837E16/gridpt/prog/lhn/' \
                      --verified_prefix '%Y%m%d%H'             \
                      --verified_pr_dt 10                      \



                      #--verified_data_dir '/space/hall3/sitestore/eccc/mrd/rpndat/dja001/maestro_archives/N2CC802E16V1//gridpt/prog/lhn/' \
                      #--verified_data_dir '/space/hall3/sitestore/eccc/mrd/rpndat/dja001/maestro/NDPS710/DJA835E19/work/20190709000000/main/assimcycle/gridpt/prog/lhn/' \
                      #--verified_data_dir '/space/hall3/sitestore/eccc/mrd/rpndat/dja001/maestro_archives/N2CC800E16V1_links_for_precip/' \

                      
                      #--reference_data_dir '/space/hall4/sitestore/eccc/mrd/rpndat/dja001/lhn_input/r_data_h5_v8_smooth_04_median_03_min_natgrid2.5/' \
                      #--reference_file_struc '%Y/%m/%d/%Y%m%d%H%M_mosaic.fst' \

