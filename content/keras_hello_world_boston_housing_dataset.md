Title: Keras "Hello World" Example for Regression
Date: 2018-10-18 12:30
Modified: 2018-10-18 12:30
Category: Keras
Tags: python, deep learning, keras, neural networks
Slug: keras_hello_world_boston_housing_dataset
Authors: Sam Zuckerman
Summary: A "Hello World" example for a neural network utilizing Keras for Regression. 


The following example uses the [Boston Housing dataset](https://www.kaggle.com/c/boston-housing) to predict the median value of homes in a specific Boston suburb in 1978.

We're using this dataset since:
 1. It's well known
 2. It's included in Keras so you don't need to download any other dependencies.
 
# Getting Keras

If you don't already have Keras and Scikit-Learn installed, you can download both using pip:

```python 
pip install keras
pip install scikit-learn
```

If you need additional help, you can check out [the Keras documentation](https://keras.io/). 

# Loading Packages

We're going to need the following:

```python
from keras.datasets import boston_housing
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler
import numpy as np
            
(X_train, y_train), (X_test, y_test) = boston_housing.load_data()
```

Neural networks work best when the data is normalized. The network would get confused with our data when comparing small and big numbers of different units (like tax rates and non-business acres). 

```python

scalerX = MinMaxScaler(feature_range(0,1))
scalerY = MinMaxScaler(feature_range(0,1))
   
scaled_training_X = scalerX.fit_transform(X_train)
scaled_testing_X = scalerX.fit_transform(X_test)
    
scaled_training_y = scalerY.fit_transform(y_train.reshape(-1, 1))
scaled_testing_y = scalerY.fit_transform(y_test.reshape(-1, 1))
```




    
We're going to create a sequential neural network, dense layers and 32 nodes for each layer.

The two important parts in the following code block are `input_dim=13` and `Dense(1, activation='linear')`.

The `input_dim` maps to the number of columns in the dataset (we have 13 variables we're using to predict) and the last layer should have one node (hence, `Dense(1)`) to show that we're predicting one value.

```python
model = Sequential()
model.add(Dense(32, input_dim=13, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))
model.compile(loss='mse', optimizer='adam')
```

The above model has four layers with two hidden layers where each of the layers are dense. Dense means that every node in one layer maps to every node in the next layer. This way as information passes through the network it will make linear transformations of the data with information of 'lower importance' being pushed closer to zero.

We're basing our loss on MSE or [Mean Squared Error](https://en.wikipedia.org/wiki/Mean_squared_error), a standard regression loss metric (i.e. how 'off' was each prediction from the real value). We're also using the [ADAM optimizer](https://en.wikipedia.org/wiki/Stochastic_gradient_descent#Adam) to update the network weights. The more finely tuned the network weights are, the better fit the model will be.

Also, there's discussion as to how many layers and nodes should be included in a network and choosing the right numbers is more of an art than a science. The above could have just as easily been:

```python
model = Sequential()
model.add(Dense(4, input_dim=13, activation='relu'))
model.add(Dense(1, activation='linear'))
model.compile(loss='mse', optimizer='adam')
```
 
But with less nodes and layers, we risk underfitting the network.

# Fitting and Evaluating the Model

Fitting a model in Keras is easy; just run the `fit` method:

```python
model.fit(scaled_training_X, scaled_training_y, shuffle=True, epochs=100, verbose=1)
```

An epoch is a "run" through the data to optimize the weights. We're choosing 100 epochs since it doesn't take that long to run and we need a good number of passes through the data to allow the optimizer to update the weights accordingly. 
     
Here's the output since we had `verbose` set to `1` (showing the first 10 and last 10 epochs):

    Epoch 1/100
    404/404 [==============================] - 0s 47us/step - loss: 0.0358
    Epoch 2/100
    404/404 [==============================] - 0s 48us/step - loss: 0.0188
    Epoch 3/100
    404/404 [==============================] - 0s 47us/step - loss: 0.0159
    Epoch 4/100
    404/404 [==============================] - 0s 40us/step - loss: 0.0139
    Epoch 5/100
    404/404 [==============================] - 0s 43us/step - loss: 0.0125
    Epoch 6/100
    404/404 [==============================] - 0s 51us/step - loss: 0.0113
    Epoch 7/100
    404/404 [==============================] - 0s 32us/step - loss: 0.0105
    Epoch 8/100
    404/404 [==============================] - 0s 40us/step - loss: 0.0099
    Epoch 9/100
    404/404 [==============================] - 0s 49us/step - loss: 0.0095
    Epoch 10/100
    404/404 [==============================] - 0s 36us/step - loss: 0.0090
    ...
    Epoch 90/100
    404/404 [==============================] - 0s 52us/step - loss: 0.0040
    Epoch 91/100
    404/404 [==============================] - 0s 48us/step - loss: 0.0041
    Epoch 92/100
    404/404 [==============================] - 0s 48us/step - loss: 0.0040
    Epoch 93/100
    404/404 [==============================] - 0s 52us/step - loss: 0.0040
    Epoch 94/100
    404/404 [==============================] - 0s 31us/step - loss: 0.0040
    Epoch 95/100
    404/404 [==============================] - 0s 42us/step - loss: 0.0040
    Epoch 96/100
    404/404 [==============================] - 0s 48us/step - loss: 0.0041
    Epoch 97/100
    404/404 [==============================] - 0s 38us/step - loss: 0.0040
    Epoch 98/100
    404/404 [==============================] - 0s 49us/step - loss: 0.0039
    Epoch 99/100
    404/404 [==============================] - 0s 49us/step - loss: 0.0039
    Epoch 100/100
    404/404 [==============================] - 0s 34us/step - loss: 0.0039
        
And to evaluate:    

```python
mse = model.evaluate(scaled_testing_X, scaled_testing_y)
```    
    
Since used mse as a loss function above, when we use the `evaluate` method, we'll get mse returned.

> Note: We are evaluating with the test data and will also be predicting with the test data as well. Usually when preparing a model for production one has a breakdown of training, testing and validation data sets for model evaluation. We are merely using the testing data to show how the model performs on unseen data.  

    
Output:
```python
>>>0.16640686755086861 
```

# So What Does This Mean?

Since we have the mse, we want to know how "off" our predictions are. The units are currently (scaled_dollars)^2 which isn't so useful. Therefore we have to 'untransform' it.

```python
result = np.sqrt(mse)
true_result = scalerY.inverse_transform([result])
```

Output:
```python
array([[ 26.80030564]])
```

__Note:__ you might get different slightly results based on rounding issues .

This shows that across all the 

def get_results(x):
	pred = model.predict(scaled_testing_X[x:x+1])
	return	y_test[x], scalerY.inverse_transform(pred)[0][0]





    scalerX = MinMaxScaler(feature_range=(0,1))
    scalerY = MinMaxScaler(feature_range=(0,1))
    
    
    scaled_training_X = scalerX.fit_transform(X_train)
    scaled_testing_X = scalerX.fit_transform(X_test)
    
    
    scaled_training_y = scalerY.fit_transform(y_train.reshape(-1, 1))
    scaled_testing_y = scalerY.fit_transform(y_test.reshape(-1, 1))
    
