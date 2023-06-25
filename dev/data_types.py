class Joint:
    def __init__(self):
        self.x = None
        self.y = None
class BoundingBox:
    def __init__(self):
        self.top = -1
        self.left= 1e9
        self.right= -1
        self.bot = 1e9
class Person:
    def __init__(self):
        self.head = Joint()
        self.chest = Joint()
        self.shoulder_l = Joint()
        self.elbow_l = Joint()
        self.wrist_l = Joint()
        self.hip_l = Joint()
        self.ankle_l = Joint()
        self.shoulder_r = Joint()
        self.elbow_r = Joint()
        self.wrist_r = Joint()
        self.hip_r = Joint()
        self.ankle_r = Joint()
        self.pelvis = Joint()
        self.joint_list = []
        self.bbox = BoundingBox()

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

    def __init__(self):
        self.base = Joint()
        self.joint1 = Joint()
        self.joint2 = Joint()
        self.joint3 = Joint()
        self.joint4 = Joint()
        self.finger1 = Joint()
        self.finger2 = Joint()
        self.joint_list = []
        self.bbox = BoundingBox()

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

class Frame:
    def __init__(self):
        self.arm = Arm()
        self.person = Person()
        self.nextFrame = None
        self.prevFrame = None