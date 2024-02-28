import numpy as np

from lib import vector_apply_euler_arr
from lib1 import vector_apply_euler, Vector3, Euler

# generate random 3d vector

for _ in range(10000):
    vector = np.random.rand(3)
    euler = np.random.rand(3)

    v1 = vector_apply_euler_arr(vector.copy(), euler.copy())
    v2 = vector_apply_euler(Vector3(*vector), Euler(*euler))

    v2 = np.array([v2.x, v2.y, v2.z])

    # check if v1, v2 are the same
    if not np.allclose(v1, v2):
        print("v1", v1)
        print("v2", v2)
    else:
        # print("ok")
        pass
