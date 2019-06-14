import numpy as np
import matplotlib.pyplot as plt

# 这里x可以理解为美团用户A对100个菜品的评分
x = np.random.random(100) * 10
# 这里y可以理解为美团用户B对100个菜品的评分
y = np.random.random(100) * 10

# 让点的面积随机在这10个数之间
area = np.random.random(10) * 50
# 设置横坐标名称
plt.xlabel("B")
# 设置纵坐标名称
plt.ylabel("A")
# 设置标题
plt.title("User ratings")
plt.scatter(x, y, s=area, c="y")

plt.show()
