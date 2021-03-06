

# coding: utf-8


# how-to:
# ~$ source ~/tensorflow/bin/activate


# In[22]:


import xlwt
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD
from numpy.linalg import matrix_rank
from PIL import Image
import matplotlib.pyplot as plt
import scipy.misc
import numpy as np
import random




# In[23]:


def low_rank_approx(A, r):
    U,D,V = np.linalg.svd(A, full_matrices=False)
    B = np.zeros((len(U), len(V)))
    for i in range(r):
        B += D[i] * np.outer(U.T[i], V[i])
    return B


def batch_mult(A,V):
    W=[]
    for v in V:
        W.append(np.dot(A,v))
    return np.asarray(W)


def print_matrix(A):
    print()
    for row in A:
        for val in row:
            print(("%.2f " % val), end=' ')
        print()
    print()


def make_matrix(type, size):
    if type == "sym":
        A = [[i+j for i in range(size)] for j in range(size)]
        for i in range(size):
            for j in range(i, size):
                A[i][j] = np.random.randint(0, 10)
                A[j][i] = A[i][j]
    return A


def closestPower(n):
    i = 1
    while(1):
        thisDiff =  abs(n - (2**i))
        lastDiff = abs(n - (2**(i-1)))
        if thisDiff > lastDiff:
            return i - 2
        i += 1


def testData(rank, n, A):
    #A = np.random.rand(n, n)
    print("Called with RANK = " + str(rank) + ", SIZE = " + str(n))


    B = low_rank_approx(A, rank)




    nTrain=10000
    nTest=1000
    
    #training data
    x_train = np.random.rand(nTrain, n)
    y_train = batch_mult(A,x_train)
    
    #test data
    x_test = np.random.rand(nTest, n)
    y_test = batch_mult(A,x_test)
    
    power = closestPower(n)
    #build neural net
    model = Sequential()
    model.add(Dense(n, input_dim=n, bias=False, init='he_normal'))
    model.add(Activation('linear'))
    
    model.add(Dense(n, bias=False, init='he_normal'))
    model.add(Activation('linear'))


    # model.add(Dense(power, bias=False, init='he_normal'))
    # model.add(Activation('linear'))
    model.add(Dense(n-1, bias=False, init='he_normal'))
    model.add(Activation('linear'))
    # model.add(Dense(power/4, bias=False, init='he_normal'))
    # model.add(Activation('linear'))


    model.add(Dense(rank,bias=False, init='he_normal'))
    model.add(Activation('linear'))

    model.add(Dense(n-1, bias=False, init='he_normal'))
    model.add(Activation('linear'))
    model.add(Dense(n-1, bias=False, init='he_normal'))
    model.add(Activation('linear'))

    model.add(Dense(rank, bias=False, init='he_normal'))
    model.add(Activation('linear'))

    # model.add(Dense(power/4, bias=False, init='he_normal'))
    # model.add(Activation('linear'))
    # model.add(Dense(power/2, bias=False, init='he_normal'))
    # model.add(Activation('linear'))
    # model.add(Dense(power, bias=False, init='he_normal'))
    # model.add(Activation('linear'))


    model.add(Dense(n, bias=False, init='he_normal'))
    model.add(Activation('linear'))
    
    model.compile(loss='mean_squared_error',optimizer='adam', metrics=["accuracy"])
    
    
    #train the neural net using the training data
    history = model.fit(x_train, y_train, nb_epoch=30, batch_size=30,)

    plt.plot(history.history['loss'][1:])
    plt.show()
    plt.clf
    
    score = model.evaluate(x_test, y_test, batch_size=30)
    print('\n score: ', score)
    
    C=model.predict(np.identity(n))
    
    
    print('Dylan\'s errors (SVD): ', np.linalg.norm(A-B, 2)/np.linalg.norm(A, 2), np.linalg.norm( A-B, 'fro')/np.linalg.norm(A,'fro'))
    print('Dylan\'s errors (NN): ', np.linalg.norm(A-C.T, 2)/np.linalg.norm(A, 2), np.linalg.norm( A-C.T, 'fro')/np.linalg.norm(A,'fro'))


                            
    rankC = matrix_rank(C)
    rankB = matrix_rank(B)
    rankA = matrix_rank(A)
    print("\nNN Rank is " + str(rankC))
    print("SVD Rank is " + str(rankB))
    print("Original Rank is " + str(rankA))
    
    # return abs(np.linalg.norm(A-B, 2)/np.linalg.norm(A, 2) - np.linalg.norm(A-C.T, 2)/np.linalg.norm(A, 2))
    return C




#    target matrix whose low-rank approximation we will learn


def doImage():
    k = 1
    fname = 'gates.jpeg'
    image = Image.open(fname).convert('L')
    arr = np.asarray(image)
    C = testData(k, len(arr), arr)
    B = low_rank_approx(arr, k)


    print((image.size))
    
    #<Bo>
    fig = plt.figure()
    a=fig.add_subplot(1,3,1)
    imgplot = plt.imshow(C.T, cmap='gray')
    a.set_title('NN')
    a=fig.add_subplot(1,3,2)
    imgplot = plt.imshow(B, cmap='gray')
    a.set_title('SVD')
    a=fig.add_subplot(1,3,3)
    imgplot=plt.imshow(arr, cmap='gray')
    a.set_title('Original')
    plt.show()






# plot(model, to_file='model.png')


def doRandom(k):
    n = 10


    A = np.random.rand(n, n)
    # A = np.identity(n)
    first = testData(k, n, A)
    #second = testData(5, n, A)


    # print("\nORIGINAL:")
    # print_matrix(A)
    # print("FIRST:")
    # print_matrix(first.T)
#    print "SECOND:"
#    print_matrix(second.T)


    # print('Error for low rank: ', np.linalg.norm(A-first.T, 2)/np.linalg.norm(A, 2), np.linalg.norm( A-first.T, 'fro')/np.linalg.norm(A,'fro'))
#    print 'Error for high rank: ', np.linalg.norm(A-second.T, 2)/np.linalg.norm(A, 2), np.linalg.norm( A-second.T, 'fro')/np.linalg.norm(A,'fro')
    return first



def graphRandom():
    n = 10
    k = 5
    arr = np.random.rand(n, n)
    #arr = [[0, 1, 2, 3, 4], [1, 2, 3, 4, 5], [0, 0, 1, 0, 0], [5, 4, 3, 2, 1], [4, 3, 2, 1, 0]]
    arr = make_matrix('sym', n)
    arr = np.identity(n)
    for i in range(n):
        arr[i][i] = random.random()
    C = testData(k, n, arr)
    # B = testData(1, n, arr)
    B = low_rank_approx(arr, k)
    
    #<Bo>
    fig = plt.figure()
    a=fig.add_subplot(1,3,1)
    imgplot = plt.imshow(C.T, cmap='gray')
    a.set_title('NN')
    a=fig.add_subplot(1,3,2)
    imgplot = plt.imshow(B, cmap='gray')
    a.set_title('SVD')
    a=fig.add_subplot(1,3,3)
    imgplot=plt.imshow(arr, cmap='gray')
    a.set_title('Original')
    plt.show()



graphRandom()
# doImage()
# doRandom(i)








