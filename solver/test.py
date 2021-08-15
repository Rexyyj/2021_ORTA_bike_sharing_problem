import numpy as np

data = np.around(np.random.uniform(
    0,
    100,
    size=(1,5,5))
)
print(data)
print(data[0][2,3])