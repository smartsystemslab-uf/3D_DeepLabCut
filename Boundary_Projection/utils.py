import os
import pickle
import numpy as np
import h5py
import cv2
import pandas as pd
import dev.data_types as data_types
from dev.globals import *
from matplotlib.pyplot import get_cmap

from typing import Union

vid_lookup = {}
vid_lookup['output_cam2DLC_dlcrnetms5_uf_cobotsJun7shuffle1_100000_el.h5'] =\
    'deeplabcut_project/data/uf_cobots_multicam-Derek_Perdomo-2023-06-12/videos/output_cam2.avi'
vid_lookup['output_cam1DLC_resnet50_uf_cobots_multicamJun12shuffle1_50000_el.h5'] = \
    'deeplabcut_project/data/uf_cobots_multicam-Derek_Perdomo-2023-06-12/videos/output_cam1.avi'
vid_lookup['output_cam3DLC_resnet50_uf_cobots_multicamJun12shuffle1_50000_el.h5'] =\
    'deeplabcut_project/data/uf_cobots_multicam-Derek_Perdomo-2023-06-12/videos/output_cam3.avi'

MS_PER_FRAME = int(1000/30)


def expand_bounds_by_joint(current_bounds: data_types.BoundingBox, new_joint: Union[data_types.Joint, np.ndarray]):
    # check bounds vs current bounding box, expand all
    if isinstance(new_joint, data_types.Joint):
        new_joint = new_joint.as_array()


    if new_joint[0] < current_bounds.left:
        current_bounds.left = new_joint[0]
    if new_joint[0] > current_bounds.right:
        current_bounds.right = new_joint[0]

    if new_joint[1] < current_bounds.top:
        current_bounds.top = new_joint[1]
    if new_joint[1] > current_bounds.bot:
        current_bounds.bot = new_joint[1]

    return current_bounds


def find_expanded_bounding_box(current_body: Union[data_types.Person, data_types.Arm]):
    current_joints = np.asarray([[joint.x, joint.y] for joint in current_body.joint_list])
    lastEstimate = current_body.window.estimate()
    joint_movements = np.where(np.isnan(current_joints), lastEstimate, current_joints)

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


def update_body_with_expanded_bb(body: Union[data_types.Person, data_types.Arm]):
    # make bounding box fit around actor
    for joint_estimate in body.window.estimate():
        body.bbox = expand_bounds_by_joint(body.bbox, joint_estimate)

    # body = find_expanded_bounding_box(body)

    return body


def draw_bb_on_frame(img: np.ndarray, bb: data_types.BoundingBox, color: Union[list, tuple, np.ndarray]):
    # if 'orig' in bb.name:
    #     return img
    bb.clean()
    top, bot, left, right = bb.as_array()
    img = cv2.rectangle(img, (left, top), (right, bot), color, 3)
    return img


def add_bodies_to_frame(bodies: Union[tuple, list], img: Union[np.ndarray],
                        name_lookups: dict, data_entry: np.ndarray, colors: Union[np.ndarray, tuple, list]):
    for body in bodies:
        for joint in body.joint_list:
            lookup_prefix = '_'.join([body.name, joint.name.upper(), ''])
            joint.x = data_entry[name_lookups[lookup_prefix + 'X']]
            joint.y = data_entry[name_lookups[lookup_prefix + 'Y']]
        body.bbox.reset()
        body = update_body_with_expanded_bb(body)
        # scale around joints
        body.bbox.scale_by(0.15)

        joint_values = []

        for joint in body.joint_list:
            try:
                img = cv2.circle(img, (int(joint.x), int(joint.y)), 4, colors[0], 4)
            except ValueError:
                pass
            joint_values.append([joint.x, joint.y])

        joint_values = np.asarray(joint_values)
        body.window.update(joint_values)

        for x, y in body.window.estimate():
            try:
                img = cv2.circle(img, (int(x), int(y)), 7, colors[1], 2)
            except ValueError:
                pass
        img = draw_bb_on_frame(img, body.bbox, colors[2])

    return img
    