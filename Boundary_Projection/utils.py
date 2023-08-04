import pickle
import numpy as np
import h5py
import cv2
import pandas as pd
import dev.data_types as data_types
from dev.globals import *
from matplotlib.pyplot import get_cmap

from typing import Union

def read_h5(file_prefix):
    filename = 'dev/h5_data/' + file_prefix + '_el.h5'
    frames = []
    with h5py.File(filename, "r") as f:
        # Print all root level object names (aka keys)
        # these can be group or dataset names
        # print("Keys: %s" % f.keys())
        # get first object name/key; may or may NOT be a group
        a_group_key = list(f.keys())[0]

        # get the object type for a_group_key: usually group or dataset
        # print(type(f[a_group_key]))

        # If a_group_key is a group name,
        # this gets the object names in the group and returns as a list
        dataset = f[a_group_key]['table']['values_block_0']
        indeces = list(f[a_group_key]['table']['index'])
        for index in indeces:
            data = dataset[index]
            frame = data_types.Frame()
            frame.arms.append(data_types.Arm('Arm0'))
            frame.persons.append(data_types.Person('Person0'))

            frame.arms[0].base.x = data[frame.arms[0].H5_BASE_LOC_X]
            frame.arms[0].base.y = data[frame.arms[0].H5_BASE_LOC_Y]
            # frame.arms[0].joint_list.append(frame.arms[0].base)

            frame.arms[0].joint1.x = data[frame.arms[0].H5_JOINT1_LOC_X]
            frame.arms[0].joint1.y = data[frame.arms[0].H5_JOINT1_LOC_Y]
            # frame.arms[0].joint_list.append(frame.arms[0].joint1)

            frame.arms[0].joint2.x = data[frame.arms[0].H5_JOINT2_LOC_X]
            frame.arms[0].joint2.y = data[frame.arms[0].H5_JOINT2_LOC_Y]
            # frame.arms[0].joint_list.append(frame.arms[0].joint2)

            frame.arms[0].joint3.x = data[frame.arms[0].H5_JOINT3_LOC_X]
            frame.arms[0].joint3.y = data[frame.arms[0].H5_JOINT3_LOC_Y]
            # frame.arms[0].joint_list.append(frame.arms[0].joint3)

            frame.arms[0].joint4.x = data[frame.arms[0].H5_JOINT4_LOC_X]
            frame.arms[0].joint4.y = data[frame.arms[0].H5_JOINT4_LOC_Y]
            # frame.arms[0].joint_list.append(frame.arms[0].joint4)

            frame.arms[0].finger1.x = data[frame.arms[0].H5_FINGER1_LOC_X]
            frame.arms[0].finger1.y = data[frame.arms[0].H5_FINGER1_LOC_Y]
            # frame.arms[0].joint_list.append(frame.arms[0].finger1)

            frame.arms[0].finger2.x = data[frame.arms[0].H5_FINGER2_LOC_X]
            frame.arms[0].finger2.y = data[frame.arms[0].H5_FINGER2_LOC_Y]
            # frame.arms[0].joint_list.append(frame.arms[0].finger2)

            frame.persons[0].head.x = data[frame.persons[0].H5_HEAD_LOC_X]
            frame.persons[0].head.y = data[frame.persons[0].H5_HEAD_LOC_Y]
            # frame.persons[0].joint_list.append(frame.persons[0].head)

            frame.persons[0].chest.x = data[frame.persons[0].H5_CHEST_LOC_X]
            frame.persons[0].chest.y = data[frame.persons[0].H5_CHEST_LOC_Y]
            # frame.persons[0].joint_list.append(frame.persons[0].chest)

            frame.persons[0].shoulder_l.x = data[frame.persons[0].H5_SHOULDER_L_LOC_X]
            frame.persons[0].shoulder_l.y = data[frame.persons[0].H5_SHOULDER_L_LOC_Y]
            # frame.persons[0].joint_list.append(frame.persons[0].shoulder_l)

            frame.persons[0].shoulder_r.x = data[frame.persons[0].H5_SHOULDER_R_LOC_X]
            frame.persons[0].shoulder_r.y = data[frame.persons[0].H5_SHOULDER_R_LOC_Y]
            # frame.persons[0].joint_list.append(frame.persons[0].shoulder_r)

            frame.persons[0].elbow_l.x = data[frame.persons[0].H5_ELBOW_L_LOC_X]
            frame.persons[0].elbow_l.y = data[frame.persons[0].H5_ELBOW_L_LOC_Y]
            # frame.persons[0].joint_list.append(frame.persons[0].elbow_l)

            frame.persons[0].elbow_r.x = data[frame.persons[0].H5_ELBOW_R_LOC_X]
            frame.persons[0].elbow_r.y = data[frame.persons[0].H5_ELBOW_R_LOC_Y]
            # frame.persons[0].joint_list.append(frame.persons[0].elbow_r)

            frame.persons[0].wrist_l.x = data[frame.persons[0].H5_WRIST_L_LOC_X]
            frame.persons[0].wrist_l.y = data[frame.persons[0].H5_WRIST_L_LOC_Y]
            # frame.persons[0].joint_list.append(frame.persons[0].wrist_l)

            frame.persons[0].wrist_r.x = data[frame.persons[0].H5_WRIST_R_LOC_X]
            frame.persons[0].wrist_r.y = data[frame.persons[0].H5_WRIST_R_LOC_Y]
            # frame.persons[0].joint_list.append(frame.persons[0].wrist_r)

            frame.persons[0].pelvis.x = data[frame.persons[0].H5_PELVIS_LOC_X]
            frame.persons[0].pelvis.y = data[frame.persons[0].H5_PELVIS_LOC_Y]
            # frame.persons[0].joint_list.append(frame.persons[0].pelvis)

            frame.persons[0].hip_l.x = data[frame.persons[0].H5_HIP_L_LOC_X]
            frame.persons[0].hip_l.y = data[frame.persons[0].H5_HIP_L_LOC_Y]
            # frame.persons[0].joint_list.append(frame.persons[0].hip_l)

            frame.persons[0].hip_r.x = data[frame.persons[0].H5_HIP_R_LOC_X]
            frame.persons[0].hip_r.y = data[frame.persons[0].H5_HIP_R_LOC_Y]
            # frame.persons[0].joint_list.append(frame.persons[0].hip_r)

            if 'cam2' in file_prefix:
                frame.persons[0].ankle_l.x = data[frame.persons[0].H5_ANKLE_L_2_LOC_X]
                frame.persons[0].ankle_l.y = data[frame.persons[0].H5_ANKLE_L_2_LOC_Y]
                # frame.persons[0].joint_list.append(frame.persons[0].ankle_l)

                frame.persons[0].ankle_r.x = data[frame.persons[0].H5_ANKLE_R_2_LOC_X]
                frame.persons[0].ankle_r.y = data[frame.persons[0].H5_ANKLE_R_2_LOC_Y]
                # frame.persons[0].joint_list.append(frame.persons[0].ankle_r)
            else:
                frame.persons[0].ankle_l.x = data[frame.persons[0].H5_ANKLE_L_LOC_X]
                frame.persons[0].ankle_l.y = data[frame.persons[0].H5_ANKLE_L_LOC_Y]
                # frame.persons[0].joint_list.append(frame.persons[0].ankle_l)

                frame.persons[0].ankle_r.x = data[frame.persons[0].H5_ANKLE_R_LOC_X]
                frame.persons[0].ankle_r.y = data[frame.persons[0].H5_ANKLE_R_LOC_Y]
                # frame.persons[0].joint_list.append(frame.persons[0].ankle_r)
            if index > 0:
                prevFrame = frames[index - 1]
                frame.prevFrame = prevFrame
                prevFrame.nextFrame = frame
                frame.currentFrameNum = index

            frames.append(frame)
    return frames


def expand_bounds_by_joint(current_bounds, new_joint):
    # check bounds vs current bounding box, expand all
    if new_joint.x < current_bounds.left:
        current_bounds.left = new_joint.x
    if new_joint.x > current_bounds.right:
        current_bounds.right = new_joint.x

    if new_joint.y < current_bounds.top:
        current_bounds.top = new_joint.y
    if new_joint.y > current_bounds.bot:
        current_bounds.bot = new_joint.y

    return current_bounds


def find_expanded_bounding_box(current_body: Union[data_types.Person, data_types.Arm],
                               prev_body: Union[data_types.Person, data_types.Arm], window:data_types.MovingWindow):
    current_body_BB = current_body.bbox
    last_body_BB = prev_body.bbox
    current_BB_area = abs(current_body_BB.width() * last_body_BB.height())
    diff_in_BB = current_body_BB.as_array() - last_body_BB.as_array()
    diff_in_BB = data_types.BoundingBox(current_body_BB.name, diff_in_BB)
    change_in_x = diff_in_BB.width()
    change_in_y = diff_in_BB.height()
    change_in_area = abs(change_in_x * change_in_y)

    overall_scale = 0.2 + (change_in_area / (current_BB_area+1))

    resulting_BB = data_types.BoundingBox(current_body_BB.name, current_body_BB)
    resulting_BB.scale_by(overall_scale)

    offset_x = change_in_x / current_body_BB.width()
    offset_y = change_in_y / current_body_BB.height()

    if offset_x > 0:
        resulting_BB.right += offset_x
    else:
        resulting_BB.left += offset_x

    if offset_y > 0:
        resulting_BB.bot -= offset_y
    else:
        resulting_BB.top += offset_y

    num_joints = len(current_body.joint_list)
    joint_diffs = [current_body.joint_list[i].calc_diff(prev_body.joint_list[i]) for i in range(num_joints)]
    joint_diffs = np.vstack(joint_diffs)
    joint_diffs[np.isnan(joint_diffs)] = 0

    joint_dists = np.sum(joint_diffs**2, axis=1)
    fastest_joint = joint_dists.argmax()
    fastest_joint_vel = joint_diffs[fastest_joint]
    window.update(fastest_joint_vel)
    vel_scale = window.calc()

    if vel_scale[0] > 0:
        resulting_BB.right += vel_scale[0]
    else:
        resulting_BB.left += vel_scale[0]

    if vel_scale[1] > 0:
        resulting_BB.bot += vel_scale[1]
    else:
        resulting_BB.top += vel_scale[1]

    resulting_BB.clean()
    return resulting_BB


def process_frames(frames):
    BB_by_frames = []
    window = data_types.MovingWindow(size=5, weights=(1, 1/2, 1/4, 1/8, 1/16))
    for frame in frames:
        prevFrame = frame.prevFrame
        BB_for_frame = {}
        for arm in frame.arms:
            # get bounding box for actor
            current_BB_Arm = arm.bbox
            # make bounding box fit around actor
            for joint in arm.joint_list:
                current_BB_Arm = expand_bounds_by_joint(current_BB_Arm, joint)

            if prevFrame is None:
                current_BB_Arm.clean()
                BB_for_frame[current_BB_Arm.name + '_original'] = current_BB_Arm
                BB_for_frame[current_BB_Arm.name + '_original'].name = current_BB_Arm.name + '_original'
                BB_for_frame[current_BB_Arm.name] = current_BB_Arm
                print('no prevFrame')
                continue
            elif arm.name not in [temp_arm.name for temp_arm in prevFrame.arms]:
                current_BB_Arm.clean()
                BB_for_frame[current_BB_Arm.name + '_original'] = current_BB_Arm
                BB_for_frame[current_BB_Arm.name + '_original'].name = current_BB_Arm.name + '_original'
                BB_for_frame[current_BB_Arm.name] = current_BB_Arm
                print('no match in arm')
                continue
            else:
                for temp_arm in prevFrame.arms:
                    if temp_arm.name == arm.name:
                        prevArm = temp_arm
                        break

            resulting_BB = find_expanded_bounding_box(arm, prevArm, window)
            BB_for_frame[resulting_BB.name] = resulting_BB

            current_BB_Arm.clean()
            BB_for_frame[current_BB_Arm.name + '_original'] = current_BB_Arm
            BB_for_frame[current_BB_Arm.name + '_original'].name = current_BB_Arm.name + '_original'

        for person in frame.persons:
            # get bounding box for actor
            current_BB_Person = person.bbox
            # make bounding box fit around actor
            for joint in person.joint_list:
                current_BB_Person = expand_bounds_by_joint(current_BB_Person, joint)

            if prevFrame is None:
                current_BB_Person.clean()
                BB_for_frame[current_BB_Person.name + '_original'] = current_BB_Person
                BB_for_frame[current_BB_Person.name + '_original'].name = current_BB_Person.name + '_original'
                BB_for_frame[current_BB_Person.name] = current_BB_Person
                print('no prevFrame')
                continue
            elif person.name not in [temp_person.name for temp_person in prevFrame.persons]:
                current_BB_Person.clean()
                BB_for_frame[current_BB_Person.name + '_original'] = current_BB_Person
                BB_for_frame[current_BB_Person.name + '_original'].name = current_BB_Person.name + '_original'
                BB_for_frame[current_BB_Person.name] = current_BB_Person
                print('no match in person')
                continue
            else:
                for temp_person in prevFrame.persons:
                    if temp_person.name == person.name:
                        prevPerson = temp_person
                        break

            resulting_BB = find_expanded_bounding_box(person, prevPerson, window)
            BB_for_frame[resulting_BB.name] = resulting_BB

            current_BB_Person.clean()
            BB_for_frame[current_BB_Person.name+'_original'] = current_BB_Person
            BB_for_frame[current_BB_Person.name + '_original'].name = current_BB_Person.name + '_original'

        BB_by_frames.append(BB_for_frame)

    return BB_by_frames


def draw_bb_on_frame(img, bb, color):
    # if 'orig' in bb.name:
    #     return img
    top, bot, left, right = bb.as_array()
    img = cv2.rectangle(img, (left, top), (right, bot), color, 3)
    return img


def main(args):
    frames = read_h5(args)
    BBs_by_frames = process_frames(frames)

    vid = cv2.VideoCapture('deeplabcut_project/cobot_test-achil-2023-06-07/videos/output_cam2.avi')

    max_bb = max([len(temp) for temp in BBs_by_frames])
    cmap = get_cmap('viridis', max_bb)
    colors = cmap.colors[:, :3] * 255

    frame_count = 0
    while True:
        ret, img = vid.read()
        if ret is not True:
            break

        bbs = BBs_by_frames[frame_count]
        frame = frames[frame_count]

        for i, bb in enumerate(bbs):
            draw_bb_on_frame(img, bbs[bb], colors[i])

        for arm in frame.arms:
            for joint in arm.joint_list:
                try:
                    img = cv2.circle(img, (int(joint.x), int(joint.y)), 5, (0, 0, 0))
                except ValueError:
                    pass

        for person in frame.persons:
            for joint in person.joint_list:
                try:
                    img = cv2.circle(img, (int(joint.x), int(joint.y)), 5, (150, 150, 150))
                except ValueError:
                    pass

        frame_count += 1
        cv2.imshow('temp', img)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()




if __name__ == "__main__":
    test_path = 'output_cam2DLC_dlcrnetms5_uf_cobotsJun7shuffle1_100000'
    main(test_path)
    