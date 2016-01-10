import numpy as np

import functions as f
import layers as l
import utils as u


class NeuralNetwork():
    def __init__(self, layers, loss_func):
        assert len(layers) > 0

        assert isinstance(layers[0], l.InputLayer)
        self.input_layer = layers[0]

        assert isinstance(layers[-1], l.FullyConnectedLayer)
        self.output_layer = layers[-1]

        self.layers = [(prev_layer, layer) for prev_layer, layer in zip(layers[:-1], layers[1:])]

        self.loss_func = loss_func

        self.weights = dict()
        self.biases = dict()
        for prev_layer, layer in self.layers:
            layer.connect_to(prev_layer)

            prev_layer_nout = prev_layer.depth * prev_layer.height * prev_layer.width
            layer_nin       = prev_layer_nout
            layer_nout      = layer.depth      * layer.height      * layer.width
            if type(layer) is l.FullyConnectedLayer:
                w_shape = (layer_nout, prev_layer_nout)
                b_shape = (layer_nout, 1)
            elif type(layer) is l.ConvolutionalLayer:
                w_shape = (layer.depth, prev_layer.depth, layer.kernel_size, layer.kernel_size)
                b_shape = (layer.depth, 1)
            elif type(layer) is l.MaxPoolingLayer:
                w_shape = (0)
                b_shape = (0)
            else:
                raise NotImplementedError
            self.weights[layer] = u.glorot_uniform(w_shape, layer_nin, layer_nout).astype(np.float32)
            self.biases[layer]  = np.zeros(b_shape).astype(np.float32)

    def feedforward(self, x):
        self.input_layer.z = x
        self.input_layer.a = x

        for prev_layer, layer in self.layers:
            w = self.weights[layer]
            b = self.biases[layer]
            layer.feedforward(prev_layer, w, b)

    def backpropagate(self, batch, optimizer):
        der_weights = {layer: np.zeros_like(self.weights[layer]) for _, layer in self.layers}
        der_biases  = {layer: np.zeros_like(self.biases[layer])  for _, layer in self.layers}

        for x, y in batch:
            self.feedforward(x)

            # propagate the error backward
            loss = self.loss_func(self.output_layer.a, y)
            delta = loss * self.output_layer.der_act_func(self.output_layer.z, y)
            for prev_layer, layer in reversed(self.layers):
                w = self.weights[layer]
                der_w, der_b, delta = layer.backpropagate(prev_layer, w, delta)
                der_weights[layer] += der_w
                der_biases[layer]  += der_b

        # update weights and biases
        if optimizer["type"] == "adadelta":
            rho = 0.95
            eps = 1e-8
            gsum_weights = {layer: 0 for _, layer in self.layers}
            xsum_weights = {layer: 0 for _, layer in self.layers}
            gsum_biases  = {layer: 0 for _, layer in self.layers}
            xsum_biases  = {layer: 0 for _, layer in self.layers}
        for _, layer in self.layers:
            gw = der_weights[layer]/len(batch)
            gb = der_biases[layer] /len(batch)

            if optimizer["type"] == "SGD":
                self.weights[layer] += -optimizer["eta"]*gw
                self.biases[layer]  += -optimizer["eta"]*gb
            elif optimizer["type"] == "adadelta":
                gsum_weights[layer] = rho*gsum_weights[layer] + (1-rho)*gw*gw
                dx = -np.sqrt((xsum_weights[layer]+eps)/(gsum_weights[layer]+eps)) * gw
                self.weights[layer] += dx
                xsum_weights[layer] = rho*xsum_weights[layer] + (1-rho)*dx*dx

                gsum_biases[layer]  = rho*gsum_biases[layer]  + (1-rho)*gb*gb
                dx = -np.sqrt((xsum_biases[layer] +eps)/(gsum_biases[layer] +eps)) * gb
                self.biases[layer]  += dx
                xsum_biases[layer]  = rho*xsum_biases[layer]  + (1-rho)*dx*dx
            else:
                raise NotImplementedError


def train(net, optimizer, num_epochs, batch_size, trn_set, vld_set=None):
    assert isinstance(net, NeuralNetwork)
    assert num_epochs > 0
    assert batch_size > 0

    trn_x, trn_y = trn_set
    inputs = [(x, y) for x, y in zip(trn_x, trn_y)]

    for i in range(num_epochs):
        np.random.shuffle(inputs)

        # divide input observations into batches
        batches = [inputs[j:j+batch_size] for j in range(0, len(inputs), batch_size)]
        for j, batch in enumerate(batches):
            net.backpropagate(batch, optimizer)
            u.print("Epoch %02d %s [%d/%d batches]" % (i+1, u.bar(j+1, len(batches)), j+1, len(batches)), override=True)

        if vld_set:
            # test the net at the end of each epoch
            u.print("Epoch %02d %s [%d/%d batches] > Testing..." % (i+1, u.bar(j+1, len(batches)), j+1, len(batches)), override=True)
            accuracy = test(net, vld_set)
            u.print("Epoch %02d %s [%d/%d batches] > Accuracy: %0.2f%%" % (i+1, u.bar(j+1, len(batches)), j+1, len(batches), accuracy*100), override=True)
        u.print()

def test(net, tst_set):
    assert isinstance(net, NeuralNetwork)

    tst_x, tst_y = tst_set
    tests = [(x, y) for x, y in zip(tst_x, tst_y)]

    accuracy = 0
    for x, y in tests:
        net.feedforward(x)
        if np.argmax(net.output_layer.a) == np.argmax(y):
            accuracy += 1
    accuracy /= len(tests)
    return accuracy
