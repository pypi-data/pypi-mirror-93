def plot_circles(ax, lats, lons, radius):

    #plot circles to debug lmin code
    import cartopy
    import cartopy.crs 
    import domutils.geo_tools as geo_tools
    import numpy as np

    #plot radar circles  
    proj_cart = cartopy.crs.PlateCarree()
    transform = proj_cart._as_mpl_transform(ax)
    azimuths = np.arange(0.,361)
    for this_lat, this_lon in zip(lats.ravel(),lons.ravel()):
        ranges   = np.full_like(azimuths, radius)
        lon1_arr = np.full_like(azimuths, this_lon)
        lat1_arr = np.full_like(azimuths, this_lat)
        rlons, rlats = geo_tools.lat_lon_range_az(lon1_in   =   lon1_arr, 
                                                  lat1_in   =   lat1_arr,
                                                  range_in  =   ranges,
                                                  azimuth_in=   azimuths)
        #circles
        color=(0./256.,81./256.,237./256.)
        ax.plot(rlons, rlats, transform=proj_cart, c=color, zorder=300, linewidth=.1)
        ax.scatter(this_lon, this_lat, transform=proj_cart, color=color, zorder=300, s=1.**2.)

        break



def plot_geo(ax):
    import cartopy.feature as cfeature
    ax.outline_patch.set_linewidth(.3)
    ax.add_feature(cfeature.STATES.with_scale('50m'), linewidth=0.2, edgecolor='0.6')


def compare_fields(reference_v_in, reference_qi_in, verified_v_in,
                   latitudes, longitudes, 
                   threshold, 
                   pic_dir, validity_date, leadtime, 
                   radius=None):
    """image of reference,quality index and verified fields
    """

    import datetime
    import os
    import numpy as np
    import pickle
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import domcmc.fst_tools as fst_tools
    import domutils.legs as legs
    import domutils.geo_tools as geo_tools
    import domutils.radar_tools as radar_tools
    import domutils._py_tools as py_tools


    #show data only above threshold
    reference_v  = reference_v_in 
    reference_qi = reference_qi_in 
    verified_v  = verified_v_in  


    #date that will be displayed
    this_date = validity_date + leadtime

    #missing val
    missing = -9999.

    #figure dimensions
    ratio  = 0.5
    rec_w  = 6.           # Horizontal size of a panel
    rec_h  = ratio*rec_w  # Vertical size of a panel
    sp_w   = .2           # horizontal space between panels
    sp_h   = 1.           # vertical space between panels
    pal_sp = .05           # spavce between panel and palette
    pal_w  = .17          # width of palette
    tit_h  = .1           # height of title
    #size of figure
    n_exp  = 4
    n_panels = 2
    fig_w  = 21.
    fig_h  = 9.
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
    #objects to handle color mappings
    pr_color_map = legs.PalObj(range_arr=[.1,.5,1.,5.,10.,20.,50.],
                                  n_col=6, 
                                  over_high='extend', under_low='white',
                                  excep_val=missing, excep_col='grey_220')
    #larger typeface
    mpl.rcParams.update({'font.size': 18})
    # Use this for editable text in svg
    mpl.rcParams['text.usetex']  = False
    mpl.rcParams['svg.fonttype'] = 'none'
    # Hi def figure
    mpl.rcParams['figure.dpi'] = 600

    #custom pastel color segments for QI index
    pastel = [ [[255,190,187],[230,104, 96]],  #pale/dark red
               [[255,185,255],[147, 78,172]],  #pale/dark purple
               [[255,227,215],[205,144, 73]],  #pale/dark brown
               [[210,235,255],[ 58,134,237]],  #pale/dark blue
               [[223,255,232],[ 61,189, 63]] ] #pale/dark green
    qi_color_map = legs.PalObj(range_arr=[0., 1.],
                               dark_pos='high',
                               color_arr=pastel,
                               excep_val=[missing, 0.],
                               excep_col=['grey_220', 'white'])

    # Full national grid
    # Use rotated pole projection
    # Use rotated pole projection
    pole_latitude=35.7
    pole_longitude=65.5
    lat_0 = 48.8
    delta_lat = 9.6
    lon_0 = 266.1
    delta_lon = 40.1
    map_extent_full=[lon_0-delta_lon, lon_0+delta_lon, lat_0-delta_lat, lat_0+delta_lat]  
    crs_full = ccrs.RotatedPole(pole_latitude=pole_latitude, pole_longitude=pole_longitude)

    #instantiate objects to handle geographical projection of data this needs to be done only once
    # onto geoAxes with this specific crs 
    proj_obj_full = geo_tools.ProjInds(src_lon=longitudes, src_lat=latitudes, 
                                       dest_crs=crs_full, extent=map_extent_full,
                                       image_res=image_res)

    #instantiate figure
    fig = plt.figure(figsize=(fig_w, fig_h))

    proj_obj_list = [proj_obj_full]
    crs_list      = [crs_full]
    extent_list   = [map_extent_full]

    for ii, [this_proj_obj, this_crs, this_extent] in enumerate(zip(proj_obj_list,crs_list,extent_list)):

        #Y position of row
        y0 = sp_h + (1.-ii)*(sp_h+rec_h)
        #title offset
        xp = .04
        yp = 1.01

        #reference values
        x0 = 0.1/fig_w
        pos = [x0, y0, rec_w, rec_h]
        ax = fig.add_axes(pos, projection=this_crs, extent=this_extent)
        #title
        ax.annotate('reference_val', size=22, xy=(xp, yp), xycoords='axes fraction')
        #print date only once
        if ii ==0:
            ax.annotate(this_date.strftime('%Y-%m-%d %Hh%M'), size=24, xy=(xp, 1.2), xycoords='axes fraction')
        #geographical projection of data into axes space
        #ddp
        projected_data = this_proj_obj.project_data(reference_v)
        #draw color figure onto axes
        pr_color_map.plot_data(ax=ax, data=projected_data)
        #format axes and draw geographical boundaries
        plot_geo(ax)

        #verified_val
        x0 = 0.1/fig_w + sp_w + rec_w
        pos = [x0, y0, rec_w, rec_h]
        ax2 = fig.add_axes(pos, projection=this_crs, extent=this_extent)
        #title
        ax2.annotate('verified_val', size=22, xy=(xp, yp), xycoords='axes fraction')
        #geographical projection of data into axes space
        #ddp
        projected_data = this_proj_obj.project_data(verified_v)
        #draw color figure onto axes
        pr_color_map.plot_data(ax=ax2, data=projected_data)
        #format axes and draw geographical boundaries
        plot_geo(ax2)
        #palette
        pal_pos = [x0+rec_w+pal_sp, y0, pal_w, rec_h]
        pr_color_map.plot_palette(pal_pos=pal_pos, 
                                     pal_linewidth=0.3, pal_units='[mm]',
                                     pal_format='{:3.0f}', equal_legs=True)

        #
        #
        #plot circles
        if radius is not None:
            delta_pt = 40
            subset_lat =  latitudes[::delta_pt,::delta_pt]
            subset_lon = longitudes[::delta_pt,::delta_pt]
            plot_circles(ax2, subset_lat, subset_lon, radius)

        ##plot circle selection
        #p_file = '/space/hall3/sitestore/eccc/mrd/rpndat/dja001/lmin_investigate/pts.pickle'
        #with open(p_file, 'rb') as f_handle:
        #    rec_dict = pickle.load(f_handle)
        #p_file = '/space/hall3/sitestore/eccc/mrd/rpndat/dja001/lmin_investigate/ll.pickle'
        #with open(p_file, 'rb') as f_handle:
        #    ll_dict = pickle.load(f_handle)
        #proj_cart = ccrs.PlateCarree()
        #print('number of balls', len(rec_dict['pt_list']))
        #for ball_list in rec_dict['pt_list']:
        #    ax2.scatter(ll_dict['longitudes'][ball_list], ll_dict['latitudes'][ball_list], 
        #                transform=proj_cart, color=(203./256.,26./256.,35./256.),zorder=300, s=.05**2.)




        #reference quality index
        x0 = 0.1/fig_w + 2.*(sp_w + rec_w)+ 5.*sp_w
        pos = [x0, y0, rec_w, rec_h]
        ax3 = fig.add_axes(pos, projection=this_crs, extent=this_extent)
        #title
        ax3.annotate('Quality index', size=22, xy=(xp, yp), xycoords='axes fraction')
        #geographical projection of data into axes space
        #ddp
        projected_data = this_proj_obj.project_data(reference_qi)
        #draw color figure onto axes
        qi_color_map.plot_data(ax=ax3, data=projected_data)
        #format axes and draw geographical boundaries
        plot_geo(ax3)
        #palette
        pal_pos = [x0+rec_w+pal_sp, y0, pal_w, rec_h]
        qi_color_map.plot_palette(pal_pos=pal_pos, 
                                  pal_linewidth=0.3, pal_units='[unitless]',
                                  pal_format='{:2.1f}')

    #make dir if it does not exist
    if not os.path.isdir(pic_dir):
        domutils._py_tools.parallel_mkdir(pic_dir)

    #figure name
    if not np.isclose(leadtime.seconds, 0):
        lt_minutes = leadtime.days*1440. + np.floor(leadtime.seconds/60.)
        svg_name = pic_dir+'/compare_fields_'+validity_date.strftime('%Y%m%d%H%M')+'{:+06.0f}m_th{:04.1f}'.format(lt_minutes, threshold)+'.svg'
    else:
        svg_name = pic_dir+'/compare_fields_'+validity_date.strftime('%Y%m%d%H%M')+'_th{:03.0f}'.format(threshold)+'.svg'
    plt.savefig(svg_name, dpi=image_dpi)
    plt.close(fig)
    py_tools.lmroman(svg_name)
    #py_tools.convert(svg_name,'gif', del_orig=True, density=400, geometry='50%')
    print('done with: ', svg_name)


def plot_fraction(reference_v_in, longitudes, latitudes, 
                  rf=None, rfi=None,
                  vf=None, vfi=None,
                  radius=None):
    """image of fractions for FSS
    """

    if rf is not None:
        reference_fractions = rf
    if rfi is not None:
        reference_fractions_int = rfi
    if vf is not None:
        verified_fractions = vf
    if vfi is not None:
        verified_fractions_int = vfi


    import datetime
    import os
    import numpy as np
    import pickle
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import domcmc.fst_tools as fst_tools
    import domutils.legs as legs
    import domutils.geo_tools as geo_tools
    import domutils.radar_tools as radar_tools
    import domutils._py_tools as py_tools


    #show data only above threshold
    reference_v  = reference_v_in

    #missing val
    missing = -9999.

    #figure dimensions
    ratio  = 0.5
    rec_w  = 6.           # Horizontal size of a panel
    rec_h  = ratio*rec_w  # Vertical size of a panel
    sp_w   = .2           # horizontal space between panels
    sp_h   = 1.           # vertical space between panels
    pal_sp = .05           # spavce between panel and palette
    pal_w  = .17          # width of palette
    tit_h  = .1           # height of title
    #size of figure
    n_exp  = 4
    n_panels = 2
    fig_w  = 21.
    fig_h  = 9.
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
    #objects to handle color mappings
    pr_color_map = legs.PalObj(range_arr=[.1,.5,1.,5.,10.,20.,50.],
                                  n_col=6, 
                                  over_high='extend', under_low='white',
                                  excep_val=missing, excep_col='grey_220')
    #larger typeface
    mpl.rcParams.update({'font.size': 18})
    # Use this for editable text in svg
    mpl.rcParams['text.usetex']  = False
    mpl.rcParams['svg.fonttype'] = 'none'
    # Hi def figure
    mpl.rcParams['figure.dpi'] = 600

    #custom pastel color segments for QI index
    pastel = [ [[255,190,187],[230,104, 96]],  #pale/dark red
               [[255,185,255],[147, 78,172]],  #pale/dark purple
               [[255,227,215],[205,144, 73]],  #pale/dark brown
               [[210,235,255],[ 58,134,237]],  #pale/dark blue
               [[223,255,232],[ 61,189, 63]] ] #pale/dark green
    qi_color_map = legs.PalObj(range_arr=[0., .2],
                               dark_pos='high',
                               color_arr=pastel,
                               over_under='extend',
                               excep_val=[missing, 0.,-1.],
                               excep_col=['grey_220', 'white', 'dark_red'])

    # Full national grid
    # Use rotated pole projection
    # Use rotated pole projection
    pole_latitude=35.7
    pole_longitude=65.5
    lat_0 = 48.8
    delta_lat = 9.6
    lon_0 = 266.1
    delta_lon = 40.1
    map_extent_full=[lon_0-delta_lon, lon_0+delta_lon, lat_0-delta_lat, lat_0+delta_lat]  
    crs_full = ccrs.RotatedPole(pole_latitude=pole_latitude, pole_longitude=pole_longitude)

    #instantiate objects to handle geographical projection of data this needs to be done only once
    # onto geoAxes with this specific crs 
    proj_obj_full = geo_tools.ProjInds(src_lon=longitudes, src_lat=latitudes, 
                                       dest_crs=crs_full, extent=map_extent_full,
                                       image_res=image_res)

    #instantiate figure
    fig = plt.figure(figsize=(fig_w, fig_h))

    proj_obj_list = [proj_obj_full]
    crs_list      = [crs_full]
    extent_list   = [map_extent_full]

    for ii, [this_proj_obj, this_crs, this_extent] in enumerate(zip(proj_obj_list,crs_list,extent_list)):

        #title offset
        xp = .04
        yp = 1.01

        #reference values
        x0 = 0.1/fig_w
        y0 = sp_h + (1.-ii)*(sp_h+rec_h)
        pos = [x0, y0, rec_w, rec_h]
        ax = fig.add_axes(pos, projection=this_crs, extent=this_extent)
        #title
        ax.annotate('reference_val', size=22, xy=(xp, yp), xycoords='axes fraction')
        #print date only once
        #if ii ==0:
            #ax.annotate(this_date.strftime('%Y-%m-%d %Hh%M'), size=24, xy=(xp, 1.2), xycoords='axes fraction')
        #geographical projection of data into axes space
        #ddp
        projected_data = this_proj_obj.project_data(reference_v)
        #draw color figure onto axes
        pr_color_map.plot_data(ax=ax, data=projected_data)
        #format axes and draw geographical boundaries
        plot_geo(ax)
        #palette
        pal_pos = [x0+rec_w+pal_sp, y0, pal_w, rec_h]
        pr_color_map.plot_palette(pal_pos=pal_pos, 
                                  pal_linewidth=0.3, pal_units='[mm/h]',
                                  pal_format='{:3.0f}', equal_legs=True)


        #full grid computation
        if rf is not None:
            x0 = 0.1/fig_w + 1.*(sp_w + rec_w)+ 5.*sp_w
            y0 = sp_h + (1.-ii)*(sp_h+rec_h)
            pos = [x0, y0, rec_w, rec_h]
            ax2 = fig.add_axes(pos, projection=this_crs, extent=this_extent)
            #title
            ax2.annotate('reference fractions', size=22, xy=(xp, yp), xycoords='axes fraction')
            #geographical projection of data into axes space
            #ddp
            projected_data = this_proj_obj.project_data(reference_fractions)
            #draw color figure onto axes
            qi_color_map.plot_data(ax=ax2, data=projected_data)
            #format axes and draw geographical boundaries
            plot_geo(ax2)
            ##palette
            #pal_pos = [x0+rec_w+pal_sp, y0, pal_w, rec_h]
            #qi_color_map.plot_palette(pal_pos=pal_pos, 
            #                             pal_linewidth=0.3, pal_units='[mm]',
            #                             pal_format='{:3.0f}', equal_legs=True)

        #
        if vf is not None:
            x0 = 0.1/fig_w + 1.*(sp_w + rec_w)+ 5.*sp_w
            y0 = sp_h + (0.-ii)*(sp_h+rec_h)
            #
            x0 = 0.1/fig_w + 1.*(sp_w + rec_w)+ 5.*sp_w
            pos = [x0, y0, rec_w, rec_h]
            ax3 = fig.add_axes(pos, projection=this_crs, extent=this_extent)
            #title
            ax3.annotate('verified fractions', size=22, xy=(xp, yp), xycoords='axes fraction')
            #geographical projection of data into axes space
            #ddp
            projected_data = this_proj_obj.project_data(verified_fractions)
            #draw color figure onto axes
            qi_color_map.plot_data(ax=ax3, data=projected_data)
            #format axes and draw geographical boundaries
            plot_geo(ax3)
            ##palette
            #pal_pos = [x0+rec_w+pal_sp, y0, pal_w, rec_h]
            #qi_color_map.plot_palette(pal_pos=pal_pos, 
            #                             pal_linewidth=0.3, pal_units='[mm]',
            #                             pal_format='{:3.0f}', equal_legs=True)


        ##
        ##
        ##plot circles
        #if radius is not None:
        #    delta_pt = 40
        #    subset_lat =  latitudes[::delta_pt,::delta_pt]
        #    subset_lon = longitudes[::delta_pt,::delta_pt]
        #    plot_circles(ax2, subset_lat, subset_lon, radius)

        ##plot circle selection
        #p_file = '/space/hall3/sitestore/eccc/mrd/rpndat/dja001/lmin_investigate/pts.pickle'
        #with open(p_file, 'rb') as f_handle:
        #    rec_dict = pickle.load(f_handle)
        #p_file = '/space/hall3/sitestore/eccc/mrd/rpndat/dja001/lmin_investigate/ll.pickle'
        #with open(p_file, 'rb') as f_handle:
        #    ll_dict = pickle.load(f_handle)

        #proj_cart = ccrs.PlateCarree()
        #print('number of balls', len(rec_dict['pt_list']))
        #for ball_list in rec_dict['pt_list']:
        #    ax2.scatter(ll_dict['longitudes'][ball_list], ll_dict['latitudes'][ball_list], 
        #                transform=proj_cart, color=(203./256.,26./256.,35./256.),zorder=300, s=.05**2.)



        #reference_fractions_int  = np.where(reference_fractions_int < 0., -1., reference_fractions_int)
        #verified_fractions_int   = np.where(verified_fractions_int < 0., -1., verified_fractions_int)

        if rfi is not None:
            x0 = 0.1/fig_w + 2.*(sp_w + rec_w)+ 5.*sp_w
            y0 = sp_h + (1.-ii)*(sp_h+rec_h)
            pos = [x0, y0, rec_w, rec_h]
            ax4 = fig.add_axes(pos, projection=this_crs, extent=this_extent)
            #title
            ax4.annotate('reference interpolated', size=22, xy=(xp, yp), xycoords='axes fraction')
            #geographical projection of data into axes space
            #ddp
            projected_data = this_proj_obj.project_data(reference_fractions_int)
            #draw color figure onto axes
            qi_color_map.plot_data(ax=ax4, data=projected_data)
            #format axes and draw geographical boundaries
            plot_geo(ax4)
            #palette
            pal_pos = [x0+rec_w+pal_sp, y0, pal_w, rec_h]
            qi_color_map.plot_palette(pal_pos=pal_pos, 
                                      pal_linewidth=0.3, pal_units='[unitless]',
                                      pal_format='{:2.1f}')
        #
        if vfi is not None:
            x0 = 0.1/fig_w + 2.*(sp_w + rec_w)+ 5.*sp_w
            y0 = sp_h + (0.-ii)*(sp_h+rec_h)
            #reference fraction
            x0 = 0.1/fig_w + 2.*(sp_w + rec_w)+ 5.*sp_w
            pos = [x0, y0, rec_w, rec_h]
            ax5 = fig.add_axes(pos, projection=this_crs, extent=this_extent)
            #title
            ax5.annotate('verified interpolated', size=22, xy=(xp, yp), xycoords='axes fraction')
            #geographical projection of data into axes space
            #ddp
            projected_data = this_proj_obj.project_data(verified_fractions_int)
            #draw color figure onto axes
            qi_color_map.plot_data(ax=ax5, data=projected_data)
            #format axes and draw geographical boundaries
            plot_geo(ax5)
            #palette
            pal_pos = [x0+rec_w+pal_sp, y0, pal_w, rec_h]
            qi_color_map.plot_palette(pal_pos=pal_pos, 
                                      pal_linewidth=0.3, pal_units='[unitless]',
                                      pal_format='{:2.1f}')

    #make dir if it does not exist
    pic_dir='/space/hall3/sitestore/eccc/mrd/rpndat/dja001/test_new_griddedobs/' 
    if not os.path.isdir(pic_dir):
        domutils._py_tools.parallel_mkdir(pic_dir)

    #figure name
    #if not np.isclose(leadtime.seconds, 0):
    #    lt_minutes = leadtime.days*1440. + np.floor(leadtime.seconds/60.)
    #    svg_name = pic_dir+'/compare_fields_'+validity_date.strftime('%Y%m%d%H%M')+'{:+06.0f}m_th{:04.1f}'.format(lt_minutes, threshold)+'.svg'
    #else:
    #    svg_name = pic_dir+'/compare_fields_'+validity_date.strftime('%Y%m%d%H%M')+'_th{:03.0f}'.format(threshold)+'.svg'
    svg_name = pic_dir+'/compare_fractions_radius'+'{:05.2f}'.format(radius)+'.svg'
    plt.savefig(svg_name, dpi=image_dpi)
    plt.close(fig)
    py_tools.lmroman(svg_name)
    #py_tools.convert(svg_name,'gif', del_orig=True, density=400, geometry='50%')
    print('done with: ', svg_name)


if __name__ == "__main__":     
    main()
