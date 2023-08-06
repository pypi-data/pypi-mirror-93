#!/bin/bash

#These systrem variables are important for preventing crashes
export XDG_RUNTIME_DIR=/space/hall3/sitestore/eccc/mrd/rpndat/dja001/tmpdir
export MPLBACKEND="agg" 
ulimit -s 128000
#make sure numpy does not use multithreading 
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1   

#colors can be specified as:
#'(r,g,b)'     colors in the range 0-255
#'(r,g,b,a)'   colors in the range 0-255  alpha in the range 0-1
#'l_orange_0.7' for legs colors         0.0 for pale color, 1.0 for dark colors
#               color can be one of 'brown','blue','green','orange', 'red','pink','purple','yellow', 'b_w'
#               see: https://domutils.readthedocs.io/en/stable/legsTutorial.html#specifying-colors
#
#any other strings will be passed "as is" to matplotlib

#linestyle: 'solid' 'dotted' 'dashed' 'dashdot'
#passed "as is" to matplotlib "linestyle" argument of the ax.plot() method

#type :
#   python gridded_obs.py -h 
#for a complete description of arguments
python -c 'import gridded_obs; gridded_obs.aggregate()'      \
                    --date_0 '2016070200'                    \
                    --date_f '2016070200'                    \
                    --delta_date 720                         \
                    --leadtime_0 -180                        \
                    --leadtime_f 730                         \
                    --delta_leadtime   10                    \
                    --leadtime_ignore  10                    \
                    --leadtime_greyed_out  -180 180          \
                    --score_dir '/space/hall3/sitestore/eccc/mrd/rpndat/dja001/dasVerif/ominusp/DJA837E16/2016070200_sqlite/' \
                    --figure_dir '/space/hall3/sitestore/eccc/mrd/rpndat/dja001/test_new_griddedobs_tmp/' \
                    --verif_domains 'radars'                 \
                    --make_same 'True'                       \
                    --thresholds  .1 .5 1. 5. 10.            \
                                                             \
                    --time_series  'fbias' 'pod' 'far' 'csi' 'lmin' 'corr_coeff'                \
                    --twod_panels  'histograms'              \
                                                             \
                    --n_cpus 1                               \
                                                             \
                    --reference_name 'bmosaicsv8'                    \
                                                                     \
                    --exp_list       'DJA837E16'     \
                    --exp_color      'l_blue_0.7'     \
                    --exp_linestyle  'solid'          \
                    --exp_linewidth  '2'              \
                                                                     \
                    #--ylim_fbias       0.85 1.4                       \
                    #--ylim_pod         0.2   .38                     \
                    #--ylim_far         0.65 0.84                       \
                    #--ylim_csi         0.11 0.22                      \
                    #--ylim_lmin        25. 180.                      \
                    #--ylim_corr_coeff  0.07 0.13                     \

                    #'N2CC802E19_rainfix'
                    #'l_orange_0.7'      
                    #'solid'             
                    #'2'                 



                    
                    #--exp_list       'N2CC800E19'   'N2CC802E19'     \
                    #--exp_color      'l_orange_0.7'        'l_blue_0.7'     \
                    #--exp_linestyle  'dashed'       'solid'          \
                    #--exp_linewidth  '2.5'          '2'              \


                    #--exp_list      'N2CC800E16V1' 'N2CC801E16V1' 'N2CC802E16V1'   \
                    #--exp_color     'l_orange_0.7' 'l_green_0.7'  'l_purple_0.3'   \
                    #--exp_linestyle 'dashed'       'solid'        'solid'          \
                    #--exp_linewidth '2.5'          '2'            '2'              \
