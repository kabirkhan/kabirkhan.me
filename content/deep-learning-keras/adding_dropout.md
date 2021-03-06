Title: Adding Dropout    
Slug: adding_dropout    
Summary: How to add dropout to a neural network model in Python.    
Date: 2018-01-25 12:00  
Category: Deep Learning - Keras  
Tags: Basics
Authors: Kabir Khan

# What is Dropout?

Dropout is a state-of-the-art regularization technique for deep neural networks. It is a mask over a particular layer of a network to remove certain nodes and their connections from a training pass.

[Original Dropout Paper](http://www.cs.toronto.edu/~rsalakhu/papers/srivastava14a.pdf)

### **e.g.** 

If you apply dropout with a probability of `0.2` to a layer, then for each node in that layer there is `0.2` chance of removing it from training. 

For each iteration, a different subset of your network is trained creating an ensemble effect. This technique is shown to reduce overfitting and is used in most network architectures today.

<img src="http://cs231n.github.io/assets/nn2/dropout.jpeg">
> Image Source: http://cs231n.github.io/neural-networks-2/#reg

## Packages


```python
# Load libraries
import numpy as np
from keras.datasets import imdb
from keras.preprocessing.text import Tokenizer
from keras import models
from keras import layers

# Set random seed
np.random.seed(0)
```

## Load IMDB Movie Review Data


```python
# Set the number of features we want
number_of_features = 1000

# Load data and target vector from movie review data
(train_data, train_target), (test_data, test_target) = imdb.load_data(num_words=number_of_features)

# Convert movie review data to a one-hot encoded feature matrix
tokenizer = Tokenizer(num_words=number_of_features)
train_features = tokenizer.sequences_to_matrix(train_data, mode='binary')
test_features = tokenizer.sequences_to_matrix(test_data, mode='binary')
```

## Functions to train and evaluate model


```python
def train_and_evaluate(model):
    # Compile neural network
    model.compile(loss='binary_crossentropy', # Cross-entropy
                optimizer='adam', # Adam Optimizer
                metrics=['accuracy']) # Accuracy performance metric
    
    # Train neural network
    history = model.fit(train_features, # Features
                      train_target, # Target vector
                      epochs=10, # Number of epochs
                      verbose=1, # No output
                      batch_size=100, # Number of observations per batch
                      validation_data=(test_features, test_target)) # Data for evaluation
    
    return history
```

## Neural Network Architecture

We'll start with a standard network architecture that doesn't use Dropout


```python
# Start neural network
network = models.Sequential()

# Add fully connected layer with a ReLU activation function for input layer
network.add(layers.Dense(units=16, activation='relu', input_shape=(number_of_features,)))

# Add fully connected layer with a ReLU activation function
network.add(layers.Dense(units=16, activation='relu'))

# Add fully connected layer with a sigmoid activation function
network.add(layers.Dense(units=1, activation='sigmoid'))
```


```python
train_and_evaluate(network)
```

    Train on 25000 samples, validate on 25000 samples
    Epoch 1/10
    25000/25000 [==============================] - 2s 62us/step - loss: 0.4306 - acc: 0.7998 - val_loss: 0.3347 - val_acc: 0.8580
    Epoch 2/10
    25000/25000 [==============================] - 1s 42us/step - loss: 0.3220 - acc: 0.8655 - val_loss: 0.3288 - val_acc: 0.8596
    Epoch 3/10
    25000/25000 [==============================] - 1s 44us/step - loss: 0.3100 - acc: 0.8716 - val_loss: 0.3346 - val_acc: 0.8578
    Epoch 4/10
    25000/25000 [==============================] - 1s 45us/step - loss: 0.3020 - acc: 0.8742 - val_loss: 0.3273 - val_acc: 0.8596
    Epoch 5/10
    25000/25000 [==============================] - 1s 42us/step - loss: 0.2910 - acc: 0.8778 - val_loss: 0.3318 - val_acc: 0.8575
    Epoch 6/10
    25000/25000 [==============================] - 1s 45us/step - loss: 0.2773 - acc: 0.8852 - val_loss: 0.3311 - val_acc: 0.8572
    Epoch 7/10
    25000/25000 [==============================] - 1s 45us/step - loss: 0.2638 - acc: 0.8940 - val_loss: 0.3382 - val_acc: 0.8552
    Epoch 8/10
    25000/25000 [==============================] - 1s 45us/step - loss: 0.2482 - acc: 0.8985 - val_loss: 0.3533 - val_acc: 0.8511
    Epoch 9/10
    25000/25000 [==============================] - 1s 59us/step - loss: 0.2325 - acc: 0.9069 - val_loss: 0.3646 - val_acc: 0.8490
    Epoch 10/10
    25000/25000 [==============================] - 1s 45us/step - loss: 0.2140 - acc: 0.9160 - val_loss: 0.3940 - val_acc: 0.8450





    <keras.callbacks.History at 0x11643df98>



## Neural Network Architecture With Dropout

In Keras, we can implement dropout using the convenient `Dropout` layer into our network architecture. Each `Dropout` layer will drop a user-defined hyperparameter of units in the previous layer every batch. 

Remember in Keras the input layer is assumed to be the first layer and not added using the `add` method. Therefore, if we want to add dropout to the input layer, the layer we add in our model is a dropout layer. This layer contains both the proportion of the input layer's units to drop `0.2` and `input_shape` defining the shape of the observation data. We add `Dropout` layers with `0.5` to each subsequent layer.


```python
# Start neural network with dropout
network_dropout = models.Sequential()

# Add a dropout layer for input layer
network_dropout.add(layers.Dropout(0.2, input_shape=(number_of_features,)))

# Add fully connected layer with a ReLU activation function
network_dropout.add(layers.Dense(units=16, activation='relu'))

# Add a dropout layer for previous hidden layer
network_dropout.add(layers.Dropout(0.5))

# Add fully connected layer with a ReLU activation function
network_dropout.add(layers.Dense(units=16, activation='relu'))

# Add a dropout layer for previous hidden layer
network_dropout.add(layers.Dropout(0.5))

# Add fully connected layer with a sigmoid activation function
network_dropout.add(layers.Dense(units=1, activation='sigmoid'))
```


```python
train_and_evaluate(network_dropout)
```

    Train on 25000 samples, validate on 25000 samples
    Epoch 1/10
    25000/25000 [==============================] - 2s 78us/step - loss: 0.6368 - acc: 0.6172 - val_loss: 0.4679 - val_acc: 0.8290
    Epoch 2/10
    25000/25000 [==============================] - 1s 54us/step - loss: 0.4896 - acc: 0.7714 - val_loss: 0.3674 - val_acc: 0.8484
    Epoch 3/10
    25000/25000 [==============================] - 2s 63us/step - loss: 0.4348 - acc: 0.8100 - val_loss: 0.3393 - val_acc: 0.8579
    Epoch 4/10
    25000/25000 [==============================] - 2s 71us/step - loss: 0.4130 - acc: 0.8181 - val_loss: 0.3261 - val_acc: 0.8603
    Epoch 5/10
    25000/25000 [==============================] - 1s 57us/step - loss: 0.4034 - acc: 0.8222 - val_loss: 0.3214 - val_acc: 0.8623
    Epoch 6/10
    25000/25000 [==============================] - 2s 83us/step - loss: 0.3980 - acc: 0.8232 - val_loss: 0.3262 - val_acc: 0.8612
    Epoch 7/10
    25000/25000 [==============================] - 1s 56us/step - loss: 0.3926 - acc: 0.8284 - val_loss: 0.3220 - val_acc: 0.8607
    Epoch 8/10
    25000/25000 [==============================] - 1s 54us/step - loss: 0.3889 - acc: 0.8263 - val_loss: 0.3233 - val_acc: 0.8588
    Epoch 9/10
    25000/25000 [==============================] - 1s 56us/step - loss: 0.3814 - acc: 0.8350 - val_loss: 0.3216 - val_acc: 0.8584
    Epoch 10/10
    25000/25000 [==============================] - 2s 66us/step - loss: 0.3804 - acc: 0.8323 - val_loss: 0.3209 - val_acc: 0.8604





    <keras.callbacks.History at 0x1170d7fd0>



## Results

We can see that without dropout we'll get a much higher training accuracy over 10 epochs. However, our validation accuracy starts to decline. With dropout, our network's training accuracy regularizes and we have a consistently higher validation accuracy.

**Validation Accuracy Comparison**:
    <table>
        <tr>
            <td></td>
            <th> **Network** </th>
            <th> **Network With Dropout** </th>
        </tr>
        <tr>
            <td> **User stayed in the course** </td>
            <td> 84.5% </td>
            <td> 86.04% </td>
        </tr>
    </table>
