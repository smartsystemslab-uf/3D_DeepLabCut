class Joint:
    def __init__(self):
        self.x = None
        self.y = None
        
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

class Arm:

    def __init__(self):
        self.base = Joint()
        self.joint1 = Joint()
        self.joint2 = Joint()
        self.joint3 = Joint()
        self.joint4 = Joint()
        self.finger1 = Joint()
        self.finger2 = Joint()

        # H5 POS Columns
        self.H5_BASE_LOC = 45

