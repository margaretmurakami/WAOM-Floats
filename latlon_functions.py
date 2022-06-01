def interpolate(xarr,yarr,ds):
    """
    inputs:
        ds: the dataset with lat and long values
        xarr: the current row of the Xgrid array
        yarr: the current row of the Ygrid array
    returns:
        points: the lat/lon values of the current array
    """
    lat_values = ds.lat_rho.values
    long_values = ds.lon_rho.values
    lat = np.array([])
    long = np.array([])
    
    for i,j in zip(xarr,yarr):
        # interpolate in latitude
        x_shape = np.arange(ds.lat_rho.shape[0])
        y_shape = np.arange(ds.lat_rho.shape[1])
        interp_x = i
        interp_y = j
        # Note the following two lines that are used to set up the
        interp_mesh = np.array(np.meshgrid(interp_x, interp_y))
        interp_points = np.rollaxis(interp_mesh, 0, 3).reshape((1, 2))
        # Perform the interpolation
        interp_arr = interpn((x_shape, y_shape), lat_values, interp_points)
        lat = np.append(interp_arr[0],lat)
        
        # interpolate in longitude
        x_shape = np.arange(ds.lon_rho.shape[0])
        y_shape = np.arange(ds.lon_rho.shape[1])
        interp_x = j
        interp_y = i
        # Note the following two lines that are used to set up the
        interp_mesh = np.array(np.meshgrid(interp_x, interp_y))
        interp_points = np.rollaxis(interp_mesh, 0, 3).reshape((1, 2))
        # Perform the interpolation
        interp_arr = interpn((x_shape, y_shape), long_values, interp_points)
        long = np.append(interp_arr[0],long)
    return (long,lat)


    # write a function to get the long and lat from the grid points
def grid_to_spherical(x,y,ds):
    """
    x: array of grid x position values
    y: array of grid y position values
    rho: the used xi_rho value 
    """
    x_long = np.empty((0,x.shape[1]))
    y_lat = np.empty((0,y.shape[1]))
    
    # first create the points in the other array
    # get the maximum and minimum values of x and y
    for i in range(len(x)):
        
        # get the min and max of x and y
        minx = (np.nanmin(x[i]))
        maxx = (np.nanmax(x[i]))
        if not (math.isnan(minx)) and not (math.isnan(maxx)):
            x_i,y_i = interpolate(x[i],y[i],ds)
        else:
            x_i,y_i = x[i],y[i]
        x_long = np.append(np.array([x_i]),x_long,axis=0)
        y_lat = np.append(np.array([y_i]),y_lat,axis=0)
        
    return (x_long,y_lat)
