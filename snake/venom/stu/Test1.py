

# 1 print 字符串
print("hello world")
print('hello world2')

# 2 print 字符串叠加
print('hello world' + ' hello hk')

# 3 简单运算
print(1 + 1)
print(3 - 1)
print(3 * 4)
print(12 / 4)
# print('phton'+4) 字符串不可以直接和数字相加

# int()和float();当int()一个浮点型数时,int会保留整数部分,比如int(1.9),会输出1,而不是四舍五入
print(int(2) + 3)  # int 定义为整数型
print(int(1.9))  # 当int一个浮点型数时,int会保留整数部分
print(float('1.2') + 3)  # float()是浮点型,可以把字符串转换成小数

# 4 ^与 **
# ^ 用两个**表示,如3的平方为3**2, **3表示立方,**4表示4次方
print(3 ** 2)  # **2表示2次方
print(3 ** 3)  # **3表示3次方
print(3 ** 4)  # **4表示4次方

# 5 取余数 %
print(8 % 3)

# 6 自变量命名规则
apple = 1  # 赋值 数字
print(apple)
apple = 'phton xxoo'  # 赋值 字符串
print(apple)
# 一次定义多个自变量 a,b,c=1,2,3
a, b, c = 11, 12, 13
print(a, b, c)

# 7 while循环
"""
while condition:
    expression
其中condition为判断条件,在python中就是True和False其中的一个,如果为True
那么将执行expression语句,否则将跳过该while语句块接着往下执行
"""
# 打印0-9的所有数据
condition = 0
while condition < 10:
    print(condition)
    condition += 1
print('------------------------')
a = range(10)
while a:
    print(a[-1])
    a = a[:len(a) - 1]
print('-------------------------------------')
# 8 for 循环
"""
for item in sequence:
    expressions
"""
example_list = [1, 2, 3, 4, 5, 6, 7, 12, 345, 213, 34, 5, 6, 3, 2, 5]
for i in example_list:
    print(i)
    print('inner of for')
print('outer of for')
print('--------------------------------------')
# 9 range 使用
# 9.1 range(start,stop) [start,stop) [其实值,结束值)
for i in range(1, 3):
    print(i)
print('------------------------------')
# 9.2 range(stop) 省略start从0开始,相当于range[0,stop)
# 9.3 range(start,stop,step) step代表的为步长,即相隔的两个值得差值
for i in range(0, 13, 5):
    print(i)
print('------------------------------')
# 10 内置集合
# 10.1 tuple类型
tup = ('python', 2.7, 64)
for i in tup:
    print(i)
print('-----------------------------')
# 10.2 dictionary类型
dic = {}
dic['lan'] = 'python'
dic['version'] = 3.7
dic['platform'] = 64
for key in dic:
    print(key, dic[key])
print('10.2---------------------------')
# 注意字典中key是乱序的,也就是说和插入的顺序是不一致的,如果想使用一致的字典,使用collections模块中的OrderedDict对象
# 10.3 set类型
s = set(['python', 'python2', 'python3', 'python'])
for item in s:
    print(item)
# set集合将会去除重复项,注意输出的结果也不是按照输入的顺序
print('10.3-------------------------------')

# 11 迭代器
"""
只要类中实现了__iter__和next函数,那么对象就可以在for语句中使用
"""


class Fib(object):
    def __init__(self, max):
        self.max = max
        self.n, self.a, self.b = 0, 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n = self.n + 1
            return r
        raise StopIteration


for i in Fib(5):
    print(i)
print('11--------------------------------------')

# 12 生成器
"""
除了使用迭代器以外,Python 使用 yield 关键字也能实现类似迭代的效果
yield 语句每次 执行时,立即返回结果给上层调用者,而当前的状态仍然保留
以便迭代器下一次循环调用.这样做的 好处是在于节约硬件资源,在需要的时候才会执行,并且每次只执行一次
"""


def fib(max):
    a, b = 0, 1
    while max:
        r = b
        a, b = b, a + b
        max -= 1
        yield r


for i in fib(5):
    print(i)
print('12--------------------------------')

# 13 if
x = 1
y = 2
z = 3
if x < y < z:
    print('x is less than y')

if (x < y) and (y < z):
    print('x is less than y')

if x == y:
    print('x is equal to y')

print('13---------------------------------')

# 14 if else
x, y, z = 1, 2, 3
if x > y:
    print('x is greater than y')
else:
    print('x is less or equal to y')
print('14-------------------------------')

# 15 python可以通过if-else的行内表达式完成类似三目操作
worked = True
result = 'done' if worked else 'not yet'
print(result)
# 首先判断如果work为True,那么将done字符串赋给result,否则将not yet赋给result,
print('15----------------------------')

# 16 if elif else 判断
x, y, z = 4, 2, 3
if x > 1:
    print('x>1')
elif x < 1:
    print('x<1')
else:
    print('x=1')
print('finish')

print('16---------------------------')

# 17 def 函数
"""
def function_name(paramters):
    expressions
括号内部为函数的参数
内部为函数的具体功能实现代码,如果想要函数有返回值,在expression中的逻辑代码中用return返回
"""


def function():
    print('thie is a function')
    a = 1 + 2
    print(a)


function()
# 17.2 函数参数 指定一些变量 函数的参数,函数调用的时候
"""
def function_name(parameters):
    expressions
"""


def func(a, b):
    c = a + b
    print('a=', a)
    print('this c is', c)


func(1, 2)
func(b=2, a=1)


# 如果忘记了函数的参数的位置,只知道各个参数的名字,可以在函数调用的过程中给指明特定的参数,参数的位置将不受影响

# 17.3 函数默认参数
def sale_car(price, color='red', brand='ct5', is_second_hand=True):
    print('price', price,
          'color', color,
          'brand', brand,
          'is_second_hand', is_second_hand)


sale_car('红色')

# 17.4 自调用
"""
如果想要在执行脚本的时候执行一些代码,比如单元测试,可以在脚本最后加上单元测试代码
但是该脚本作为一个模块对外提供功能的时候单元测试代码也会执行
这些往往我们不想要的
我们可以把这些代码放入脚本最后
"""
if __name__ == '__main__':
    sale_car('xxx')


# 17.5 可变参数
# 可变参数在函数定义不能出现在特定参数和默认参数前面,因为可变参数会吞噬掉这些参数
def report(name, *grades):
    total_grade = 0
    for grade in grades:
        total_grade += grade
    print(name, 'total grade is', total_grade)


report('小黑', 100, 99, 98)

# 17.6 关键字参数
"""
关键字参数可以传入0个或者任意个含参数名的参数,这些参数名在函数定义中并没有出现
这些参数在函数内部自动封装成一个字典dict
"""


def portrait(name, **kw):
    print('name is', name)
    for k, v in kw.items():
        print(k, v)


portrait('小黑2', age=24, country='china', education='bachelor')

print('17---------------------------------------')
# 18 全局 & 局部 变量
# 局部变量 在def中,我们可以定义一个局部变量,这个变量a只能在这个功能fun中有效,出了这个功能,a这个变量就不是那个局部的a
apply = 100  # 全局变量


def fun():
    a = 10  # 局部变量
    return a + 100


print(apply)

# 全局变量
"""
如何在外部也能调用一个在局部里修改了的全局变量呢
首先我们在外部定义一个全局变量a=None
然后再fun()中声明这个a是来自外部的a
声明方式就是global a
然后对这个外部的a修改后,修改的效果会被施加到外部的a上,
"""
apply = 100
a = None


def fun():
    global a  # 使用之前在全局里定义的a
    a = 20  # 现在的a是全局变量了
    return a + 100


print(apply)
print('a past:', a)
fun()
print('a now:', a)
