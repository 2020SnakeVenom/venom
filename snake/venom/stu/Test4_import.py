import time

print(time.localtime())  # 当地时间
print(time.localtime().tm_year)

# 1 自建一个模块
# 2 continue & break
# 3 错误处理
try:
    file = open('eee.txt', 'r')
except Exception as e:
    print(e)
# 4 zip lambda map
# zip
a = [1, 2, 3]
b = [4, 5, 6]
ab = zip(a, b)
print(list(ab))
# zip中的运算
for i, j in zip(a, b):
    print(i / 2, j * 2)

# lambda
# func = lambda x,y:x+y 冒号前的x,y为自变量,冒号后x+y为具体运算
fun = lambda x, y: x + y
x = 3
y = 8
print(fun(x, y))

# map 把函数和参数绑定在一起
print('------------')


def fun(x, y):
    return (x + y)


print(list(map(fun, [3, 1], [4, 1])))

print('---------------------')

# copy & deepcopy 浅复制 深复制
