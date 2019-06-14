import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x = np.random.randint(low=0, high=10, size=1000)
# 增加3个11到20之间的数据
xmax = np.random.randint(low=11, high=20, size=3)
# 增加3个-15到-1之间的数据
xmin = np.random.randint(low=-15, high=-1, size=3)
# 合并三个数组
x = np.append(np.append(x, xmin), xmax)
# 将numpy行向量转成DF，以便用value_counts()统计每个评分出现的次数
df = pd.DataFrame({"a": x})
cn = df["a"].value_counts()  # 统计次数，返回序列
bin = cn.sort_index()  # 对每个评分做排序
print(bin)
print(df.describe())

figure, ax = plt.subplots()
plt.boxplot(x)
plt.xlabel("user")
ax.set_xticklabels("A")
plt.ylabel("score")
plt.title("Grade distribution")
plt.show()

# https://towardsdatascience.com/understanding-boxplots-5e2df7bcbd51
