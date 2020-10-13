"""
class 定义一个类,后面的类别首字母推荐大写的
class后面还可以跟def,定义一个函数,比如 def add(self,x,y):加法
其他的函数定义方法一样,注意这里的self是默认值
"""


class Calculator:  # 首字母大写,冒号不能缺
    name = 'Good Calculator'  # 该行为class的属性
    price = 18

    def add(self, x, y):
        print(self.name)
        result = x + y
        print(result)

    def minus(self, x, y):
        result = x - y
        print(result)

    def times(self, x, y):
        print(x * y)

    def divide(self, x, y):
        print(x / y)


cal = Calculator()  # 注意这里运行class的时候要加()
print('cal_name=', cal.name)
print('cal_price=', cal.price)

cal.add(10, 20)

cal.minus(10, 20)

print('1=======================================')

# 2 class 类 init功能
"""
__init__可以理解成初始化class的变量,取自英文中initial最初的意思,可以在运行时,给初始值赋值
"""


class Calculator2:
    name = 'good calculator'
    price = 18

    def __init__(self, name, price, height, width, weight):  # 注意这里的下划线是双下划线
        self.name = name
        self.price = price
        self.h = height
        self.wi = width
        self.we = weight


c = Calculator2('bad calculator', 18, 17, 16, 15)
print('c-name', c.name)
print('c-price', c.price)
print('c-h', c.h)

"""
如何设置属性的默认值,直接在def里出入即可

"""


class Calculator3:
    name = 'good calculator'
    price = 18

    def __init__(self, name, price, height=10, width=14, weight=16):  # 注意这里的下划线是双下划线
        self.name = name
        self.price = price
        self.h = height
        self.wi = width
        self.we = weight


c3 = Calculator3('bad calculator', 19)
print('c-price', c3.price)
print('c-h', c3.h)
c3.we = 22
print('c3-we', c3.we)
print('3----------------------------------')
# 3 input 输入
# variable=input()表示运行之后,可以在屏幕中输入一个数字,该数字会赋值给自变量
# a_input = input('please input a number:')
# print('this number is:', a_input)

# 4 元组 列表
# Tuple ,用小括号或者无括号来表述
a_tupe = (1, 2, 3, 4, 5, 6, 3)
a2_tuple = 1, 2, 3, 4, 5
# list 以中括号来命名的
a_list = [1, 2, 3, 4, 5, 6, 7]
# 对比
for content in a_tupe:
    print(content)
print('--------------')
for content_list in a_list:
    print(content_list)

# 依次输出a_tuple和a_list中的各个元素
for index in range(len(a_list)):
    print('index=', index, 'number in list=', a_list[index])

print('----------')
for index in range(len(a2_tuple)):
    print('index=', index, 'number in tuple=', a2_tuple[index])
print('4--------------------------------')
# 5 list列表
# 列表是一些列有序的数列,有一系列自带的动能
a = [1, 2, 3, 4, 1, 1, -1]
a.append(0)  # 在a的最后面追加一个0
print(a)
a.insert(1, 0)  # 在位置1 处添加0
print(a)

# list 移除
a = [1, 2, 3, 4, 1, 1, -1]
a.remove(2)  # 删除列表中第一个出现的值为2的项
print(a)
# list 索引
# 显示特定位
a = [1, 2, 3, 4, 1, 1, -1]
print(a[0])  # 显示列表a的第0位的值
print(a[-1])  # 显示列表a的最末尾的值

print(a[0:3])  # 显示列表a的从第0位到第2位的所有项的值
print(a[5:])  # 显示列表a的第5位及以后的所有项的值
print(a[-3:])  # 显示列表a的倒数第3位及以后的所有项的值

# 打印列表中的某个值得索引index
print(a.index(2))  # 显示列表a中第一次出现的值为2的项的索引

# 统计列表中某值出现的次数
print(a.count(1))

# list排序
# 对列表的项进行排序
a.sort()  # 默认从小到大排序
print(a)
a.sort(reverse=True)  # 从大到小排序
print(a)
print('-----------------')
# 多维列表
a = [1, 2, 3, 4, 5]  # 一行五列
multi_dim_a = [[1, 2, 3],
               [2, 3, 4],
               [3, 4, 5]]  # 三行三列
print(a[1])
print(multi_dim_a[0][1])
print('---------------------')

# dictionary字典
a_list = [1, 2, 3, 4, 5, 6, 7, 8]
d1 = {'apple': 1, 'pear': 2, 'orange': 3}
d2 = {1: 'a', 2: 'b', 3: 'c'}
d3 = {1: 'a', 'b': 2, 'c': 3}
print(d1['apple'])
print(a_list[0])
print('-------')

del d1['pear']
print(d1)
d1['b']=20
print(d1)