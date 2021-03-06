from math import e, tanh, exp
from mind.dtypes import *
import matplotlib.pyplot as plt
import matplotlib.style as stl
from random import random
stl.use('classic')

# Neural Network loss functions
# Note: While adding any new function add its derivative under the der == True clause


def l1_loss(label, prediction, der=False):
    if der:
        return (label - prediction)/abs(label - prediction)
    else:
        return abs(label - prediction)


def l2_loss(label, prediction, der=False):
    if der:
        return 2*(label - prediction)
    else:
        return (label - prediction)**2


# Neural Network activation functions.
# Note: While adding any new function add its derivative under the der == True clause.


def re_l_u(x, a=0, der=False):
    if der:
        if x > 0:
            return 1
        else:
            return a
    else:
        if x > 0:
            return x
        else:
            return a * x


def sigmoid(x, der=False):
    ret = e ** x / (e ** x + 1)
    if der:
        return ret * (1 - ret)
    return ret


def tan_h(x, der=False):
    if der:
        return 1 - tanh(x) ** 2
    return tanh(x)


def linear(x, der=False):
    if der:
        return 1
    return x


def soft_max(x=[], der=False):
    ret = []
    m = max(x)
    exp_sum = 0
    for i in x:
        ret += [exp(i)]
        exp_sum += exp(i - m)
    for i in range(len(ret)):
        ret[i] = ret[i] / exp_sum
    if der:
        for i in range(len(ret)):
            ret[i] = ret[i] * (1 - ret[i])
    return Vector(ret)


# Layer and NeuralNet classes


class Layer(object):
    def __init__(self, size=0, activation=linear, rem=0):
        self.body = Vector(length=size)
        self.activation = activation
        self.rems = []
        for i in range(rem):
            self.rems += [Vector(length=size)]

    def __repr__(self):
        ret = 'Layer Vector:' + self.body.__repr__() + '\n'
        ret += 'Activation function:' + self.activation.__name__ + '\n'
        if len(self.rems):
            ret += 'Recurrent Memory Vector(s):\n'
            for i in range(len(self.rems)):
                ret += ' ' * 13 + self.rems[i].__repr__() + '\n'
        return ret

    def num_inputs(self):
        return len(self.body)

    def get_value(self, body=[]):
        body = Vector(body)
        a = len(self.rems)
        if self.activation is soft_max:
            self.body = self.activation(body)
        else:
            self.body = body.apply(self.activation)
        if a:
            self.rems = [self.body] + self.rems[:-1]

    def all_nodes(self):
        ret = Vector()
        ret = ret.join(self.body)
        for i in self.rems:
            ret = ret.join(i)
        return ret

    def num_outputs(self):
        return self.num_inputs() * (1 + len(self.rems))


class NeuralNet(object):
    def __init__(self):
        self.x = []
        self.w = []
        self.z = []
        self.b = []
        self.dw = []

    def __repr__(self):
        ret = 'Neural Network:-'
        ret += '\n'
        for i in range(self.depth()):
            ret += '\nLayer ' + str(i + 1) + ':-' + '\n' + self.x[i].__repr__()
        return ret

    def inputs(self):
        return self.x[0].num_inputs()

    def outputs(self):
        return self.x[-1].num_outputs()

    def depth(self):
        return len(self.x)

    def add_layer(self, size=0, activation=linear, rem=0):
        self.x += [Layer(size, activation, rem)]

    def build_connections(self):        
	self.w = []
	self.z = []	
	for i in range(self.depth() - 1):
            self.w += [Matrix(rows=self.x[i + 1].num_inputs(), columns=self.x[i].num_outputs())]
            self.z += [Vector(length=self.x[i + 1].num_inputs())]
            self.b += [Vector(length=self.x[i + 1].num_inputs())]
        self.dw = self.w

    def process(self, inp=[]):
        inp = Vector(inp)
        self.x[0].get_value(inp)
        for i in range(self.depth() - 1):
            self.z[i] = self.w[i] * self.x[i].all_nodes()
            self.x[i + 1].get_value(self.z[i] + self.b[i])
        return self.x[-1].body

    def show(self, col='g', tpe='-', width=1, style='dark_background'):
        stl.use(style)
        if self.w is []:
            self.build_connections()
        for i in range(self.depth() - 1):
            a = self.x[i].num_outputs()
            b = self.x[i + 1].num_inputs()
            for j in range(a):
                for k in range(b):
                    plt.plot([i, i+1], [j - a/2, k - b/2], tpe + col, linewidth=width)
        plt.xlabel('<------ LAYERS ------>')
        plt.ylabel('<------ NEURONS ------>')
        plt.title("<0>Neural Network structure diagram<0>")
        print(self)
        plt.show()

    def back_propagate(self, loss=[], sigma=1, mu=0.001, theta=2, previous_nets=False, momentum=False, bs=1):
        d = self.depth()
        for inp_layer in range(d - 1).__reversed__():
            a = self.x[inp_layer+1].activation
            inputs = self.w[inp_layer].columns()
            outputs = self.w[inp_layer].rows()
            next_loss = Vector(length=inputs)
            x = self.x[inp_layer].all_nodes()
            for otp in range(outputs):
                next_loss_partial = []
                for inp in range(inputs):
                    a_z_i = a(self.z[inp_layer][otp], der=True)
                    w_i_j = self.w[inp_layer][otp][inp]
                    i_j = x[inp]
                    di = loss[otp]
                    next_loss_partial += [di*di*di/(a_z_i*w_i_j + sigma) * 1/inputs]
                    if momentum:
                        self.dw[inp_layer][otp][inp] = (mu*di/(theta*a_z_i*i_j + sigma)) + (self.dw[inp_layer][otp][inp]/200)
                        self.w[inp_layer][otp][inp] += self.dw[inp_layer][otp][inp]
                    else:
                        self.w[inp_layer][otp][inp] += mu * bs * di/(theta*a_z_i*i_j + sigma)
                next_loss = next_loss + next_loss_partial
            loss = next_loss
        if previous_nets:
            return loss

    def train(self, features=[], labels=[], loss_function=l2_loss, mu=0.001, sigma=1, batch_size=1, theta=2, p_n=False, m=False, plot=True, epochs=1):
        if not len(self.w):
            self.build_connections()
        preds = []
        labes = []
        loss_plot = []
        for ep in range(epochs):
            n = len(labels)
            loss = Vector(length=self.outputs())
            for i in range(n):
                otp = self.process(features[i])
                for j in range(len(loss)):
                    loss[j] += loss_function(labels[i][j], otp[j], der=True)/batch_size
                if i % batch_size is 0 or i is n-1:
                    self.back_propagate(loss=loss, sigma=sigma, mu=mu, previous_nets=p_n, momentum=m, theta=theta, bs=batch_size)
                    if plot:
                        loss_plot += [sum(loss*loss)/len(loss)]
                        preds += [otp]
                        labes += [labels[i]]
                    loss = Vector(length=self.outputs())
        preds = transpose(preds)
        labes = transpose(labes)
        stl.use('dark_background')
        a = plt.subplot(211)
        plt.plot(loss_plot, '-r', linewidth=1)
        plt.title('Loss Curve')
        plt.ylabel('average error -->')
        plt.subplot(212, sharex=a)
        for i in range(len(preds)):
            plt.plot(preds[i], '-g', linewidth=1)
            plt.plot(labes[i], '-y', linewidth=1)
        plt.legend(["Prediction", "Label"])
        plt.xlabel("iterations (in " + str(batch_size) + "'s) -->")
        plt.show()







