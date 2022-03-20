import numpy as np
from Node import Node
from Element import Element
import matplotlib.pyplot as plt


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

# %%画图
for i in range(len(ele)):
    x = [dot[int(ele[i].node1) - 1].x, dot[int(ele[i].node2) - 1].x]
    y = [dot[int(ele[i].node1) - 1].y, dot[int(ele[i].node2) - 1].y]
    # plt.scatter(x, y, c='b')
    plt.plot(x, y, c='r')
plt.show()


# %% 定义拼接函数

def k_assemble(ele, dot):
    k_total = np.zeros([2 * len(dot), 2 * len(dot)])

    for ele_num in range(len(ele)):
        for i in range(4):
            for j in range(4):
                if (i <= 1) & (j <= 1):
                    k_total[2 * (int(ele[ele_num].node1) - 1) + i, 2 * (int(ele[ele_num].node1) - 1) + j] += \
                        ele[ele_num].k[i, j]
                elif (i >= 2) & (j <= 1):
                    k_total[2 * (int(ele[ele_num].node2) - 1) + i - 2, 2 * (int(ele[ele_num].node1) - 1) + j] += \
                        ele[ele_num].k[i, j]
                elif (i <= 1) & (j >= 2):
                    k_total[2 * (int(ele[ele_num].node1) - 1) + i, 2 * (int(ele[ele_num].node2) - 1) + j - 2] += \
                        ele[ele_num].k[i, j]
                elif (i >= 2) & (j >= 2):
                    k_total[2 * (int(ele[ele_num].node2) - 1) + i - 2, 2 * (int(ele[ele_num].node2) - 1) + j - 2] += \
                        ele[ele_num].k[i, j]

    return k_total


# %%求解全局刚度矩阵
k_total = k_assemble(ele, dot)

# %%用置大数法处理约束

for i in range(len(data_boundary)):
    if (data_boundary[i, 1]) == 1:
        k_total[2 * (int(data_boundary[i, 0]) - 1), 2 * (int(data_boundary[i, 0]) - 1)] = 1e20
    if (data_boundary[i, 2]) == 2:
        k_total[2 * (int(data_boundary[i, 0]) - 1)+1, 2 * (int(data_boundary[i, 0]) - 1)+1] = 1e20
        pass

# %%写出载荷矩阵
force = np.zeros([2 * len(dot), 1])
for i in range(len(data_Cload)):
    if data_Cload[1, 1] == 1:
        force[2 * (int(data_Cload[i, 0] - 1)), 0] = data_Cload[i, 2]
    elif data_Cload[1, 1] == 2:
        force[2 * (int(data_Cload[i, 0] - 1)) + 1, 0] = data_Cload[i, 2]
# %%解最终节点位移
u = np.array(np.matrix(k_total).I * force)
