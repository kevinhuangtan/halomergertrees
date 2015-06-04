import os
import numpy as np
import h5py

class RockstarReader(object):

    def __init__(self, filename):
        """
        RockstarReader(filename)
        """
        

        if not os.path.isfile(filename):
            raise IOError("Input filename %s is not a file" % filename)
        self.f = h5py.File('sample1.hdf5', 'w')  
        self.fname = filename
        self._uncompress_ascii()

    def get_header(self):
        header = {}
        with open(self.fname) as ascii_file:
            header['ascii_header'] = []
            for i, line in enumerate(ascii_file):
                header['ascii_header'].append(line)
                #create categories from first line
                if(i==0):
                    header['categories'] = line.split()
                if(line[0]!='#'):
                    break

        hd_header = self.f.create_group('header')
        hd_header['categories'] = np.asarray(header['categories'])
        hd_header['ascii_header'] = header['ascii_header']
        print header['ascii_header']


    def _uncompress_ascii(self):
        """ If the input fname has file extension `.gz`, 
        then the method uses `gunzip` to decompress it, 
        and returns the input fname truncated to exclude 
        the `.gz` extension. If the input fname does not 
        end in `.gz`, method does nothing besides return 
        the input fname. 
        """
        if self.fname[-3:]=='.gz':
            print("...uncompressing ASCII data")
            os.system("gunzip "+self.fname)
            self.fname = self.fname[:-3]
        else:
            pass
        return

