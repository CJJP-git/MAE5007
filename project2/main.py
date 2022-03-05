import numpy as np
import matplotlib.pyplot as plt

# 定义node类包含坐标x，y


class Node(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 定义element类，包含每个单元的节点坐标序号node1，node2， 单元长度length， 单元角度angle，单元刚度矩阵k


class Element(object):
    length = 0
    angle = 0
    k = np.zeros([4, 4])

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
        cls.k = [[pow(np.cos(theta), 2), np.cos(theta)*np.sin(theta), -pow(np.cos(theta), 2), -np.cos(theta)*np.sin(theta)],
             [np.cos(theta)*np.sin(theta), pow(np.sin(theta), 2), -np.cos(theta)*np.sin(theta), -pow(np.sin(theta), 2)],
             [-pow(np.cos(theta), 2), -np.cos(theta)*np.sin(theta), pow(np.cos(theta), 2), np.cos(theta)*np.sin(theta)],
             [-np.cos(theta)*np.sin(theta), -pow(np.sin(theta), 2), np.cos(theta)*np.sin(theta), pow(np.sin(theta), 2)]]
        cls.k = E * A / l * np.array(cls.k)
        return cls.k

# 定义读取文件函数，返回节点坐标到m，单元节点编号到n


def openfile(path):
    data = np.loadtxt(path, dtype=np.float32, delimiter=',', comments="*")
    m = data[0:105, :]
    n = data[105:, :]
    return m, n


# 实例化，读取数据
data_m, data_n = openfile('Inp_Proj1-2.txt')
dot = [Node(data_m[i, 1], data_m[i, 2]) for i in range(len(data_m[:, 0]))]
ele = [Element(data_n[i, 1], data_n[i, 2]) for i in range(len(data_n[:, 0]))]

# 计算每个element的angle、length与k属性，其中EA取1
for i in range(len(ele)):
    ele[i].length = ele[i].Length(dot[ele[i].node1-1].x, dot[ele[i].node1-1].y, dot[ele[i].node2-1].x, dot[ele[i].node2-1].y)
    ele[i].angle = ele[i].Angle(dot[ele[i].node1 - 1].x, dot[ele[i].node1 - 1].y, dot[ele[i].node2 - 1].x, dot[ele[i].node2 - 1].y)
    ele[i].k = ele[i].ElementK(E=1, A=1)

