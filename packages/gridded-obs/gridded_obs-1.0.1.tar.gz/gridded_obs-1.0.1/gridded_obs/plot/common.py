"""ploting routines
"""

def plot_header( fig, domain, params, 
                 fig_w  , fig_h  ,
                 rec_w  , rec_h  ,
                 sp_w   , sp_h   ,
                 pal_sp , pal_w  ,
                 tit_h  , 
                 threshold=None):
    '''header for figure
    '''

    tit_w = 8./fig_w
    pos = [0.,1.-tit_h,tit_w,tit_h] 
    y_top = 0.95
    linespace = .5/(tit_h*fig_h)
    tit_ax = fig.add_axes(pos, zorder=10)
    tit_ax.set_facecolor((0.,0.,0.,0.))
    tit_ax.set_xlim((0.,1.))
    tit_ax.set_ylim((0.,1.))
    tit_ax.axis('off')
    #date range
    date_str = params.date_list[0].strftime('%Y%m%d%H')+' - '+params.date_list[-1].strftime('%Y%m%d%H')
    tit_ax.annotate(date_str,(sp_w, y_top-0.*linespace),           xycoords='axes fraction', ha='left', va='top', fontsize=24)
    #number of forecasts
    num_str = '{:5d}'.format(len(params.date_list))+ ' forecasts considered'
    tit_ax.annotate(num_str, (.9, y_top-0.*linespace), xycoords='axes fraction', ha='left', va='top', fontsize=24)
    #thresholds
    if threshold is not None:
        th_str = 'threshold: '+'{:10.4f}'.format(threshold)
        tit_ax.annotate(th_str, (sp_w, y_top-1.*linespace), xycoords='axes fraction', ha='left', va='top', fontsize=24)
    #domain
    do_str = 'on domain: '+domain
    tit_ax.annotate(do_str, (.9, y_top-1.*linespace), xycoords='axes fraction', ha='left', va='top', fontsize=24)
    #legend for identifying experiments
    l_top = y_top - 1.5/(tit_h*fig_h)
    xs = [.1, .8 ]
    ys = [l_top, l_top-.5/(tit_h*fig_h), l_top-1./(tit_h*fig_h)]
    pos_list = [(xx,yy) for yy in ys for xx in xs]
    line_l = .17
    for kk, experiment in enumerate(params.exp_list):
        xx = pos_list[kk][0]
        yy = pos_list[kk][1]
        tit_ax.plot(   [xx, xx+line_l], [yy, yy], 
                       color=params.exp_color[kk], 
                       linestyle=params.exp_linestyle[kk], 
                       linewidth=2.*params.exp_linewidth[kk], )
        tit_ax.annotate(experiment, (xx+line_l, yy), xycoords='data', ha='left', va='center', fontsize=24)

def autorange(score):
    '''determine nim max range for multiple experiments
    '''

    import numpy as np

    minv = np.nanmin(score)
    maxv = np.nanmax(score)
    rangev = maxv - minv
    headspace = .10 # % headspace below and above max value; improves readability

    return (minv - headspace*rangev, maxv + headspace*rangev )








