import os

class RockstarReader(object):

    def __init__(self, filename):
        """
        RockstarReader(filename)
        """

        if not os.path.isfile(filename):
            raise IOError("Input filename %s is not a file" % filename)
                
        self.fname = filename
        self._uncompress_ascii()

    def get_header(self):
        """ Return the header as a list of strings, 
        one entry per header row. 

        Parameters 
        ----------
        fname : string 

        Nrows_header_total :  int, optional
            If the total number of header rows is not known in advance, 
            method will call `header_len` to determine Nrows_header_total. 

        Notes 
        -----
        Empty lines will be included in the returned header. 

        """

        with open(self.fname) as f:
            line = f.readline()
            s = line.split()
            print s
        return 

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

