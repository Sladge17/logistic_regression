# lst = list(range(5))
# lst.pop(2)
# print(lst)

# lst = [1, 2, 'NaN', 4]
# lst = list(filter(lambda x: type(x) == int, lst))
# print(lst)

# q = -9.8
# print(q // 1)
# print('q' * 2)

# lst = [17, 19, 21, 22, 22, 23]
# mean_lst = sum(lst) / len(lst)
# div = [(i - mean_lst) ** 2 for i in lst]
# std = (sum(div) / (len(div) - 1)) ** 0.5
# print(std)

# lst = [1,5,3,2,8,7]
# lst = sorted(lst)
# print(lst)

# q = 3.0
# print(q%1 == True)

import math

q = 3.0
# q = 3.2
# q = 3.5
# q = 3.8
# q = 4
print(math.ceil(q))