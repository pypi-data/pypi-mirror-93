
class ModelFst:
    def __init__(self, name=None, data_dir=None, file_struc=None, varname=None, qi_varname=None):
        """reader for CMC 'standard' files

        args:
            data_dir:      [str]  /basse/dir/where/data/is/
            file_struc:    [strftime format]  how to construct filename from date
            varname:       [str] Name of variable to read in standard file
        """

        print('initializing "ModelFst" reader')

        if name is not None:
            self.name  = name
        else:
            raise ValueError('keyword "name" must be speficied')

        if data_dir is not None:
            self.data_dir  = data_dir
        else:
            raise ValueError('keyword "data_dir" must be speficied')

        if file_struc is not None:
            self.file_struc  = file_struc
        else:
            raise ValueError('keyword "file_struc" must be speficied')

        if varname is not None:
            self.varname  = varname
        else:
            raise ValueError('keyword "varname" must be speficied')

        #optionnal variable
        self.qi_varname = qi_varname

    def get_data(self, validity_date, leadtime=None):
        """read data from a standard file

        args:
            validity_date:  [datetime object]  date at which data is desired
            leadtime:       [datetime timedelta object]  offset with respect to validity time

        """

        import domcmc.fst_tools 
        import numpy as np

        #take leadtime into account
        if leadtime is None:
            this_date = validity_date
        else:
            this_date = validity_date + leadtime

        this_file = self.data_dir + this_date.strftime(self.file_struc)

        data_dict = domcmc.fst_tools.get_data(file_name=this_file, var_name=self.varname, datev=this_date, latlon=True)

        #get quality index 
        if self.qi_varname is not None:
            qi_dict = domcmc.fst_tools.get_data(file_name=this_file, var_name=self.qi_varname, datev=this_date)
            if qi_dict is not None:
                qi_values = qi_dict['values']
            else:
                qi_values = None
        else:
            qi_values = None


        if data_dict is None:
            return None
        else:
            return {'values':data_dict['values'], 
                    'qi_values':qi_values,
                    'lats':data_dict['lat'], 
                    'lons':data_dict['lon']}

