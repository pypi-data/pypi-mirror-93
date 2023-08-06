
def twod_panels(params, domain, twod_avg_list, leadtime_minutes,
                hist_bin_edges, avg_reference_hists, avg_verified_hists):
    """plot 2D pannels statistics

    what is being plotted is defined in params.twod_panels from the bottom up
    """

    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    import domcmc.fst_tools as fst_tools
    import domutils.legs as legs
    import domutils.geo_tools as geo_tools
    import domutils.radar_tools as radar_tools
    import domutils._py_tools as py_tools
    import gridded_obs.plot 

    n_stat_types  = len(params.twod_panels)
    n_panels = len(twod_avg_list)

    #missing val
    missing = -9999.

    #figure dimensions
    ratio  = 0.75
    rec_w  = 4.           # Horizontal size of a panel
    rec_h  = ratio*rec_w  # Vertical size of a panel
    sp_w   = 1.2           # horizontal space between panels
    sp_h   = 1.           # vertical space between panels
    pal_sp = .05          # space between panel and palette
    pal_w  = .17          # width of palette
    tit_h  = 1.6 + 0.5*np.ceil(len(params.exp_list)/2.)  # height of title
    #size of figure
    fig_w  = sp_w + n_panels*(rec_w + sp_w) +  sp_w
    fig_h  = sp_h + n_stat_types*(rec_h+sp_h) + tit_h + .9
    #normalize sizes relative to figure
    rec_w  = rec_w / fig_w
    rec_h  = rec_h / fig_h
    sp_w   = sp_w / fig_w
    sp_h   = sp_h / fig_h
    pal_sp = pal_sp / fig_w
    pal_w  = pal_w / fig_w
    tit_h  = tit_h / fig_h
    #pixel resolution of image being generated
    grid_w_pts = 1200.
    image_dpi = grid_w_pts/(rec_w*fig_w)
    image_res = [grid_w_pts,ratio*grid_w_pts]

    #larger typeface
    mpl.rcParams.update({'font.size': 20})
    # Use this for editable text in svg
    mpl.rcParams['text.usetex']  = False
    mpl.rcParams['svg.fonttype'] = 'none'
    # Hi def figure
    mpl.rcParams['figure.dpi'] = 600

    #instantiate figure
    fig = plt.figure(figsize=(fig_w, fig_h))

    #header, legend and other explanations
    gridded_obs.plot.plot_header(fig, domain, params,
                                 fig_w  , fig_h  ,
                                 rec_w  , rec_h,
                                 sp_w   , sp_h,
                                 pal_sp , pal_w,
                                 tit_h  )

    for nn, stat_type in enumerate(params.twod_panels):
        y0 = sp_h + nn*(rec_h + sp_h) 
        
        params.ylim_hist = None
        if params.ylim_hist is not None:
            y_lim = params.ylim_hist
        else:
            y_lim = gridded_obs.plot.autorange(avg_reference_hists)
            y_lim = (0., y_lim[1])   #no bottom headspace for histograms

        for ii, lt_inds in enumerate(twod_avg_list):
            x0 = sp_w + ii*(rec_w + sp_w) 
            pos = [x0, y0, rec_w, rec_h]


            #Setup the general look 
            #Ticks length and width
            major_height = 5
            major_width = .3
            minor_height = 2
            minor_width = .3
            #axes containing data
            ax = fig.add_axes(pos, label = 'twod_plot', zorder=10)
            ax.set_facecolor((0.,0.,0.,0.))
            #ax.set_xlim((leadtime_hours[0], leadtime_hours[-1]))
            ax.set_ylim(y_lim)
            #ax.tick_params(axis='both', which='both', direction='in', top='on', right=True)
            #ax.set_xticks(xticks)
            #ax.set_yticks(this_var_info['ticks']) 
            #ax.tick_params('both', length=major_height, width=major_width, which='major')
            #ax.tick_params('both', length=minor_height, width=minor_width, which='minor')
            #if nn == 0:
            #    ax.set_xlabel('Leadtime (h)')
            #else:
            #    ax.set_xticklabels([])
            #ax.set_ylabel(unit_dict[score])
            ax.set_xscale('log')
            ax.set_xlim((1e-2,1e2))
            ## set x ticks
            x_major = matplotlib.ticker.FixedLocator([1e-2, 1e-1, 1., 1e1, 1e2])
            #major = matplotlib.ticker.LogLocator(base = 10.0, numticks = 5)
            ax.xaxis.set_major_locator(x_major)
            x_minor = matplotlib.ticker.LogLocator(base = 10.0, subs = np.arange(1.0, 10.0) * 0.1, numticks = 10)
            #x_minor = matplotlib.ticker.Formatter
            ax.xaxis.set_minor_locator(x_minor)
            #ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%f2.0'))
            ax.set_xticklabels(['0.01', '0.1', '1', '10', '100' ])
            ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

            #ax info
            minute_0 = leadtime_minutes[lt_inds[0]]
            minute_f = leadtime_minutes[lt_inds[-1]]
            bound_str = '[{:4d}m,{:4d}m]'.format(minute_0, minute_f)
            ax.annotate(bound_str, (.50, .96), xycoords='axes fraction', ha='left', va='top', fontsize=18)

            left  = hist_bin_edges[:-1]
            right = hist_bin_edges[1:]
            xx = np.array([left,right]).T.flatten()

            #for reference_data
            bin_v = avg_reference_hists[ii,:]
            yy = np.array([bin_v,bin_v]).T.flatten()
            ax.plot(  xx, yy, color='black')

            for kk, experiment in enumerate(params.exp_list):
                bin_v = avg_verified_hists[kk,ii,:]
                yy = np.array([bin_v,bin_v]).T.flatten()
                ax.plot( xx, yy,color=params.exp_color[kk], 
                                linestyle=params.exp_linestyle[kk], 
                                linewidth=params.exp_linewidth[kk], )
    #save image
    date_dir = params.score_dir+ params.date_list[0].strftime('%Y%m%d%H')+'_to_'+ params.date_list[-1].strftime('%Y%m%d%H')
    py_tools.parallel_mkdir(date_dir)
    svg_name = date_dir+'/twod_panels__'+domain+'.svg'
    plt.savefig(svg_name, dpi=image_dpi)
    plt.close(fig)
    py_tools.lmroman(svg_name)
    #py_tools.convert(svg_name,'gif', del_orig=True, density=400, geometry='50%')
    print('done with: ', svg_name)


