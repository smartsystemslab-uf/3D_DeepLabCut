import numpy as np
from typing import Union
from dev.globals import *

class Joint:
    def __init__(self, name):
        self.x = np.NAN
        self.y = np.NAN
        self.name = name

    def calc_diff(self, other_joint):
        return np.asarray([self.x - other_joint.x, self.y - other_joint.y])

    def __str__(self):
        return 'Joint: {} X: {} Y: {}'.format(self.name, self.x, self.y)


class BoundingBox:
    def __init__(self, name, initial_vals=None):
        self.reset()
        self.values = [self.top, self.bot, self.left, self.right]

        self.name = name

        if isinstance(initial_vals, np.ndarray) or isinstance(initial_vals, list) or isinstance(initial_vals, tuple):
            self.load_array(initial_vals)
        elif isinstance(initial_vals, BoundingBox):
            self.top = initial_vals.top
            self.bot = initial_vals.bot
            self.left = initial_vals.left
            self.right = initial_vals.right

    def __str__(self):
         return 'Top: {} Bot: {} Left: {} Right: {}'.format(self.top, self.bot, self.left, self.right)

    def as_array(self):
        return np.asarray([self.top, self.bot, self.left, self.right])

    def height(self):
        height = self.bot - self.top
        return height

    def width(self):
        width = self.right - self.left
        return width

    def load_array(self, in_array):
        self.top = in_array[0]
        self.bot = in_array[1]
        self.left = in_array[2]
        self.right = in_array[3]

    def scale_by(self, scale_amount: Union[int, float, tuple, list, np.ndarray]):
        height = self.height()
        width = self.width()
        if isinstance(scale_amount, int) or isinstance(scale_amount, float):
            scale_amount = (scale_amount, scale_amount)
        else:
            assert len(scale_amount) == 2, 'scale factor has too many values'
        assert all([x > 0 for x in scale_amount]), 'scale factor must be > 0'
        self.top -= (scale_amount[1] * height)
        self.bot += (scale_amount[1] * height)
        self.left -= (scale_amount[0] * width)
        self.right += (scale_amount[0] * width)

    def clean(self):
        if self.bot > HEIGHT-1:
            self.bot = HEIGHT-1
        if self.top < 0:
            self.top = 0
        if self.left < 0:
            self.left = 0
        if self.right > WIDTH-1:
            self.right = WIDTH-1

        self.top = int(self.top)
        self.bot = int(self.bot)
        self.left = int(self.left)
        self.right = int(self.right)

    def reset(self):
        self.top = HEIGHT
        self.bot = 0
        self.left = WIDTH
        self.right = 0


class MovingWindow:
    def __init__(self, length: int, width:int, weights: Union[tuple, list, iter, range] = None):
        self.length = length
        self.width = width
        self.buffer = np.empty((length, width, 2))
        self.buffer[:] = np.nan
        self.shape = self.buffer.shape

        if not weights:
            # weights = np.arange(length, 0, -1)
            weights = np.ones(length)
        self.weights = weights[:, np.newaxis, np.newaxis]

    def __len__(self):
        return self.length

    def update(self, new_diffs: Union[np.ndarray]):
        self.buffer = np.roll(self.buffer, 1, axis=0)
        self.buffer[0] = new_diffs

    def estimate(self):
        not_detected_joints = np.isnan(self.buffer)
        denominator = np.sum(np.where(not_detected_joints, 0, self.weights), axis=0)
        numerator = np.where(not_detected_joints, 0, self.buffer * self.weights)
        current_estimate = np.nansum(numerator, axis=0) / denominator

        diff_in_poses = current_estimate - self.buffer[-1]
        next_pose = self.buffer[0] + diff_in_poses
        return next_pose


class Person:
    def __init__(self, name, window_length=30):
        self.head = Joint('HEAD')
        self.chest = Joint('CHEST')
        self.shoulder_l = Joint('SHOULDER_L')
        self.elbow_l = Joint('ELBOW_L')
        self.wrist_l = Joint('WRIST_L')
        self.hip_l = Joint('HIP_L')
        self.ankle_l = Joint('ANKLE_L')
        self.shoulder_r = Joint('SHOULDER_R')
        self.elbow_r = Joint('ELBOW_R')
        self.wrist_r = Joint('WRIST_R')
        self.hip_r = Joint('HIP_R')
        self.ankle_r = Joint('ANKLE_R')
        self.pelvis = Joint('PELVIS')
        self.joint_list = (self.head, self.chest, self.shoulder_l, self.elbow_l, self.wrist_l, self.hip_l, self.ankle_l,
                           self.shoulder_r, self.elbow_r, self.hip_r, self.ankle_r, self.pelvis)
        self.name = name
        self.bbox = BoundingBox(name+'_bb')
        self.window = MovingWindow(length=window_length, width=len(self.joint_list))


class Arm:
    def __init__(self, name, window_length=30):
        self.base = Joint('BASE')
        self.joint1 = Joint('JOINT_1')
        self.joint2 = Joint('JOINT_2')
        self.joint3 = Joint('JOINT_3')
        self.joint4 = Joint('JOINT_4')
        self.finger1 = Joint('FINGER1')
        self.finger2 = Joint('FINGER2')
        self.joint_list = (self.base, self.joint1, self.joint2, self.joint3, self.joint4, self.finger1, self.finger2)
        self.bbox = BoundingBox(name+'_bb')
        self.window = MovingWindow(length=window_length, width=len(self.joint_list))

        # H5 POS Columns
        # self.h5_lookup = {}
        # self.h5_lookup['H5_BASE_LOC_X'] = 45
        # self.h5_lookup['H5_BASE_LOC_Y'] = 46
        # self.h5_lookup['H5_JOINT1_LOC_X'] = 48
        # self.h5_lookup['H5_JOINT1_LOC_Y'] = 49
        # self.h5_lookup['H5_JOINT2_LOC_X'] = 51
        # self.h5_lookup['H5_JOINT2_LOC_Y'] = 52
        # self.h5_lookup['H5_JOINT3_LOC_X'] = 54
        # self.h5_lookup['H5_JOINT3_LOC_Y'] = 55
        # self.h5_lookup['H5_JOINT4_LOC_X'] = 57
        # self.h5_lookup['H5_JOINT4_LOC_Y'] = 58
        # self.h5_lookup['H5_FINGER1_LOC_X'] = 60
        # self.h5_lookup['H5_FINGER1_LOC_Y'] = 61
        # self.h5_lookup['H5_FINGER2_LOC_X'] = 63
        # self.h5_lookup['H5_FINGER2_LOC_Y'] = 64
        self.name = name


class Frame:
    def __init__(self):
        self.arms = []
        self.persons = []
        self.currentFrameNum = None
        self.nextFrame = None
        self.prevFrame = None
        self.currentTask = None
