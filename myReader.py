import os
import numpy as np
import h5py


if(a.f):
  a.f.close()


class RockstarReader(object):

    def __init__(self, filename):
        """
        RockstarReader(filename)
        """
        

        if not os.path.isfile(filename):
            raise IOError("Input filename %s is not a file" % filename)
        self.f = h5py.File('sample.hdf5', 'w')  
        self.fname = filename
        self._uncompress_ascii()
        self.get_header()
        self.num_trees = 0
        self.tree_ids = []
        self.tree_space = self.create_tree_space()
        self.forest = self.read_in_trees()

    def get_header(self):
        header = {}
        hd_header = self.f.create_group('header')
        with open(self.fname) as ascii_file:
            header['ascii_header'] = []
            for i, line in enumerate(ascii_file):
                header['ascii_header'].append(line)
                #create categories from first line
                if(i==0):
                    header['categories'] = line.split()
                if(line[0]!='#'):
                    hd_header.attrs['length'] = i
                    break
        hd_header['categories'] = np.asarray(header['categories'])
        hd_header['ascii_header'] = header['ascii_header']

    def create_tree_space(self): #stores length of each tree in array
        f = self.f
        with open(self.fname) as ascii_file:

             #skip header lines
            for _ in xrange(f['header'].attrs['length']):
                next(ascii_file)    

            #number of trees in file
            self.num_trees = int(next(ascii_file))

            #inialize array of trees
            tree_ids = [0] * (self.num_trees)
            # tree_sizes = {}
            tree_sizes_array = [0] * self.num_trees

            #iterate through lines in file
            tree_index = 0
            tree_size = 0
            for line in ascii_file:
                if(line[0]=='#'): #new tree
                    if(tree_size!=0): #if not first line (first tree), add tree size to last tree
                        # tree_sizes[tree_ids[tree_index]] = tree_size
                        tree_sizes_array[tree_index] = tree_size
                        tree_size = 0
                        tree_index = tree_index + 1
                    tree_ids[tree_index] = int(line[6:]) #next tree id
                   
                else: #add to tree size if not a new tree
                    tree_size = tree_size + 1

            #last tree before EOF
            # tree_sizes[tree_ids[tree_index]] = tree_size
            tree_sizes_array[tree_index] = tree_size
        self.tree_ids = tree_ids
        return tree_sizes_array


    def read_in_trees(self):
        f = self.f
        tree_space = self.tree_space
        tree_ids = self.tree_ids
        forest = {}
        with open(self.fname) as ascii_file:
             #skip header lines
            for _ in xrange(f['header'].attrs['length']):
                next(ascii_file)    

            next(ascii_file)
            category_length = len(f['header/categories'])
            tree_element_index = 0
            tree_index = 0
            first_line = True

            #create first numpy container
            z = np.zeros((self.tree_space[tree_index],category_length))
            tree_element_index = 0

            for line in ascii_file:
                if(line[0]=='#'): #new tree
                    if(not first_line): #not first tree
                        forest[str(tree_ids[tree_index - 1])] = z #store last finished tree
                        f[str(tree_ids[tree_index - 1])] = z
                        #initialize numpy array with proper dimensions
                        # print z
                        # print 'tree index', tree_index
                        # print 'tree space', self.tree_space[tree_index]
                        z = np.zeros((self.tree_space[tree_index],category_length))
                        tree_element_index = 0
                        tree_index += 1
                    else:
                        # print 'tree index', tree_index
                        # print 'tree space', self.tree_space[tree_index]
                        # forest[str(tree_ids[tree_index])] = z #store last finished tree
                        tree_index += 1
                    first_line = False
                else: #read in next tree element
                    z[tree_element_index] = line.split()
                    tree_element_index += 1
            # print z
            forest[str(tree_ids[tree_index - 1])] = z
            f[str(tree_ids[tree_index - 1])] = z

        return forest
            
            
    def _uncompress_ascii(self):
        if self.fname[-3:]=='.gz':
            print("...uncompressing ASCII data")
            os.system("gunzip "+self.fname)
            self.fname = self.fname[:-3]
        else:
            pass
        return

a = RockstarReader('sample_with_categories.txt')
# print a.forest
