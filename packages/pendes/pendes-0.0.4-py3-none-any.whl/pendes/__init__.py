def print1():
    pass

def print2a():
    s = """
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    # Reading Data
    data = pd.read_csv('headbrain.csv')
    print(data.shape)
    data.head()
    # Collecting X and Y
    X = data['Head Size(cm^3)'].values
    Y = data['Brain Weight(grams)'].values
    # Calculating coefficient

    # Mean X and Y
    mean_x = np.mean(X)
    mean_y = np.mean(Y)

    print(mean_x)
    print(mean_y)

    # Total number of values
    n = len(X)
    print(n)

    # Using the formula to calculate b1 and b0
    numer = 0
    denom = 0
    for i in range(n):
        numer += (X[i] - mean_x) * (Y[i] - mean_y)
        denom += (X[i] - mean_x) ** 2
    b1 = numer / denom
    b0 = mean_y - (b1 * mean_x)
    # Printing coefficients
    print("Coefficients")
    print(b1, b0)

    # Plotting Values and Regression Line

    max_x = np.max(X) + 100
    min_x = np.min(X) - 100

    # Calculating line values x and y
    x = np.linspace(min_x, max_x, 1000)
    y = b0 + b1 * x

    # Ploting Line
    plt.plot(x, y, color='#58b970', label='Regression Line')
    # Ploting Scatter Points
    plt.scatter(X, Y, c='#ef5423', label='Scatter Plot')

    plt.xlabel('Head Size in cm3')
    plt.ylabel('Brain Weight in grams')
    plt.legend()
    plt.show()

    # Calculating R2 Score
    ss_tot = 0
    ss_res = 0
    for i in range(n):
        y_pred = b0 + b1 * X[i]
        ss_tot += (Y[i] - mean_y) ** 2
        ss_res += (Y[i] - y_pred) ** 2
    r2 = 1 - (ss_res/ss_tot)
    print("R2 Score")
    print(r2)
    """
    return s

def print2b():
    s = """
    # Step1:importing all the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Step2:load dataset
df=pd.read_csv("housing_prices_SLR.csv",delimiter=',')
df.head()


x=df[['AREA']].values#feature Matrix
y=df.PRICE.values#Target Matrix
x[:5] #slicing
y[:5]


from sklearn.model_selection import train_test_split


x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=100)

print(x_train.shape)
print(x_test.shape)
print(x_train.shape)
print(x_test.shape)


from sklearn.linear_model import LinearRegression


lr_model= LinearRegression()


lr_model.fit(x_train,y_train)

print(lr_model.intercept_) 
print(lr_model.coef_)

from sklearn.metrics import r2_score
print(lr_model.predict(x_train))
print(lr_model.score(x_test,y_test))
print(lr_model.score(x_train,y_train))   
plt.scatter(x_train,y_train,c='red')
plt.scatter(x_test,y_test,c='blue')
plt.plot(x_train,lr_model.predict(x_train),c='green')
"""
    return s

def print3a():
    s = """
    import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = pd.read_csv('student.csv')
print(data.shape)
data.head()

math = data['Math'].values
read = data['Reading'].values
write = data['Writing'].values
print(math)



# Ploting the scores as scatter plot
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(math, read, write, color='r')
plt.legend()
plt.show()


m = len(math)
x0 = np.ones(m)
X = np.array([x0, math, read]).T



B = np.array([0, 0, 0])
Y = np.array(write)
print(Y)
alpha = 0.0001
def cost_function(X, Y, B):
    m = len(Y)
    J = np.sum((X.dot(B) - Y) ** 2)/(2 * m)
    return J
inital_cost = cost_function(X, Y, B)
print("Initial Cost")
print(inital_cost)
def gradient_descent(X, Y, B, alpha, iterations):
    cost_history = [0] * iterations
    m = len(Y)
    for iteration in range(iterations):
        h = X.dot(B)
        loss = h - Y
        gradient = X.T.dot(loss) / m
        B = B - alpha * gradient
    cost = cost_function(X, Y, B)
    cost_history[iteration] = cost
    return B, cost_history
newB, cost_history = gradient_descent(X, Y, B, alpha, 100000)
print("New Coefficients")
print(newB)
# Final Cost of new B
print("Final Cost")
print(cost_history[-1])

def r2_score(Y, Y_pred):
    mean_y = np.mean(Y)
    ss_tot = sum((Y - mean_y) ** 2)
    ss_res = sum((Y - Y_pred) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    return r2


Y_pred = X.dot(newB)

print("R2 Score")
print(r2_score(Y, Y_pred))
"""
    return s

def print3b():
    s = """
    import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("housing_prices.csv")

df.head()

df=df.iloc[:,[0,1,2,4]]

df.head()

x=df.iloc[:,:3].values
y=df.iloc[:,3].values

print(x[:5])
print(y[:5])

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=100)

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

from sklearn.linear_model import LinearRegression

model= LinearRegression()

model.fit(x_train,y_train)

print(model.intercept_) # (PRICE=(-4481.80028058845)+8.65903854)*AREA
print(model.coef_)#y=c+mx


print(model.score(x_train,y_train))
print(model.score(x_test,y_test))
"""
    return s

def print4a():
    s = """
    import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv('breast_cancer.csv')
df

df = df.iloc[:, :-1] 


df.head()

x = df.iloc[:, 2:].values 
x.shape
y = df.diagnosis.values

print(x[:2]) 

print(y[:5]) 

from sklearn.model_selection import train_test_split 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)

from sklearn.tree import DecisionTreeClassifier

dt_classifier = DecisionTreeClassifier()

dt_classifier.fit(x_train, y_train) 

predictions = dt_classifier.predict(x_test) 
prob_predictions = dt_classifier.predict_proba(x_test) 

print(predictions) 

print(prob_predictions) 

from sklearn.metrics import accuracy_score, confusion_matrix 

print("Training accuracy Score is : ", accuracy_score(y_train, dt_classifier.predict(x_train))) 

print("Testing accuracy Score is : ", accuracy_score(y_test, dt_classifier.predict(x_test))) 

print("Training Confusion Matrix is : \n", confusion_matrix(y_train, dt_classifier.predict(x_train)))

print("Testing Confusion Matrix is : \n", confusion_matrix(y_test, dt_classifier.predict(x_test)))
    """
    return s

def print4b():
    s = """
    import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn as sk

df=pd.read_csv("breast_cancer.csv")

df=df.iloc[:,:-1]

df.shape

x=df.iloc[:,2:].values
y=df.diagnosis.values

print(x[:2])
print(y[:5])

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=500)

x_train.shape

x_test.shape

y_train.shape

y_test.shape

(y_train == 'M').sum()

(y_train=='B').sum()

278/len(y_train)

from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

baseline_pred=["B"] *len(y_train) # baseline hoga beningn for sabke liye

accuracy_score(y_train,baseline_pred) #  parameter me actual aur predicted data lenge

confusion_matrix(y_train,baseline_pred)# parameter me actual aur predicted data lege

print(classification_report(y_train,baseline_pred))

from sklearn.naive_bayes import GaussianNB

nb_model=GaussianNB()

nb_model.fit(x_train,y_train)

print(x_train)

nb_model.score(x_train,y_train)

nb_model.score(x_test,y_test)

#confusion_matrix training data ke liye
confusion_matrix(y_train,nb_model.predict(x_train))

#confusion matrix test data ke liye
confusion_matrix(y_test,nb_model.predict(x_test))

print(classification_report(y_train,nb_model.predict(x_train)))

print(classification_report(y_test,nb_model.predict(x_test)))
"""
    return s 

def print5a():
    s = """
    import matplotlib

import matplotlib.pyplot as plt

def plot_svc_decision_boundary(svm_clf, xmin, xmax):
    w = svm_clf.coef_[0]
    b = svm_clf.intercept_[0]

    #using this eqn fr clculating w0*x0 + w1*x1 + b = 0
    #x1 = -w0/w1 * x0 - b/w1
    x0 = np.linspace(xmin, xmax, 200)
    decision_boundary = -w[0]/w[1] * x0 - b/w[1]

    margin = 1/w[1]
    gutter_up = decision_boundary + margin
    gutter_down = decision_boundary - margin

    svs = svm_clf.support_vectors_
    plt.scatter(svs[:, 0], svs[:, 1], s=180, facecolors='#FFAAAA')
    plt.plot(x0, decision_boundary, "k-", linewidth=2)
    plt.plot(x0, gutter_up, "k--", linewidth=2)
    plt.plot(x0, gutter_down, "k--", linewidth=2)

from sklearn.svm import SVC
from sklearn import datasets
iris = datasets.load_iris()#iris dataset inbuild hai 
X = iris["data"][:, (2, 3)]  # hume 4 data diye gaye hai but qs me petal leghth and petal width 
#ka bola gya hai tabi 2,3 liya gya hai
iris
y = iris["target"]
setosa_or_versicolor = (y == 0) | (y == 1)
X = X[setosa_or_versicolor]
y = y[setosa_or_versicolor]
svm_clf = SVC(kernel="linear", C=float("inf"))
svm_clf.fit(X, y)
svm_clf.predict([[2.4, 3.1]])
#SVM classifiers do not output a probability like logistic regression classifiers

#plot the decision boundaries
import numpy as np
plt.figure(figsize=(12,3.2))
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
svm_clf.fit(X_scaled, y)
plt.plot(X_scaled[:, 0][y==1], X_scaled[:, 1][y==1], "bo")# ye versiolor lene pr
plt.plot(X_scaled[:, 0][y==0], X_scaled[:, 1][y==0], "ms")#ye setosa lene par
plot_svc_decision_boundary(svm_clf, -2, 2)#rangegraph ki har side se boundry
plt.xlabel("Petal Width normalized", fontsize=12)
plt.ylabel("Petal Length normalized", fontsize=12)
plt.title("Scaled", fontsize=16)
plt.axis([-2, 2, -2, 2])
"""
    return s

def print5b():
    s = """
    from sklearn.datasets import make_moons
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from sklearn.datasets import make_moons
X, y = make_moons(n_samples=100, noise=0.15, random_state=42)
def plot_dataset(X, y, axes):
    plt.plot(X[:, 0][y==0], X[:, 1][y==0], "rs")
    plt.plot(X[:, 0][y==1], X[:, 1][y==1], "ms")
    plt.axis(axes)
    plt.grid(True, which='both')
    plt.xlabel('X1', fontsize=20)
    plt.ylabel('X2', fontsize=20, rotation=0)

plot_dataset(X, y, [-1.5, 2.5, -1, 1.5])
plt.show()

def plot_predictions(clf, axes):
    x0s = np.linspace(axes[0], axes[1], 100)
    x1s = np.linspace(axes[2], axes[3], 100)
    x0, x1 = np.meshgrid(x0s, x1s)
    X = np.c_[x0.ravel(), x1.ravel()]
    y_pred = clf.predict(X).reshape(x0.shape)
    y_decision = clf.decision_function(X).reshape(x0.shape)
    plt.contourf(x0, x1, y_pred, cmap=plt.cm.brg, alpha=0.2)
    plt.contourf(x0, x1, y_decision, cmap=plt.cm.brg, alpha=0.1)

polynomial_svm_clf = Pipeline((
    ("poly_features", PolynomialFeatures(degree=3)),
    ("scalar", StandardScaler()),
    ("svm_clf", SVC(kernel="poly", degree=10, coef0=1, C=5)) 
))

polynomial_svm_clf.fit(X,y)

plt.figure(figsize=(11, 4))
plot_predictions(polynomial_svm_clf, [-1.5, 2.5, -1, 1.5])
plot_dataset(X, y, [-1.5, 2.5, -1, 1.5])

plt.title("d=3, coef0=1, C=5", fontsize=18)
plt.show()
"""
    return s

def print6a():
    s = """
    import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv('ch1ex1.csv')
points = df.values
print(points)

from sklearn.cluster import KMeans
model = KMeans(n_clusters=3)
model.fit(points)
labels = model.predict(points)

xs = points[: , 0]
ys = points[:,1]
print(xs)
print(ys)

plt.scatter(xs, ys,c=labels)
plt.show()

centroids = model.cluster_centers_

centroids_x = centroids[:,0]
centroids_y = centroids[:,1]

plt.scatter(xs, ys, c=labels)
plt.scatter(centroids_x, centroids_y, marker='*', s=200)
plt.show()
"""
    return s

def print6b():
    s = """
    import pandas as pd

seeds_df = pd.read_csv('seeds-less-rows.csv')
varieties = list(seeds_df.pop('grain_variety'))
samples = seeds_df.values

from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

mergings = linkage(samples, method='complete')

dendrogram(mergings,
           labels=varieties,
           leaf_rotation=60,
           leaf_font_size=12,
)
plt.show()

from scipy.cluster.hierarchy import fcluster

labels = fcluster(mergings, 6, criterion='distance')

df = pd.DataFrame({'labels': labels, 'varieties': varieties})

ct = pd.crosstab(df['labels'], df['varieties'])

ct
"""
    return s

def print7a():
    s = """
    import numpy as np
from functools import reduce
def perceptron(weight, bias, x):
    model = np.add(np.dot(x, weight), bias)#wx+b
    print('model: ',(model))
    logit = 1/(1+np.exp(-model))
    print('Type:',(logit))
    return np.round(logit)
def compute(logictype, weightdict, dataset):
    weights = np.array([ weightdict[logictype][w] for w in weightdict[logictype].keys()])
    output = np.array([ perceptron(weights, weightdict['bias'][logictype], val) for val in dataset])
    print(logictype)
    return logictype, output

def main():
    logic = {
        'logic_and' : {
            'w0': -0.1,
            'w1': 0.2,
            'w2': 0.2
        },
        
        'logic_nand': {
            'w0': 0.6,
            'w1': -0.8,
            'w2': -0.8
        },
        
        'bias': {
            'logic_and': -0.2,
            'logic_nand': 0.3,
        }
    }
    dataset = np.array([
        [1,0,0],
        [1,0,1],
        [1,1,0],
        [1,1,1]
    ])

    logic_and = compute('logic_and', logic, dataset)
    logic_nand = compute('logic_nand', logic, dataset)
    print(logic_nand)
    def template(dataset, name, data):
        print("Logic Function: ",name[6:].upper())
        print("X0\tX1\tX2\tY")
        toPrint = ["{1}\t{2}\t{3}\t{0}".format(output, *datas) for datas, output in zip(dataset, data)]
        for i in toPrint:
            print(i)

    gates = [logic_and, logic_nand]
    print("yaha pe maine print karaya",*logic_and[1])
    for i in gates:
        template(dataset, *i)
main()
"""
    return s

def print7b():
    s = """
    import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
img = cv2.imread('people.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY )
faces = face_cascade.detectMultiScale(gray, 1.1, 5)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
cv2.imshow('img',img)
cv2.waitKey(215465)
cv2.destroyAllWindows()
"""
    return s
def print8():
    s = """
    import numpy as np
import pandas as pd
from  keras.layers import Dense
from keras.models import Sequential
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


df=pd.read_csv('pima-indians-diabetes.csv')

df.head()

x=df.iloc[:,:-1]
y=df.iloc[:,8]
x.head()


x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33,random_state=0)

network=Sequential()
network.add(Dense(units=8,activation='relu',input_shape=(x_train.shape[1],)))
network.add(Dense(units=16,activation='relu'))
network.add(Dense(units=1,activation='sigmoid'))

network.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

history=network.fit(x_train,y_train,epochs=20,verbose=1,batch_size=100,validation_data=(x_test,y_test))

print(history.history)
training_loss=history.history['loss']
test_loss=history.history["val_loss"]
print(training_loss)
print(test_loss)

epoch_count=range(1,len(training_loss)+1)


plt.plot(epoch_count,training_loss,"r--")
plt.plot(epoch_count,test_loss,"b-")
plt.legend(['training_loss','test_loss'])
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()


ankit, accuracy = network.evaluate(x_train,y_train)
print('Accuracy:' , (accuracy*100))
print(ankit)

ankit, accuracy = network.evaluate(x_test,y_test)
print('Accuracy:' , (accuracy*100))
print(ankit)

predicted_y= network.predict(x_test)
for i in range(10):
    print(predicted_y[i])

training_accuracy=history.history["accuracy"]
test_accuracy=history.history["val_accuracy"]
plt.plot(epoch_count,training_accuracy,"r--")
plt.plot(epoch_count,test_accuracy,"g-")
plt.legend(["Training Accuracy","Test Accuracy"])
plt.xlabel("Epoch")
plt.ylabel("Accuracy Score")
plt.show()
"""
    return s

def print9():
    s = """
    import numpy as np
from keras.datasets import mnist
from keras.utils import to_categorical
import matplotlib.pyplot as plt
%matplotlib inline

import keras
from keras.models import Sequential,Input,Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
#from keras.datasets import mnist
(train_X,train_Y), (test_X,test_Y) = mnist.load_data()
print('Training data shape : ', train_X.shape, train_Y.shape)

print('Testing data shape : ', test_X.shape, test_Y.shape)
# Find the unique numbers from the train labels
classes = np.unique(train_Y)
nClasses = len(classes)
print('Total number of outputs : ', nClasses)
print('Output classes : ', classes)
plt.figure(figsize=[5,5])

# Display the first image in training data
plt.subplot(121)
plt.imshow(train_X[0,:,:], cmap='gray')
plt.title("Ground Truth : {}".format(train_Y[0]))

# Display the first image in testing data
plt.subplot(122)
plt.imshow(test_X[0,:,:], cmap='gray')
plt.title("Ground Truth : {}".format(test_Y[0]))
train_X = train_X.reshape(-1, 28,28, 1)
test_X = test_X.reshape(-1, 28,28, 1)
train_X.shape, test_X.shape
train_X = train_X.astype('float32')
test_X = test_X.astype('float32')
train_X = train_X / 255
test_X = test_X / 255
# Change the labels from categorical to one-hot encoding
train_Y_one_hot = to_categorical(train_Y)
test_Y_one_hot = to_categorical(test_Y)

# Display the change for category label using one-hot encoding
print('Original label:', train_Y[0])
print('After conversion to one-hot:', train_Y_one_hot[0])
from sklearn.model_selection import train_test_split
train_X,valid_X,train_label,valid_label = train_test_split(train_X, train_Y_one_hot, test_size=0.2, random_state=13)
train_X.shape,valid_X.shape,train_label.shape,valid_label.shape
batch_size = 64
epochs = 3
num_classes = 10
m_model = Sequential()
m_model.add(Conv2D(32, kernel_size=(3, 3),activation='linear',input_shape=(28,28,1),padding='same'))
m_model.add(LeakyReLU(alpha=0.1))
m_model.add(MaxPooling2D((2, 2),padding='same'))
#fashion_model.add(Conv2D(64, (3, 3), activation='linear',padding='same'))
#fashion_model.add(LeakyReLU(alpha=0.1))
#fashion_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
#fashion_model.add(Conv2D(128, (3, 3), activation='linear',padding='same'))
#fashion_model.add(LeakyReLU(alpha=0.1))                  
#fashion_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
m_model.add(Flatten())
m_model.add(Dense(128, activation='linear'))
m_model.add(LeakyReLU(alpha=0.1))                  
m_model.add(Dense(num_classes, activation='softmax'))
m_model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(),metrics=['accuracy'])
m_model.summary()
m_train = m_model.fit(train_X, train_label, batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(valid_X, valid_label))
test_eval = m_model.evaluate(test_X, test_Y_one_hot, verbose=0)
print('Test loss:', test_eval[0])
print('Test accuracy:', test_eval[1])
accuracy = m_train.history['accuracy']
val_accuracy = m_train.history['val_accuracy']
loss = m_train.history['loss']
val_loss = m_train.history['val_loss']
epochs = range(len(accuracy))
plt.plot(epochs, accuracy, '--', label='Training accuracy')
plt.plot(epochs, val_accuracy, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs, loss, '--', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()
epochs=1
# ADDING DROPOUT
m_model = Sequential()
m_model.add(Conv2D(32, kernel_size=(3, 3),activation='linear',padding='same',input_shape=(28,28,1)))
m_model.add(LeakyReLU(alpha=0.1))
m_model.add(MaxPooling2D((2, 2),padding='same'))
m_model.add(Dropout(0.25))
#fashion_model.add(Conv2D(64, (3, 3), activation='linear',padding='same'))
#fashion_model.add(LeakyReLU(alpha=0.1))
#fashion_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
#fashion_model.add(Dropout(0.25))
#fashion_model.add(Conv2D(128, (3, 3), activation='linear',padding='same'))
#fashion_model.add(LeakyReLU(alpha=0.1))                  
#fashion_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
#fashion_model.add(Dropout(0.4))
m_model.add(Flatten())
m_model.add(Dense(128, activation='linear'))
m_model.add(LeakyReLU(alpha=0.1))           
m_model.add(Dropout(0.3))
m_model.add(Dense(num_classes, activation='softmax'))
m_model.summary()
m_model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(),metrics=['accuracy'])
m_train_dropout = m_model.fit(train_X, train_label, batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(valid_X, valid_label))
m_model.save("fashion_model_dropout.h5py")
test_eval = m_model.evaluate(test_X, test_Y_one_hot, verbose=1)
print('Test loss:', test_eval[0])
print('Test accuracy:', test_eval[1])
accuracy = m_train_dropout.history['accuracy']
val_accuracy = m_train_dropout.history['val_accuracy']
loss = m_train_dropout.history['loss']
val_loss = m_train_dropout.history['val_loss']
epochs = range(len(accuracy))
plt.plot(epochs, accuracy, 'bo', label='Training accuracy')
plt.plot(epochs, val_accuracy, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()
predicted_classes = m_model.predict(test_X)
predicted_classes = np.argmax(np.round(predicted_classes),axis=1)
predicted_classes.shape, test_Y.shape
correct = np.where(predicted_classes==test_Y)[0]
print ("Found %d correct labels" % len(correct))
for i, correct in enumerate(correct[:9]):
    plt.subplot(3,3,i+1)
    plt.imshow(test_X[correct].reshape(28,28), cmap='gray', interpolation='none')
    plt.title("Predicted {}, Class {}".format(predicted_classes[correct], test_Y[correct]))
    plt.tight_layout()
incorrect = np.where(predicted_classes!=test_Y)[0]
print ("Found %d incorrect labels" % len(incorrect))
for i, incorrect in enumerate(incorrect[:9]):
    plt.subplot(3,3,i+1)
    plt.imshow(test_X[incorrect].reshape(28,28), cmap='gray', interpolation='none')
    plt.title("Predicted {}, Class {}".format(predicted_classes[incorrect], test_Y[incorrect]))
    plt.tight_layout()
from sklearn.metrics import classification_report
target_names = ["Class {}".format(i) for i in range(num_classes)]
print(classification_report(test_Y, predicted_classes, target_names=target_names))
"""
    return s

def print10():
    s = """
    from keras.models import Sequential
from keras.layers import Embedding, SimpleRNN,Dense
from keras.datasets import imdb
from keras.preprocessing import sequence
max_features = 10000
maxlen = 500
batch_size = 32

print('Loading data...')
(input_train, y_train), (input_test, y_test) = imdb.load_data( num_words=max_features)
print(len(input_train), 'train sequences')
print(len(input_test), 'test sequences')
print('Pad sequences (samples x time)')
input_train = sequence.pad_sequences(input_train, maxlen=maxlen)
input_test = sequence.pad_sequences(input_test, maxlen=maxlen)
print('input_train shape:', input_train.shape)
print('input_test shape:', input_test.shape)

model = Sequential()
model.add(Embedding(max_features, 32)) #max features  ye hai agar =10,000  to 32 se multiple karne ke baad  320,000
model.add(SimpleRNN(32))               #(32+32+1)*32=2080
model.add(Dense(1, activation='sigmoid'))#(32+1)*1=33
model.summary()

model.compile(optimizer='rmsprop', loss='binary_crossentropy',metrics=['acc'])
history = model.fit(input_train, y_train,epochs=10, batch_size=128, validation_split=0.2)

predicted_classes = model.predict(input_test)

import numpy as np
predicted_classes = np.argmax(np.round(predicted_classes),axis=1)

predicted_classes.shape, y_test.shape

correct = np.where(predicted_classes==y_test)[0]
print ("Found %d correct labels" % len(correct))


incorrect = np.where(predicted_classes!=y_test)[0]
print ("Found %d incorrect labels" % len(incorrect))

from sklearn.metrics import classification_report
num_classes=2
target_names = ["Class {}".format(i) for i in range(num_classes)]
print(classification_report(y_test, predicted_classes, target_names=target_names))

import matplotlib.pyplot as plt
acc = history.history['acc']
val_acc = history.history['val_acc']
epochs = range(1, len(acc) + 1)
plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()



plt.figure()
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(acc) + 1)
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()
"""
    return s




# print(print8())
# print(print2a())
# print(print2b())
# print(print3a())
# print(print3b())
# print(print4a())
# print(print4b())
# print(print5a())
# print(print5b())
# print(print6a())
# print(print6b())
# print(print7a())
# print(print7b())
# print(print8())
# print(print9())
# print(print10())