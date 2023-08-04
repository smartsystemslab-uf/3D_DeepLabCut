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


class Person:
    def __init__(self, name):
        self.head = Joint('head')
        self.chest = Joint('chest')
        self.shoulder_l = Joint('shoulder_l')
        self.elbow_l = Joint('elbow_l')
        self.wrist_l = Joint('wrist_l')
        self.hip_l = Joint('hip_l')
        self.ankle_l = Joint('ankle_l')
        self.shoulder_r = Joint('shoulder_r')
        self.elbow_r = Joint('elbow_r')
        self.wrist_r = Joint('wrist_r')
        self.hip_r = Joint('hip_r')
        self.ankle_r = Joint('ankle_r')
        self.pelvis = Joint('pelvis')
        self.joint_list = (self.head, self.chest, self.shoulder_l, self.elbow_l, self.wrist_l, self.hip_l, self.ankle_l,
                           self.shoulder_r, self.elbow_r, self.hip_r, self.ankle_r, self.pelvis)
        self.name = name
        self.bbox = BoundingBox(name+'_bb')

        # H5 POS Columns
        self.H5_HEAD_LOC_X = 66
        self.H5_HEAD_LOC_Y = 67
        self.H5_CHEST_LOC_X = 69
        self.H5_CHEST_LOC_Y = 70
        self.H5_SHOULDER_L_LOC_X = 72
        self.H5_SHOULDER_L_LOC_Y = 73
        self.H5_ELBOW_L_LOC_X = 78
        self.H5_ELBOW_L_LOC_Y = 79
        self.H5_WRIST_L_LOC_X = 84
        self.H5_WRIST_L_LOC_Y = 85
        self.H5_HIP_L_LOC_X = 93
        self.H5_HIP_L_LOC_Y = 94
        self.H5_ANKLE_L_LOC_X = 99
        self.H5_ANKLE_L_LOC_Y = 100
        self.H5_SHOULDER_R_LOC_X = 75
        self.H5_SHOULDER_R_LOC_Y = 76
        self.H5_ELBOW_R_LOC_X = 81
        self.H5_ELBOW_R_LOC_Y = 82
        self.H5_WRIST_R_LOC_X = 87
        self.H5_WRIST_R_LOC_Y = 88
        self.H5_HIP_R_LOC_X = 96
        self.H5_HIP_R_LOC_Y = 97
        self.H5_ANKLE_R_LOC_X = 102
        self.H5_ANKLE_R_LOC_Y = 103
        self.H5_PELVIS_LOC_X = 90
        self.H5_PELVIS_LOC_Y = 91

        # Output Camera 2 has knees which are not needed
        self.H5_ANKLE_L_2_LOC_X = 105
        self.H5_ANKLE_L_2_LOC_Y = 106
        self.H5_ANKLE_R_2_LOC_X = 108
        self.H5_ANKLE_R_2_LOC_Y = 109


class Arm:
    def __init__(self, name):
        self.base = Joint('base')
        self.joint1 = Joint('joint1')
        self.joint2 = Joint('joint2')
        self.joint3 = Joint('joint3')
        self.joint4 = Joint('joint4')
        self.finger1 = Joint('finger1')
        self.finger2 = Joint('finger2')
        self.joint_list = (self.base, self.joint1, self.joint2, self.joint3, self.joint4, self.finger1, self.finger2)
        self.bbox = BoundingBox(name+'_bb')

        # H5 POS Columns
        self.H5_BASE_LOC_X = 45
        self.H5_BASE_LOC_Y = 46
        self.H5_JOINT1_LOC_X = 48
        self.H5_JOINT1_LOC_Y = 49
        self.H5_JOINT2_LOC_X = 51
        self.H5_JOINT2_LOC_Y = 52
        self.H5_JOINT3_LOC_X = 54
        self.H5_JOINT3_LOC_Y = 55
        self.H5_JOINT4_LOC_X = 57
        self.H5_JOINT4_LOC_Y = 58
        self.H5_FINGER1_LOC_X = 60
        self.H5_FINGER1_LOC_Y = 61
        self.H5_FINGER2_LOC_X = 63
        self.H5_FINGER2_LOC_Y = 64
        self.name = name


class Frame:
    def __init__(self):
        self.arms = []
        self.persons = []
        self.currentFrameNum = None
        self.nextFrame = None
        self.prevFrame = None
        self.currentTask = None

class MovingWindow:
    def __init__(self, size: int, weights: tuple):
        self.size = size
        self.buffer = [(0, 0)] * size
        self.weights = weights

    def __len__(self):
        return self.size

    def update(self, new_value: Union[float, np.float32]):
        self.buffer.pop()
        self.buffer.insert(0, new_value)

    def calc(self):
        total_x = sum([self.buffer[i][0] * self.weights[i] for i in range(self.size)])
        total_y = sum([self.buffer[i][1] * self.weights[i] for i in range(self.size)])
        return total_x, total_y
