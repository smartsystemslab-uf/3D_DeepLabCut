import numpy as np
import pickle as pkl
import cv2
import h5py
import os
import dev.data_types as data_types

from typing import Union
from matplotlib.pyplot import get_cmap

from utils import MS_PER_FRAME, add_bodies_to_frame, vid_lookup

def populate_frames(file_prefix: Union[str, os.PathLike], num_body_types: int = 2):
    filename = 'dev/h5_data/' + file_prefix + '_el.h5'
    frames = []

    vid_name = vid_lookup[file_prefix+ '_el.h5']

    vid = cv2.VideoCapture(vid_name)

    dataset = h5py.File(filename, "r")

    for track in dataset.keys():
        table = dataset[track]['table']
        attrs_in_order = table.attrs.get('values_block_0_kind').decode('ascii')
        attrs_in_order = eval(attrs_in_order)

        arms = []
        persons = []
        name_lookups = {}
        for column_num, (model_name, body_name, joint_name, loc) in enumerate(attrs_in_order):
            if body_name not in [temp_arm.name for temp_arm in arms] and 'arm' in body_name:
                arms.append(data_types.Arm(body_name))
            elif body_name not in [temp_person.name for temp_person in persons] and 'person' in body_name:
                persons.append(data_types.Person(body_name))

            lookup = '_'.join([body_name, joint_name.upper(), loc.upper()])
            name_lookups[lookup] = column_num

        all_colors = get_cmap('viridis', num_body_types*3).colors
        arm_colors = all_colors[:3, :-1] * 255
        person_colors = all_colors[3:, :-1] * 255

        for frame_num, entry in table:
            frame = data_types.Frame()
            frame.arms = arms
            frame.persons = persons
            ret, img = vid.read()

            img = add_bodies_to_frame(frame.arms, img, name_lookups, entry, arm_colors)

            img = add_bodies_to_frame(frame.persons, img, name_lookups, entry, person_colors)

            cv2.imshow('temp', img)

            key = cv2.waitKey(MS_PER_FRAME)
            if key:
                if key & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
                elif key & 0xFF == ord('s'):
                    cv2.imwrite('saved_frame.jpg', img)
                    cv2.destroyAllWindows()
                    break

            if frame_num > 0:
                prevFrame = frames[frame_num - 1]

                frame.prevFrame = prevFrame
                prevFrame.nextFrame = frame
                frame.currentFrameNum = frame_num


            frames.append(frame)
    dataset.close()
    return frames

if __name__ == "__main__":
    test_path = 'output_cam2DLC_dlcrnetms5_uf_cobotsJun7shuffle1_100000'
    populate_frames(test_path)