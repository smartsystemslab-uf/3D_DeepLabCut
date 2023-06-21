import pandas as pd
import h5py
import data_types as dt

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
        indeces = list(f[a_group_key]['table']['index'])
        frames = []
        for index in indeces:
            data = dataset[index]
            frame = dt.Frame()

            frame.arm.base.x = data[frame.arm.H5_BASE_LOC_X]
            frame.arm.base.y = data[frame.arm.H5_BASE_LOC_Y]

            frame.arm.joint1.x = data[frame.arm.H5_JOINT1_LOC_X]
            frame.arm.joint1.y = data[frame.arm.H5_JOINT1_LOC_Y]

            frame.arm.joint2.x = data[frame.arm.H5_JOINT2_LOC_X]
            frame.arm.joint2.y = data[frame.arm.H5_JOINT2_LOC_Y]

            frame.arm.joint3.x = data[frame.arm.H5_JOINT3_LOC_X]
            frame.arm.joint3.y = data[frame.arm.H5_JOINT3_LOC_Y]

            frame.arm.joint4.x = data[frame.arm.H5_JOINT4_LOC_X]
            frame.arm.joint4.y = data[frame.arm.H5_JOINT4_LOC_Y]

            frame.arm.finger1.x = data[frame.arm.H5_FINGER1_LOC_X]
            frame.arm.finger1.y = data[frame.arm.H5_FINGER1_LOC_Y]

            frame.arm.finger2.x = data[frame.arm.H5_FINGER2_LOC_X]
            frame.arm.finger2.y = data[frame.arm.H5_FINGER2_LOC_Y]

            frame.person.head.x = data[frame.person.H5_HEAD_LOC_X]
            frame.person.head.y = data[frame.person.H5_HEAD_LOC_Y]

            frame.person.chest.x = data[frame.person.H5_CHEST_LOC_X]
            frame.person.chest.y = data[frame.person.H5_CHEST_LOC_Y]

            frame.person.shoulder_l.x = data[frame.person.H5_SHOULDER_L_LOC_X]
            frame.person.shoulder_l.y = data[frame.person.H5_SHOULDER_L_LOC_Y]

            frame.person.shoulder_r.x = data[frame.person.H5_SHOULDER_R_LOC_X]
            frame.person.shoulder_r.y = data[frame.person.H5_SHOULDER_R_LOC_Y]

            frame.person.elbow_l.x = data[frame.person.H5_ELBOW_L_LOC_X]
            frame.person.elbow_l.y = data[frame.person.H5_ELBOW_L_LOC_Y]

            frame.person.elbow_r.x = data[frame.person.H5_ELBOW_R_LOC_X]
            frame.person.elbow_r.y = data[frame.person.H5_ELBOW_R_LOC_Y]

            frame.person.wrist_l.x = data[frame.person.H5_WRIST_L_LOC_X]
            frame.person.wrist_l.y = data[frame.person.H5_WRIST_L_LOC_Y]

            frame.person.wrist_r.x = data[frame.person.H5_WRIST_R_LOC_X]
            frame.person.wrist_r.y = data[frame.person.H5_WRIST_R_LOC_Y]

            frame.person.pelvis.x = data[frame.person.H5_PELVIS_LOC_X]
            frame.person.pelvis.y = data[frame.person.H5_PELVIS_LOC_Y]

            frame.person.hip_l.x = data[frame.person.H5_HIP_L_LOC_X]
            frame.person.hip_l.y = data[frame.person.H5_HIP_L_LOC_Y]

            frame.person.hip_r.x = data[frame.person.H5_HIP_R_LOC_X]
            frame.person.hip_r.y = data[frame.person.H5_HIP_R_LOC_Y]

            if 'cam2' in file_prefix:
                frame.person.ankle_l.x = data[frame.person.H5_ANKLE_L_2_LOC_X]
                frame.person.ankle_l.y = data[frame.person.H5_ANKLE_L_2_LOC_Y]

                frame.person.ankle_r.x = data[frame.person.H5_ANKLE_R_2_LOC_X]
                frame.person.ankle_r.y = data[frame.person.H5_ANKLE_R_2_LOC_Y]
            else:
                frame.person.ankle_l.x = data[frame.person.H5_ANKLE_L_LOC_X]
                frame.person.ankle_l.y = data[frame.person.H5_ANKLE_L_LOC_Y]

                frame.person.ankle_r.x = data[frame.person.H5_ANKLE_R_LOC_X]
                frame.person.ankle_r.y = data[frame.person.H5_ANKLE_R_LOC_Y]

            if index > 0:
                prevFrame = frames[index-1]
                frame.prevFrame = prevFrame
                prevFrame.nextFrame = frame

            frames.append(frame)
        pass

if __name__ == '__main__':
    file_prefix = 'output_cam1DLC_resnet50_uf_cobots_multicamJun12shuffle1_50000'

    #read_pickles(file_prefix)
    read_h5(file_prefix)
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
