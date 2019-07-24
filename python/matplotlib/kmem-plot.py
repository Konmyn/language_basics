# import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ValueError: Unrecognized backend string 'gtkagg': valid strings are ['GTK3Agg', 'GTK3Cairo', 'MacOSX', 'nbAgg', 'Qt4Agg', 'Qt4Cairo', 'Qt5Agg', 'Qt5Cairo', 'TkAgg', 'TkCairo', 'WebAgg', 'WX', 'WXAgg', 'WXCairo', 'agg', 'cairo', 'pdf', 'pgf', 'ps', 'svg', 'template']
# matplotlib.use('GTK3Agg')  # 算了，不好用

# file, title = "kmem-4gheap6glimit.log", "kmem growth by time(4g heap, 6g limit)"
# file, title = "kmem-4gheap6glimit-oraclejdk.log", "kmem growth by time(4g heap, 6g limit, oracle jdk)"
# file, title = "kmem-8gheap18glimit-inuse.log", "kmem growth by time(8g heap, 18g limit, in use)"
file, title = "kmem-8gheap32glimit-inuse.log", "kmem growth by time(8g heap, 32g limit, in use)"
with open(file, "r") as f:
    data = f.readlines()
    time = np.array(list(map(lambda x: datetime.strptime(x[4:28], "%b %d %H:%M:%S CST %Y"), data)))
    kmem = np.array(list(map(lambda x: int(x[29: -2]), data)))

plt.plot(time, kmem, c="b")
plt.xlabel("Time")
plt.ylabel("Kmem(Bytes)")
plt.title(title)
plt.grid()

plt.show(block=True)  # 怎么对这个绘图耗时计时？
