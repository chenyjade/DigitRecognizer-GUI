# -*- coding:utf-8 -*-  
import network
import mnist_loader
from PIL import Image
import numpy as np
net = network.Network([784, 50, 10])
training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
#print (np.reshape(int(training_data[2][0]),(28,28)))
net.SGD(training_data, 30, 10, 3.0, test_data=test_data)
#print(net.predict('sample.png'))
net.saveModel()