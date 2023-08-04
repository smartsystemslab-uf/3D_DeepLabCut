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
        self.top = HEIGHT
        self.bot = 0
        self.left = WIDTH
        self.right = 0
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


class MovingWindow:
    def __init__(self, length: int, width:int, weights: Union[tuple, list, iter, range] = None):
        self.length = length
        self.width = width
        self.buffer = np.zeros((length, width, 2))
        self.shape = self.buffer.shape

        if not weights:
            # weights = np.arange(length, 0, -1)
            weights = np.ones(length)

        self.weights = weights[:, np.newaxis, np.newaxis]

    def __len__(self):
        return self.length

    def update(self, new_joints: Union[np.ndarray]):
        self.buffer = np.roll(self.buffer, 1, axis=0)
        self.buffer[0] = new_joints

    def estimate(self):
        denominator = sum(self.weights)
        numerator = self.buffer * self.weights
        return numerator.sum(axis=0)/denominator


class Person:
    def __init__(self, name, window_length=5):
        self.head = Joint('HEAD')
        self.chest = Joint('CHEST')
        self.shoulder_l = Joint('SHOULDER_L')
        self.elbow_l = Joint('ELBOW_L')
        self.wrist_l = Joint('WRIST_L')
        self.hip_l = Joint('HIP_L')
        self.ankle_l = Joint('ANKKLE_L')
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

        # H5 POS Columns
        self.h5_lookup = {}
        self.h5_lookup['H5_HEAD_LOC_X'] = 66
        self.h5_lookup['H5_HEAD_LOC_Y'] = 67
        self.h5_lookup['H5_CHEST_LOC_X'] = 69
        self.h5_lookup['H5_CHEST_LOC_Y'] = 70
        self.h5_lookup['H5_SHOULDER_L_LOC_X'] = 72
        self.h5_lookup['H5_SHOULDER_L_LOC_Y'] = 73
        self.h5_lookup['H5_ELBOW_L_LOC_X'] = 78
        self.h5_lookup['H5_ELBOW_L_LOC_Y'] = 79
        self.h5_lookup['H5_WRIST_L_LOC_X'] = 84
        self.h5_lookup['H5_WRIST_L_LOC_Y'] = 85
        self.h5_lookup['H5_HIP_L_LOC_X'] = 93
        self.h5_lookup['H5_HIP_L_LOC_Y'] = 94
        self.h5_lookup['H5_ANKLE_L_LOC_X'] = 105
        self.h5_lookup['H5_ANKLE_L_LOC_Y'] = 106
        self.h5_lookup['H5_SHOULDER_R_LOC_X'] = 75
        self.h5_lookup['H5_SHOULDER_R_LOC_Y'] = 76
        self.h5_lookup['H5_ELBOW_R_LOC_X'] = 81
        self.h5_lookup['H5_ELBOW_R_LOC_Y'] = 82
        self.h5_lookup['H5_WRIST_R_LOC_X'] = 87
        self.h5_lookup['H5_WRIST_R_LOC_Y'] = 88
        self.h5_lookup['H5_HIP_R_LOC_X'] = 96
        self.h5_lookup['H5_HIP_R_LOC_Y'] = 97
        self.h5_lookup['H5_ANKLE_R_LOC_X'] = 108
        self.h5_lookup['H5_ANKLE_R_LOC_Y'] = 109
        self.h5_lookup['H5_PELVIS_LOC_X'] = 90
        self.h5_lookup['H5_PELVIS_LOC_Y'] = 91

        # # Output Camera 2 has knees which are not needed
        # self.h5_lookup['H5_ANKLE_L_2_LOC_X'] = 105
        # self.h5_lookup['H5_ANKLE_L_2_LOC_Y'] = 106
        # self.h5_lookup['H5_ANKLE_R_2_LOC_X'] = 108
        # self.h5_lookup['H5_ANKLE_R_2_LOC_Y'] = 109


class Arm:
    def __init__(self, name, window_length=5):
        self.base = Joint('BASE')
        self.joint1 = Joint('JOINT1')
        self.joint2 = Joint('JOINT2')
        self.joint3 = Joint('JOINT3')
        self.joint4 = Joint('JOINT4')
        self.finger1 = Joint('FINGER1')
        self.finger2 = Joint('FINGER2')
        self.joint_list = (self.base, self.joint1, self.joint2, self.joint3, self.joint4, self.finger1, self.finger2)
        self.bbox = BoundingBox(name+'_bb')
        self.window = MovingWindow(length=window_length, width=len(self.joint_list))

        # H5 POS Columns
        self.h5_lookup = {}
        self.h5_lookup['H5_BASE_LOC_X'] = 45
        self.h5_lookup['H5_BASE_LOC_Y'] = 46
        self.h5_lookup['H5_JOINT1_LOC_X'] = 48
        self.h5_lookup['H5_JOINT1_LOC_Y'] = 49
        self.h5_lookup['H5_JOINT2_LOC_X'] = 51
        self.h5_lookup['H5_JOINT2_LOC_Y'] = 52
        self.h5_lookup['H5_JOINT3_LOC_X'] = 54
        self.h5_lookup['H5_JOINT3_LOC_Y'] = 55
        self.h5_lookup['H5_JOINT4_LOC_X'] = 57
        self.h5_lookup['H5_JOINT4_LOC_Y'] = 58
        self.h5_lookup['H5_FINGER1_LOC_X'] = 60
        self.h5_lookup['H5_FINGER1_LOC_Y'] = 61
        self.h5_lookup['H5_FINGER2_LOC_X'] = 63
        self.h5_lookup['H5_FINGER2_LOC_Y'] = 64
        self.name = name


class Frame:
    def __init__(self):
        self.arms = []
        self.persons = []
        self.currentFrameNum = None
        self.nextFrame = None
        self.prevFrame = None
        self.currentTask = None
