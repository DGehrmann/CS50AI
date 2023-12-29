CS50AI - Introduction to Artificial Intelligence with Python
Lesson 5 - Project 5 - TRAFFIC

I started testing my model with a setup of one convolutional layer using 32 filters and a 3x3 kernel, one pooling layer of size 2x2, one dropout layer with dropout rate 0.5 and one hidden layer with 64 units. This setup resulted in very low accuracies and high losses:

- Accuracy of training set: 0.056
- Loss of training set: 3.50
- Accuracy of test set: 0.056
- Loss of test set: 3.49#

First, I increased the numbers of convolutional (32 filters, 3x3) and pooling layers (2x2):

- 2 convolutional and 2 pooling layers --> no significant changes
- 3 convolutional and 3 pooling layers --> significant increase of both accuracies (train: 0.858, test: 0.925) and decrease of losses (train: 0.457, test: 0.259).

Secondly, I tested different amounts of filters of the convolutional layers (16 and 48). With 48 layers, accuracy was slightly lower than with 32 filters (train: 0.828, test: 0.895). With 16 layers, accuracy decreased even more (train: 0.751, test: 0.816).

Next, I tried different filter sizes: 4x4 filter sizes decreased accuracy back to the level where I originally started from (e. g. the original setup). 2x2 filter size also resulted in a decrease of accuracy (train: 0.666, test: 0.777). I thus decided to continue with 3x3 filter size.

In a third step, I changed numbers and sizes of hidden layers.
I therefor increased the size of the one hidden layer continuously from 64 to 128, 256 and 512 units. Using 128 units, the accuracy increased slightly to 0.878 (train) and 0.906 (test). Using 256 units, this trend continued (train: 0.929, test: 0.938). Further increasing the amount of units did not change much anymore. 
Next, I increased the number of hidden layers (each using 256 units): Using 2 hidden layers, accuracy improved slightly (train: 0.947, test: 0.953). Adding a third and even a fourth layer, however, did not change much anymore.

Using the results so far, I changed my setup to:
2 convolutional layers (32 filters, 3x3) and 2 pooling layers (2x2), and added three hidden layers using 128 units.

Fourth, I variied dropout rate:
With the original dropout rate of 0.5, the results where as follows: accuracy train: 0.975, accuracy test: 0.978.
Increasing dropout rate to 0.6 resulted in a decrease of accuracy (train: 0.909, test: 0.931). Decreasing dropout rate to 0.3 increased accuracy to 0.974 (train) and 0.96 (test), reaching similar values as with the original value. Further decreasing dropout rate to 0.2 did not improve the situation. 
I also tested the same setup using hidden layers with 256 units. In this case, the best result was reached using dropout rate of 0.3 (train: 0.955, test: 0.956).

I then made 5 runs with each of the following two setups to ensure stability:

First setup: 
    - 2 convolutional layers with 32 filters, 3x3 and two pooling layers 2x2
    - 3 hidden layers, 128 units
    - dropout rate: 0.5

Second setup:
    - 2 convolutional layers with 32 filters, 3x3 and two pooling layers 2x2
    - 3 hidden layers, 256 units
    - dropout rate: 0.3

Both setups performed well, reaching training accuracies in a similar range between 0.95 and 0.98, test accuracies in a range between 0.93 to 0.98, training losses between 0.09 and 0.17 and test losses between 0.12 and 0.26.
