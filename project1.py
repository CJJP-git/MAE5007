# This is a sample Python script.
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt


class Node(object):
    def __init__(self):
        self.x = []
        self.y = []


class Element(object):
    def __init__(self):
        self.node1 = []
        self.node2 = []


def openfile(path):
    data = np.loadtxt(path, dtype=np.float32, delimiter=',', comments="*")
    m = data[0:105, :]
    n = data[105:, :]
    return m, n


dot = Node()
ele = Element()

data_n, data_m = openfile("Inp_Proj1-2.txt")


dot.x = (data_n[:, 1])
dot.y = (data_n[:, 2])

ele.node1 = (data_m[:, 1])
ele.node2 = (data_m[:, 2])
for i in range(len(ele.node1)):
    x = [dot.x[int(ele.node1[i])-1], dot.x[int(ele.node2[i])-1]]
    y = [dot.y[int(ele.node1[i])-1], dot.y[int(ele.node2[i])-1]]
    plt.scatter(x, y, c='b')
    plt.plot(x, y, c='r')
