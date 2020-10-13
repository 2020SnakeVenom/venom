import tensorflow as tf
import numpy as np

v = np.__version__
c = tf.__version__
print(c, v)
"""
神经网络在干嘛
拟合曲线

机器学习 其实就是让电脑不断的尝试模拟已知的数据
他能知道自己你和的数据离真实的数据差距有多远
然后不断地改进自己拟合的参数 提高拟合的相似度

拟合参数

因为TensorFlow是采用数据流图 data flow graphs来计算
首先我们得创建一个数据流流图
然后再将我们的数据 数据以张量tensor的形式存在
放在数据流图中计算
节点nodes在图中表示数学操作
图中的线edges则表示在节点间相互联系的多维数据数组
即张量tensor
训练模型时tensor会不断的从数据流图中的一个节点flow到另一个节点
这就是tensorflow名字的由来

tensor张量意义
张量 tensor 
张量有多种 零阶张量为纯量 或标量scalar也就是一个数值
比如 [1]*一阶张量为 向量 vector
比如一维[1,2,3]*
二阶张量为矩阵matrix
比如二维的[[1,2,3],[4,5,6],[7,8,9]]
"""
# 1 创建数据
# 需要加载tensorflow 和numpy两个模块,并且使用numpy来创建我们的数据
# create data
x_data = np.random.rand(100).astype(np.float32)
y_data = x_data * 0.1 + 0.3
# 接着 我们用tf.Variable来创建描述y的参数,我们可以把y_data=x_data*0.1+0.3
# 想象成 y=Weights*x+biases
# 然后神经网络也就是学者把weights变成0.1 biases变成0.3

# 2 搭建模型
Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
# Weights = tf.Variable(tf.random_uniform_initializer())
biases = tf.Variable(tf.zeros([1]))
y = Weights * x_data + biases

# 3 计算误差
#  接着就是计算y和y_data的误差
loss = tf.reduce_mean(tf.square(y - y_data))

# 4 传播误差
# 反向传递误差的工作就交给optimizer了,我们使用的误差传递方法是梯度下降法
# GradientDescent让后我们使用optimizer来进行参数的更新
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

# 5 训练
# 在使用这个结构之前,我们必须先初始化所有之前定义的Variable,所以这一步是很重要的
init = tf.global_variables_initializer()
# 接着 我们再创建会话 session
# 用Session来run每一次training的数据,逐步提升神经网络的预测准确性
sess = tf.Session()
sess.run(init)  # very important

for step in range(201):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(Weights), sess.run(biases))
