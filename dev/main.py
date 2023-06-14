import pandas as pd
import h5py

def read_pickles(file_prefix):
    dict_assemblies = pd.read_pickle('pickle_data/'+ file_prefix +'_assemblies.pickle')
    dict_full       = pd.read_pickle('pickle_data/'+ file_prefix +'_full.pickle')
    dict_el         = pd.read_pickle('pickle_data/'+ file_prefix +'_el.pickle')
    dict_meta       = pd.read_pickle('pickle_data/'+ file_prefix +'_meta.pickle')

def read_h5(file_prefix):
    filename = 'h5_data/' + file_prefix + '_el.h5'
    with h5py.File(filename, "r") as f:
        # Print all root level object names (aka keys)
        # these can be group or dataset names
        #print("Keys: %s" % f.keys())
        # get first object name/key; may or may NOT be a group
        a_group_key = list(f.keys())[0]

        # get the object type for a_group_key: usually group or dataset
        #print(type(f[a_group_key]))

        # If a_group_key is a group name,
        # this gets the object names in the group and returns as a list
        dataset = f[a_group_key]['table']['values_block_0']

        pass
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_prefix = 'output_cam2DLC_dlcrnetms5_uf_cobotsJun7shuffle1_100000'
    #read_pickles(file_prefix)
    read_h5(file_prefix)
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
