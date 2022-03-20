# %%
# 定义node类包含坐标x，y
class Node(object):
    def __init__(self, x, y,x_force=0,y_force=0):
        self.x = x
        self.y = y
        self.x_force = x_force
        self.y_force = y_force
