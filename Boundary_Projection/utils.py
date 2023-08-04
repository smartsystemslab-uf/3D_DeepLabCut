import pickle
import numpy as np
import h5py
import cv2
import pandas as pd
import dev.data_types as data_types
from dev.globals import *
from matplotlib.pyplot import get_cmap

from typing import Union


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


def find_expanded_bounding_box(current_body: Union[data_types.Person, data_types.Arm]):
    current_joints = np.asarray([[joint.x, joint.y] for joint in current_body.joint_list])
    lastEstimate = current_body.window.estimate()
    joint_movements = np.where(np.isnan(current_joints), lastEstimate, current_joints)
    # print('**************************** Current')
    # print(current_joints)
    # print('###################### Estimate')
    # print(lastEstimate)
    # print('**************************** Joints')
    # print(joint_movements)

    offset_x = np.max(joint_movements[:, 0])
    offset_y = np.max(joint_movements[:, 1])

    if offset_x > 0:
        current_body.bbox.right += offset_x
    else:
        current_body.bbox.left += offset_x

    if offset_y > 0:
        current_body.bbox.bot -= offset_y
    else:
        current_body.bbox.top += offset_y


    current_body.bbox.clean()
    return current_body


def update_body_with_expanded_bb(body):
    # make bounding box fit around actor
    for joint in body.joint_list:
        body.bbox = expand_bounds_by_joint(body.bbox, joint)

    body = find_expanded_bounding_box(body)

    return body

def main(file_prefix):
    filename = 'dev/h5_data/' + file_prefix + '_el.h5'
    frames = []

    vid = cv2.VideoCapture('deeplabcut_project/cobot_test-achil-2023-06-07/videos/output_cam2.avi')

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
        Arm = data_types.Arm('Arm0')
        Person = data_types.Person('Person0')
        for index in indeces:
            data = dataset[index]
            frame = data_types.Frame()
            frame.arms.append(Arm)
            frame.persons.append(Person)
            ret, img = vid.read()

            for arm in frame.arms:
                available_keys = list(arm.h5_lookup.keys())
                for joint in arm.joint_list:
                    for lookup_name in available_keys:
                        if joint.name in lookup_name:
                            if 'X' in lookup_name:
                                joint.x = data[arm.h5_lookup[lookup_name]]
                            elif 'Y' in lookup_name:
                                joint.y = data[arm.h5_lookup[lookup_name]]

                arm = update_body_with_expanded_bb(arm)
                for joint in arm.joint_list:
                    try:
                        img = cv2.circle(img, (int(joint.x), int(joint.y)), 7, (0, 0, 0))
                    except ValueError:
                        pass
                for x, y in arm.window.estimate():
                    try:
                        img = cv2.circle(img, (int(x), int(y)), 7, (150, 150, 0))
                    except ValueError:
                        pass
                joint_values = np.asarray([[joint.x, joint.y] for joint in arm.joint_list])
                bodyJointEstimate = arm.window.estimate()

                updates = bodyJointEstimate
                updates = np.where(np.isnan(joint_values), updates, joint_values)
                arm.window.update(updates)

                cv2.imshow('temp', img)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            if index > 0:
                prevFrame = frames[index - 1]

                frame.prevFrame = prevFrame
                prevFrame.nextFrame = frame
                frame.currentFrameNum = index


            frames.append(frame)

    return frames




'''
BB_for_frame[resulting_BB.name] = resulting_BB

    current_BB_Arm.clean()
    BB_for_frame[current_BB_Arm.name + '_original'] = current_BB_Arm
    BB_for_frame[current_BB_Arm.name + '_original'].name = current_BB_Arm.name + '_original'
    joint_values = np.asarray([[joint.x, joint.y] for joint in arm.joint_list])
    updates = np.where(np.isnan(joint_values), lastEstimateArm, joint_values)
    arm.window.update(updates)'''





# def process_frames(frames):
#     BB_by_frames = []
#     found_arms = []
#     found_persons = []
#     for frame in frames:
#         prevFrame = frame.prevFrame
#         BB_for_frame = {}
#         for arm in frame.arms:
#             # get bounding box for actor
#
#
#         for person in frame.persons:
#             # get bounding box for actor
#             current_BB_Person = person.bbox
#             lastEstimatePerson = person.window.estimate()
#             # make bounding box fit around actor
#             for joint in person.joint_list:
#                 current_BB_Person = expand_bounds_by_joint(current_BB_Person, joint)
#
#             if prevFrame is None:
#                 current_BB_Person.clean()
#                 BB_for_frame[current_BB_Person.name + '_original'] = current_BB_Person
#                 BB_for_frame[current_BB_Person.name + '_original'].name = current_BB_Person.name + '_original'
#                 BB_for_frame[current_BB_Person.name] = current_BB_Person
#                 print('no prevFrame')
#             elif person.name not in [temp_person.name for temp_person in prevFrame.persons]:
#                 current_BB_Person.clean()
#                 BB_for_frame[current_BB_Person.name + '_original'] = current_BB_Person
#                 BB_for_frame[current_BB_Person.name + '_original'].name = current_BB_Person.name + '_original'
#                 BB_for_frame[current_BB_Person.name] = current_BB_Person
#                 print('no match in person')
#             else:
#                 for temp_person in prevFrame.persons:
#                     if temp_person.name == person.name:
#                         prevPerson = temp_person
#                         break
#
#                 resulting_BB = find_expanded_bounding_box(person, prevPerson, lastEstimatePerson)
#                 BB_for_frame[resulting_BB.name] = resulting_BB
#
#             current_BB_Person.clean()
#             BB_for_frame[current_BB_Person.name+'_original'] = current_BB_Person
#             BB_for_frame[current_BB_Person.name + '_original'].name = current_BB_Person.name + '_original'
#             joint_values = np.asarray([[joint.x, joint.y] for joint in person.joint_list])
#             updates = np.where(np.isnan(joint_values), lastEstimatePerson, joint_values)
#             person.window.update(updates)
#
#         BB_by_frames.append(BB_for_frame)
#
#     return BB_by_frames


def draw_bb_on_frame(img, bb, color):
    # if 'orig' in bb.name:
    #     return img
    top, bot, left, right = bb.as_array()
    img = cv2.rectangle(img, (left, top), (right, bot), color, 3)
    return img


# def main(args):
#     frames = read_h5(args)
#     BBs_by_frames = process_frames(frames)
#
#     vid = cv2.VideoCapture('deeplabcut_project/cobot_test-achil-2023-06-07/videos/output_cam2.avi')
#
#     max_bb = max([len(temp) for temp in BBs_by_frames])
#     cmap = get_cmap('viridis', max_bb)
#     colors = cmap.colors[:, :3] * 255
#
#     frame_count = 0
#     while True:
#         ret, img = vid.read()
#         if ret is not True:
#             break
#
#         bbs = BBs_by_frames[frame_count]
#         frame = frames[frame_count]
#
#         for i, bb in enumerate(bbs):
#             draw_bb_on_frame(img, bbs[bb], colors[i])
#
#         for arm in frame.arms:
#             for joint in arm.joint_list:
#                 print(joint)
#                 try:
#                     img = cv2.circle(img, (int(joint.x), int(joint.y)), 5, (0, 0, 0))
#                 except ValueError:
#                     pass
#
#         for person in frame.persons:
#             for joint in person.joint_list:
#                 try:
#                     img = cv2.circle(img, (int(joint.x), int(joint.y)), 5, (150, 150, 150))
#                 except ValueError:
#                     pass
#
#         frame_count += 1
#         cv2.imshow('temp', img)
#         if cv2.waitKey(30) & 0xFF == ord('q'):
#             break
#     cv2.destroyAllWindows()




if __name__ == "__main__":
    test_path = 'output_cam2DLC_dlcrnetms5_uf_cobotsJun7shuffle1_100000'
    main(test_path)
    