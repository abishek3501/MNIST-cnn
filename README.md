# MNIST-cnn
This repository contains a Python implementation of a neural network with convolutional and polling layers. The purpose of this project was to correctly implement backpropagation on convolutional networks, and the code here provided could be useful only for educational purposes. To demonstrate the correctness of our network we tested it on the well-known [MNIST](http://yann.lecun.com/exdb/mnist/) data set.

Alessandro and Francesco


## Prerequisites
The code uses the [NumPy](http://www.numpy.org/) and [SciPy](https://www.scipy.org/) libraries. Install the required dependencies with:
```
pip3 install numpy scipy
```

Then, download the MNIST data set (four `.gz` archives, see link above) and decompress it:
```
~ ➤ cd Downloads
Downloads ➤ pwd
/Users/fcagnin/Downloads
Downloads ➤ ls
t10k-images-idx3-ubyte.gz  t10k-labels-idx1-ubyte.gz  train-images-idx3-ubyte.gz train-labels-idx1-ubyte.gz
Downloads ➤ gzip -d *
Downloads ➤ ls
t10k-images-idx3-ubyte  t10k-labels-idx1-ubyte  train-images-idx3-ubyte train-labels-idx1-ubyte
```


## Usage
Convert the downloaded data set into the more convenient NPZ binary data format using the function `build_mnist_npz()` from `utils.py`:
```
MNIST-cnn ➤ ls
README.md src
MNIST-cnn ➤ cd src
src ➤ ls
examples.py  functions.py layers.py    network.py   utils.py
src ➤ python3 -q
>>> import utils
>>> utils.build_mnist_npz('/Users/fcagnin/Downloads')
>>> exit()
src ➤ file mnist.npz
mnist.npz: Zip archive data, at least v2.0 to extract
```

Run any of the included examples:
```
src ➤ python3 examples.py mnist.npz fcl01
Loading 'mnist.npz'...
Loading 'fcl01'...
def fcl01():  # 91.75%
    net = n.NeuralNetwork([
        l.InputLayer(height=28, width=28),
        l.FullyConnectedLayer(height=10, act_func=f.softmax)
    ], f.log_likelihood)
    optimizer = {"type": "SGD", "eta": 0.1}
    num_epochs = 1
    batch_size = 10
    return net, optimizer, num_epochs, batch_size
Training NN...
Epoch 01 [==========] [6000/6000 batches] > Accuracy: 91.75%
```


## License
The MIT License (MIT)

Copyright (c) 2015-2016 Alessandro Torcinovich, Francesco Cagnin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
