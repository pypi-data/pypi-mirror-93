"""Common functions for PyMINEr"""
import pickle
import os
import numpy as np
from scipy.sparse import csc_matrix, lil_matrix
import networkx as nx
import community
import time
import shutil
import h5py
from subprocess import check_call, Popen, PIPE


def cp(file1,file2 = None):
    if file2 is None:
        ## check if a single string was given in, separated by a space
        temp_f_list = file1.split(" ")
        if len(temp_f_list)==2:
            file1 = temp_f_list[0]
            file2 = temp_f_list[1]
        else:
            print("\n\nsomething wrong with the cp syntax!\n\n")
            print("don't know how to interpret:",file1)
            sys.exit()
    with open(file1, 'rb') as f_in:
        with open(file2, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return()


def rm(rm_file):
    if os.path.isfile(rm_file):
        os.remove(rm_file)
    else:
        print('WARNING:',rm_file,"doesn't exist, couldn't remove it")
    return()


def process_dir(in_dir):
	## process the output dir
	if in_dir[-1]!='/':
		in_dir+='/'
	if not os.path.isdir(in_dir):
		os.makedirs(in_dir)
	return(in_dir)


def run_cmd(in_message, com=True, stdout=None):
    if type(in_message)==str:
        print(in_message)
    elif type(in_message)==list:
        print('\n', " ".join(in_message), '\n')
    else:
        sys.exit("not sure how to parse this for command line run:\n",in_message)
    if stdout:
        with open(stdout, 'w') as out:
            process = Popen(in_message, stdout=PIPE)
            while True:
                line = process.stdout.readline().decode("utf-8")
                out.write(line)
                if line == '' and process.poll() is not None:
                    break
    if com:
        Popen(in_message).communicate()
    else:
        check_call(in_message)


def cmd(in_message, com=True):
    print(in_message)
    time.sleep(.25)
    if com:
        Popen(in_message,shell=True).communicate()
    else:
        Popen(in_message,shell=True)



def read_file(temp_file, lines_o_raw='lines', quiet=False):
    """ basic function library """
    lines = None
    if not quiet:
        print('reading', temp_file)
    file_handle = open(temp_file, 'r')
    if lines_o_raw == 'lines':
        lines = file_handle.readlines()
        for i, line in enumerate(lines):
            lines[i] = line.strip('\n')
    elif lines_o_raw == 'raw':
        lines = file_handle.read()
    file_handle.close()
    return lines


def make_file(contents, path):
    file_handle = open(path, 'w')
    if isinstance(contents, list):
        file_handle.writelines(contents)
    elif isinstance(contents, str):
        file_handle.write(contents)
    file_handle.close()


# def flatten_2D_table(table, delim):
#     # print(type(table))
#     if str(type(table)) == "<class 'numpy.ndarray'>":
#         out = []
#         for i, row in enumerate(table):
#             out.append([])
#             for j, cell in enumerate(row):
#                 try:
#                     str(cell)
#                 except ValueError:
#                     print(cell)
#                 else:
#                     out[i].append(str(cell))
#             out[i] = delim.join(out[i]) + '\n'
#         return out
#     else:
#         for i, row in enumerate(table):
#             for j, cell in enumerate(row):
#                 try:
#                     str(row)
#                 except ValueError:
#                     print(row)
#                 else:
#                     table[i][j] = str(cell)
#             table[i] = delim.join(row) + '\n'
#         return table

def flatten_2D_table(table, delim):
    # print(type(table))
    if str(type(table)) == "<class 'numpy.ndarray'>":
        out = []
        for i in range(0, len(table)):
            out.append([])
            for j in range(0, len(table[i])):
                try:
                    str(table[i][j])
                except:
                    print(table[i][j])
                else:
                    out[i].append(str(table[i][j]))
            out[i] = delim.join(out[i]) + '\n'
        return out
    else:
        for i in range(0, len(table)):
            for j in range(0, len(table[i])):
                try:
                    str(table[i][j])
                except:
                    print(table[i][j])
                else:
                    table[i][j] = str(table[i][j])
            table[i] = delim.join(table[i]) + '\n'
        # print(table[0])
        return table


def strip_split(line, delim='\t'):
    return line.strip('\n').split(delim)


def make_table(lines, delim, range_min=0, num_convert = float):
    for i in range(range_min, len(lines)):
        lines[i] = lines[i].strip()
        lines[i] = lines[i].split(delim)
        for j in range(range_min, len(lines[i])):
            if i!=0 or j!=0:
                try:
                    float(lines[i][j])
                except ValueError:
                    lines[i][j] = lines[i][j].replace('"', '')
                else:
                    lines[i][j] = num_convert(lines[i][j])
    return lines


def get_file_path(in_path):
    return os.path.dirname(in_path)+os.sep


def read_table(file, sep='\t', num_convert = float):
    return make_table(read_file(file, 'lines'), sep, num_convert = num_convert)


def write_table(table, out_file, sep='\t'):
    make_file(flatten_2D_table(table, sep), out_file)


def import_dict(file_handle):
    file_handle = open(file_handle, 'rb')
    data = pickle.load(file_handle)
    file_handle.close()
    return data


def save_dict(data, path):
    file_handle = open(path, 'wb')
    pickle.dump(data, file_handle)
    file_handle.close()


def check_infile(infile):
    if os.path.isfile(infile):
        return
    else:
        sys.exit(str('could not find '+infile))

def outfile_exists(outfile):
    if os.path.isfile(outfile):
        statinfo = os.stat(outfile)
        if statinfo.st_size!=0:
            return(True)
        else:
            return(False)
    else:
        return(False)




# def get_sample_k_lists(group_numeric_vector, total_groups = None):
#     if total_groups == None:
#         total_groups = max(group_numeric_vector)+1
#     print(total_groups)
#     group_index_lists = [[] for i in range(total_groups)]
#     for i in range(0,len(group_numeric_vector)):
#         temp_group = group_numeric_vector[i]
#         group_index_lists[temp_group].append(i)
#     print("\n\ngroup_index_lists")
#     print(group_index_lists)
#     return(group_index_lists)


def get_sample_k_lists(group_numeric_vector, total_groups = None):
    temp_group_numeric_vector = []
    for num in group_numeric_vector:
        try:
            temp_group_numeric_vector.append(int(num))
        except:
            temp_group_numeric_vector.append(num)
    group_numeric_vector = temp_group_numeric_vector
    if total_groups == None:
        all_vect = list(set(group_numeric_vector))
        numeric_vect = []
        for entry in all_vect:
            #print(type(entry),entry)
            if type(entry)==int:
                numeric_vect.append(entry)
        total_groups = max([len(numeric_vect),max(numeric_vect)+1])
    # print(total_groups)
    group_index_lists = [[] for i in range(total_groups)]
    for i in range(0,len(group_numeric_vector)):
        if type(group_numeric_vector[i]) ==  int or type(group_numeric_vector[i]) == float:

            temp_group = group_numeric_vector[i]
            group_index_lists[temp_group].append(i)
    # print("\n\ngroup_index_lists\n\n")
    # print(group_index_lists)
    return(group_index_lists)


def convert_vect_to_mi_bins(in_vect):
    out_vect = np.array(in_vect, dtype = str)
    ## first get all the unique values
    all_vals = list(set(list(in_vect)))
    ## next get all the numeric convertable values
    ## or return the original vect if there are none
    all_num_vals = []
    all_num_idxs=[]
    for i in range(len(in_vect)):
        try:
            float(in_vect[i])
        except:
            pass
        else:
            temp_val = float(in_vect[i])
            if not np.isnan(temp_val):
                all_num_vals.append(temp_val)
                all_num_idxs.append(i)
    ## if there aren't enough numeric values to warrant conversion, then don't
    if len(all_num_vals) < 10:
        return in_vect
    ## calculate the number of bins
    bin_num = max([2,int(np.sqrt(len(all_num_vals)/5))])
    ## min-max linear normalize the vector
    all_num_vals = np.array(all_num_vals)
    all_num_vals -= np.min(all_num_vals)
    all_num_vals = all_num_vals / np.max(all_num_vals)
    ## calculate the bin interval
    bins = np.arange(bin_num)/bin_num
    digitized_num_vals = np.digitize(all_num_vals, bins)
    print(digitized_num_vals)
    ## now update the original vector to return it
    for i in range(0,len(all_num_idxs)):
        original_idx = all_num_idxs[i]
        new_val = digitized_num_vals[i]
        out_vect[original_idx] = str(new_val)
    return out_vect


def digitize_for_max_info(in_mat):
    ## takes in a full input matrix & digitizes the numeric values of the colums
    in_mat = np.array(in_mat,dtype=str)
    ncol = np.shape(in_mat)[1]
    nrow = np.shape(in_mat)[0]
    for i in range(1,ncol):
        in_mat[1:nrow,i] = convert_vect_to_mi_bins(in_mat[1:nrow,i])
    return in_mat


## this function was adopted from emre's stackoverflow answer found here:
## https://stackoverflow.com/questions/7450957/how-to-implement-rs-p-adjust-in-python
def correct_pvalues_for_multiple_testing(pvalues, correction_type = "Benjamini-Hochberg"):                
    """                                                                                                   
    consistent with R - print correct_pvalues_for_multiple_testing([0.0, 0.01, 0.029, 0.03, 0.031, 0.05, 0.069, 0.07, 0.071, 0.09, 0.1]) 
    """
    from numpy import array, empty
    pvalues = array(pvalues)

    ## convert to linear if needed
    #print(pvalues)
    if len(np.shape(pvalues)) > 1:
        needs_reshaping = True
        original_shape = np.shape(pvalues)
        new_shape = pvalues.size
        #print(new_shape)
        pvalues = pvalues.reshape((new_shape))
        #print(pvalues)
    else:
        needs_reshaping = False

    n = int(pvalues.shape[0])
    new_pvalues = empty(n)
    if correction_type == "Bonferroni":
        new_pvalues = n * pvalues
    elif correction_type == "Bonferroni-Holm":
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]
        values.sort()
        for rank, vals in enumerate(values):
            pvalue, i = vals
            new_pvalues[i] = (n-rank) * pvalue
    elif correction_type == "Benjamini-Hochberg":
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]
        values.sort()
        values.reverse()
        new_values = []
        for i, vals in enumerate(values):
            rank = n - i
            pvalue, index = vals
            new_values.append((n/rank) * pvalue)
        for i in range(0, int(n)-1):
            if new_values[i] < new_values[i+1]:
                new_values[i+1] = new_values[i]
        for i, vals in enumerate(values):
            pvalue, index = vals
            new_pvalues[index] = new_values[i]
    if needs_reshaping:
        #print('original_shape\n',pvalues.reshape((original_shape)))
        #print('new_pvalues\n',new_pvalues.reshape((original_shape)))
        new_pvalues = new_pvalues.reshape((original_shape))
    #print("new_pvalues\n",new_pvalues)
    return new_pvalues


def do_louvain_merger(in_mat, sample_k_lists, cutoff = 0):
    ## take in the BH corrected p-values for whether 
    ## the groups are significantly different for this ome
    ## at the level of the feature selected affinity matrix
    # actually cut the edges that need to be pruned (apparently setting the weights to 0 doesn't actually give it zero weight...?)
    cut_counter = 0
    for i in range(in_mat.shape[0]):
        for j in range(in_mat.shape[1]):
            if in_mat[i,j] < cutoff:
                in_mat[i,j] = 0
                cut_counter +=1
    print('cut',cut_counter,'low weight edges')
    ## make the fully connected, weighted matrix
    G = nx.from_numpy_matrix(in_mat)
    for node in G.nodes():
        print(node)
    for edge in G.edges():
        print(edge)
    partition = community.best_partition(G)
    ## this is a dictionary with the original group index as the keys
    ## and the new group index as the 
    print(partition)
    ## make the empty lists for holding all of the 
    ## new sample group lists
    new_groups = []
    new_group_annotations = []
    for i in range(len(set(partition.values()))):
        new_groups.append([])
        new_group_annotations.append([])
    for i in range(in_mat.shape[0]):
        new_groups[partition[i]]+=sample_k_lists[i]
        new_group_annotations[partition[i]].append(i)
    return(new_groups,new_group_annotations, partition)



def removeNonAscii(s):
    ## taken from: https://drumcoder.co.uk/blog/2012/jul/13/removing-non-ascii-chars-string-python/
    return "".join(i for i in s if ord(i)<128)


##################################################################
############### some ray specific functions ######################
def get_num_rows_from_dict_lists(dict_list):
    ## goes through all of the indices & returns the number of dims
    row_dims = 0
    for temp_dict in dict_list:
        for temp_key in list(temp_dict.keys()):
            #print(temp_key)
            if temp_key > row_dims:
                row_dims = temp_key
    return(row_dims+1)


def get_num_cols_from_dict_lists(dict_list):
    ## first get the dimentions
    first_key = list(dict_list[0].keys())[0]
    first = dict_list[0][first_key]
    if type(first) == list:
        col_dims = len(first)
    else:
        col_dims = 1
    return(col_dims)


def ray_dicts_to_array(dict_list, csc = False):
    row_dims = get_num_rows_from_dict_lists(dict_list)
    col_dims = get_num_cols_from_dict_lists(dict_list)
    if csc:
        out_array = np.zeros((row_dims, col_dims))
    else:
        out_array = csc_matrix((row_dims, col_dims))
    print(out_array)
    for temp_dict in dict_list:
        for idx, value in temp_dict.items():
            #print(idx)
            #print(value)
            out_array[idx] = value
    return(out_array)


def get_indices(threads, num_genes):
    indices_list = []
    for t in range(threads):
        indices_list.append([])
    temp_idx = 0
    while temp_idx < num_genes:
        for t in range(threads):
            if temp_idx < num_genes:
                indices_list[t].append(temp_idx)
                temp_idx += 1
    return(indices_list)


def ray_get_indices_from_list(threads, original_idx_list):
    indices_list = []
    for t in range(threads):
        indices_list.append([])
    temp_idx = 0
    while temp_idx < len(original_idx_list):
        for t in range(threads):
            if temp_idx < len(original_idx_list):
                indices_list[t].append(original_idx_list[temp_idx])
                temp_idx += 1
    return(indices_list)


def get_contiguous_indices(threads, num_genes):
    old_format_indices = get_indices(threads, num_genes)
    new_indices = []
    for t in range(threads):
        new_indices.append([])
    cur_idx=0
    for t in range(threads):
        while len(new_indices[t]) <= len(old_format_indices[t]) and cur_idx<num_genes:
            new_indices[t].append(cur_idx)
            cur_idx+=1
    return(new_indices)
##########################################################

def read_cz_h5(in_file, load_binary=False):
    h5f = h5py.File(in_file , 'r')
    if 'X' not in h5f:
        print("couldn't find the data in the cz h5 file")
    if 'shape' in dir(h5f['X']):
        in_mat= lil_matrix(h5f['X'])
    elif 'keys' in dir(h5f['X']):
        if ('data' in h5f['X']) and ('indices' in h5f['X'])  and ('indptr' in h5f['X']):
            if not load_binary:
                in_mat= csc_matrix((h5f['X']['data'], h5f['X']['indices'], h5f['X']['indptr']))
            else:
                data_vect=np.ones(h5f['X']['data'].shape)
                in_mat= csc_matrix((data_vect, h5f['X']['indices'], h5f['X']['indptr']))
    ## read the genes
    if "shape" in dir(h5f['var']):
        genes = [entry[0] for entry in h5f['var']]
    ## read the cells
    if "shape" in dir(h5f['obs']):
        cells = ['variable'] + [entry[0] for entry in h5f['obs']]
    h5f.close()
    return(in_mat, genes, cells)


def read_tsv(in_file):
    in_table = read_table(in_file)
    cells = in_table[0]
    genes = []
    in_mat_num = np.zeros((len(in_table)-1,len(cells)-1))
    for i in range(1,len(in_table)):
        genes.append(in_table[i,0])
        in_mat_num[i-1,:] = in_table[i,1:]
    return(in_mat_num, genes, cells)
