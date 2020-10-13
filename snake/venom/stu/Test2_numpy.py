import numpy as np
import matplotlib.pyplot as plt

# 1 换行命令
text = 'This is my first test. This is the second line. This the third'
print(text)

text2 = 'This is my first test.\nThis is the second line.\nThis the third line'
print(text2)

# 2 open 读文件方式
"""
使用open能够打开一个文件,open的第一个参数为文件名和路径 'my file.txt',第二个参数为将要以什么方式打开它
比如w为可写方式
如果计算机没有找到my file.txt 这个文件,w方式能够创建一个新的文件,并命名为my file.txt
"""
my_file = open('my file.txt', 'w')  # 用法 open('文件名','形式') 其中形式有 w write, r read
my_file.write(text)  # 该语句会写入先前定义好的text
my_file.close()  # 关闭文件

# 3 tab 对齐
# 使用 \t 能够达到tab对齐的效果
text = '\tThis is my first test.\n\tThis is the second line.\n\tThis is the third line'
print(text)  # 延伸 使用\t对齐

print('3--------------------------')

# 4 给文件增加内容
append_text = '\nthis is append file'  # 为这行文字提取空行 \n
my_file = open('my file2.txt', 'a')  # a=append 以增加内容的形式打开
my_file.write(append_text)
my_file.close()

# 5 读取文件内容 file.read()
file = open('my file2.txt', 'r')
content = file.read()
print(content)
print('5-------------------------')
# 6 按行读取 file.readline()
file = open('my file2.txt', 'r')
content = file.readline()  # 读取第一行
print(content)

print('6------------------')
# 7 读取所有行 file.readlines()
"""
如果想要读取所有行,并可以使用像for一样的迭代器这些行结果,我们可以使用file.readlines()
将每一行的结果存储在list中,方便以后迭代
"""
file = open('my file2.txt', 'r')
content = file.readlines()  # python_list 形式
print(content)
# 之后如果使用for来迭代输出: for item in content: print(item)

for item in content:
    print(item)
