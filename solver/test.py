import numpy as np

data = np.around(np.abs(np.random.normal(
    10,
    5,
    size=(5,5))
))
print(data)
