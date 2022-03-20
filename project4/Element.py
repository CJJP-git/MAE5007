
import numpy as np


# %% 定义element类，包含每个单元的节点坐标序号node1，node2， 单元长度length， 单元角度angle，单元刚度矩阵k
class Element(object):
    k = np.zeros([4, 4])
    length = 0
    angle = 0

    def __init__(self, node1, node2):
        self.node1 = int(node1)
        self.node2 = int(node2)

    # 计算单元长度

    @classmethod
    def Length(cls, x1, y1, x2, y2):
        cls.length = np.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
        return cls.length

    # 计算单元角度

    @classmethod
    def Angle(cls, x1, y1, x2, y2):
        if (x1 == x2) & (y1 > y2):
            cls.angle = np.pi / 2
        elif (x1 == x2) & (y2 > y1):
            cls.angle = -np.pi / 2
        else:
            cls.angle = np.arctan((y2 - y1) / (x2 - x1))
        return cls.angle

    # 计算单元刚度矩阵

    @classmethod
    def ElementK(cls, E, A):
        l = cls.length
        theta = cls.angle
        cls.k = [[pow(np.cos(theta), 2), np.cos(theta) * np.sin(theta), -pow(np.cos(theta), 2),
                  -np.cos(theta) * np.sin(theta)],
                 [np.cos(theta) * np.sin(theta), pow(np.sin(theta), 2), -np.cos(theta) * np.sin(theta),
                  -pow(np.sin(theta), 2)],
                 [-pow(np.cos(theta), 2), -np.cos(theta) * np.sin(theta), pow(np.cos(theta), 2),
                  np.cos(theta) * np.sin(theta)],
                 [-np.cos(theta) * np.sin(theta), -pow(np.sin(theta), 2), np.cos(theta) * np.sin(theta),
                  pow(np.sin(theta), 2)]]
        cls.k = E * A / l * np.array(cls.k)
        return cls.k