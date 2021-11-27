from numpy.lib.function_base import append


test = "60"
sp = test.split("*")
print(sp)
result = []
for s in sp:
    try:
        temp = int(s)
        result.append(temp)
    except:
        result.append(s)
print(result)