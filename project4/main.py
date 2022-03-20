import numpy as np
from Node import Node
from Element import Element
from Boundary_condition import boundary_cd, Cload


# %% 定义读取文件函数，返回节点坐标到m，单元节点编号到n
def openfile(path):
    global data_node, data_element, data_boundary
    f = open(path, 'r')
    data = []
    for lines in f:
        if lines.startswith("*Node"):
            lines = f.readline()
        elif lines.startswith("*Element"):
            lines = f.readline()
            data_node = data
            data = []
        elif lines.startswith("*Boundary"):
            lines = f.readline()
            data_element = data
            data = []
        elif lines.startswith("*Cload"):
            lines = f.readline()
            data_boundary = data
            data = []
        a = lines.strip().split(",")
        b = [float(x) for x in a]
        data.append(b)
    return np.array(data_node), np.array(data_element), np.array(data_boundary), np.array(data)


# %% 读取数据
data_node, data_element, data_boundary, data_Cload = openfile('Inp_Simplified.txt')

# %%实例化，计算每个element的angle、length与k属性，其中EA取1
dot = [Node(data_node[i, 1], data_node[i, 2]) for i in range(len(data_node[:, 0]))]
ele = [Element(data_element[i, 1], data_element[i, 2]) for i in range(len(data_element[:, 0]))]
for i in range(len(ele)):
    ele[i].length = ele[i].Length(dot[ele[i].node1 - 1].x, dot[ele[i].node1 - 1].y, dot[ele[i].node2 - 1].x,
                                  dot[ele[i].node2 - 1].y)
    ele[i].angle = ele[i].Angle(dot[ele[i].node1 - 1].x, dot[ele[i].node1 - 1].y, dot[ele[i].node2 - 1].x,
                                dot[ele[i].node2 - 1].y)
    ele[i].k = ele[i].ElementK(E=1, A=1)


# %% 定义拼接函数
def k_assemble(k_total, k, node1, node2):
    for i in range(4):
        for j in range(4):
            k_total[4 * (node1 - 1) + i, 4 * (node2 - 1) + j] = \
                k_total[4 * (node1 - 1) + i, 4 * (node2 - 1) + j] + k[i, j]
    return k_total


# %% 拼接
k_total = np.zeros([4 * len(dot), 4 * len(dot)])
for i in range(len(ele)):
    k_total = k_assemble(k_total, ele[i].k, ele[i].node1, ele[i].node2)

# %%对节点施加约束
boundary = [boundary_cd(data_boundary[i, 0], data_boundary[i, 1], data_boundary[i, 2]) for i in
            range(len(data_boundary[:, 0]))]
load = [Cload(data_Cload[i, 0], data_Cload[i, 1], data_Cload[i, 2]) for i in range(len(data_Cload[:, 0]))]
