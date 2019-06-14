import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 这里可以理解为美团用户A对10个菜品的评分
x = np.random.randint(low=0, high=10, size=1000)
# 将numpy行向量转成DF，以便用value_counts()统计每个评分出现的次数
df = pd.DataFrame({"a": x})
# 统计次数，返回序列
cn = df["a"].value_counts()
# 对每个评分做排序
bin = cn.sort_index()
print(bin)
# plt.hist(x,bins=4,color='y',range=(0, 10), rwidth=1)
plt.hist(
    x, bins=[0, 1, 2, 4, 10], color="y", range=(0, 10), edgecolor="black", linewidth=1.2
)
plt.xlabel("score")
plt.ylabel("count")
plt.title("Grade distribution")
plt.show()
