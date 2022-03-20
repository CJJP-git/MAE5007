import numpy as np


# %% 定义边界条件类
class boundary_cd(object):
    node_num = 0
    x_axis = 0
    y_axis = 0
    z_axis = 0

    def __init__(self, node_num, start, stop):
        self.ele_num = node_num
        if (start == 1) & (stop == 3):
            self.x_axis = 1
            self.y_axis = 1
            self.z_axis = 1
        elif (start == 1) & (stop == 2):
            self.x_axis = 1
            self.y_axis = 1
        elif (start == 1) & (stop == 1):
            self.x_axis = 1
        elif (start == 2) & (stop == 3):
            self.y_axis = 1
            self.z_axis = 1
        elif (start == 3) & (stop == 3):
            self.z_axis = 1


# %% 定义载荷类
class Cload(object):

    def __init__(self, node_mum, force_axis, force):
        self.node_num = node_mum
        self.force_axis = force_axis
        self.force = force
