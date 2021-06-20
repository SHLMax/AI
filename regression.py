import numpy as np
from matplotlib import pyplot as plt
import csv
import math


# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.


def get_dataset(filename):
    """
    TODO: implement this function.

    INPUT: 
        filename - a string representing the path to the csv file.

    RETURNS:
        An n by m+1 array, where n is # data points and m is # features.
        The labels y should be in the first column.
    """
    dataset = []
    with open(filename,encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        next(reader)
        for row in reader:
            dataset.append(row[1:])
        
    return np.array(dataset)


def print_stats(dataset, col):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        col     - the index of feature to summarize on. 
                  For example, 1 refers to density.

    RETURNS:
        None
    """
    num_data = len(dataset)
    data = []
    for row in dataset:
        data.append(row[col])
    s = 0
    for e in data:
        e = float(e)
        s = s + e;
    mean = s/num_data
    deviation = 0
    for e in data:
        e = float(e)
        deviation = deviation + math.pow(e - mean,2)
    deviation = math.sqrt(deviation/num_data)
    
    print(num_data)
    print("%.2f" % mean)
    print("%.2f" % deviation)
    pass


def regression(dataset, cols, betas):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        mse of the regression model
    """
    mse = 0
    n = len(dataset)
    for row in dataset:
        i = 0
        y_MSE = 0
        for b in betas[1:]:
            y_MSE = y_MSE + b * float(row[cols[i]])
            i = i + 1
        y_MSE = y_MSE + betas[0]
        

        difference = y_MSE - float(row[0])
        mse = mse + math.pow(difference, 2)
    
    mse = mse / n
    return mse


def gradient_descent(dataset, cols, betas):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        An 1D array of gradients
    """
    grads = []
    n = len(dataset)
    grad = 0
    for row in dataset:
        i = 0;
        g = betas[0];
        for b in betas[1:]:
            g = g + b * float(row[cols[i]])
            i = i + 1
        difference = (g - float(row[0]))
        grad = grad + difference
    grad = 2 * grad / n
    grads.append(grad)
        
    for col in cols:
        grad = 0
        sum = 0
        for row in dataset:
            i = 0;
            g = betas[0];
            for b in betas[1:]:
                g = g + b * float(row[cols[i]])
                i = i + 1
            difference = (g - float(row[0])) * float(row[col])
            sum = sum + difference
        grad = 2 * sum / n
        grads.append(grad)
    grads = np.array(grads)
    return grads


def iterate_gradient(dataset, cols, betas, T, eta):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]
        T       - # iterations to run
        eta     - learning rate

    RETURNS:
        None
    """
    prev_betas = betas
    for t in range(1,T+1):
        i = 0;
        grad_betas = gradient_descent(dataset, cols, betas)
        for b in prev_betas:
            prev_betas[i] = b - eta * grad_betas[i]
            i = i + 1
        mse = regression(dataset, cols, prev_betas)
        print(t,mse, end = " ")
        for j in range(len(betas)):
            if j == len(betas) - 1:
                print("%.2f" % prev_betas[j])
            else:
                print("%.2f" % prev_betas[j], end = " ")
    pass


def compute_betas(dataset, cols):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.

    RETURNS:
        A tuple containing corresponding mse and several learned betas
    """
    betas = []
    mse = 0
    data = np.array(dataset, dtype=np.float32)
    
    n = len(dataset)
    y = data[:,0].reshape(n,1)
    x = np.ones([n,1],dtype = float)
    col = data[:,cols]
    x = np.hstack((x, col))
    x_t = np.transpose(x)  
    squarex = np.matmul(x_t,x)
    inverse = np.linalg.inv(squarex)
    a = np.matmul(inverse,x_t)
    beta = np.matmul(a,y)
    for e in beta:
        betas.append(e[0])
    mse = regression(dataset, cols, betas)
    
    return (mse, *betas)


def predict(dataset, cols, features):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        features- a list of observed values

    RETURNS:
        The predicted body fat percentage value
    """
    result = 0
    beta = list(compute_betas(dataset, cols))
    
    b = beta[1:]
    
    i = 1
    for f in features:
        result = result + f * b[i]
        i = i + 1
    result = result + b[0]
    return result


def synthetic_datasets(betas, alphas, X, sigma):
    """
    TODO: implement this function.

    Input:
        betas  - parameters of the linear model
        alphas - parameters of the quadratic model
        X      - the input array (shape is guaranteed to be (n,1))
        sigma  - standard deviation of noise

    RETURNS:
        Two datasets of shape (n,2) - linear one first, followed by quadratic.
    """
    
    one = np.ones([len(X),1],dtype = float)
    x = np.hstack((one, X))
    x_square = np.square(X)
    x_square = np.hstack((one, x_square))
    betas = betas.reshape(1,2)
    alphas = alphas.reshape(1,2)
    L = []
    Q = []
    for e in x:
        z = np.random.normal(0,sigma)
        e = e.reshape(2,1)
        e_square = np.square(e)
        x_linear = np.matmul(betas,e) + z
        x_square = np.matmul(alphas,e_square) + z
        L.append(x_linear)
        Q.append(x_square)
    Linear = np.array(L).reshape(len(X),1)
    Linear = np.hstack((Linear,X))

    Quadratic = np.array(Q).reshape(len(X),1)
    Quadratic = np.hstack((Quadratic,X))
    return (Linear, Quadratic)


def plot_mse():
    from sys import argv
    if len(argv) == 2 and argv[1] == 'csl':
        import matplotlib
        matplotlib.use('Agg')

    # TODO: Generate datasets and plot an MSE-sigma graph
    sigmas = []
    X = np.random.randint(-100,101,1000).reshape(1000,1)     
    for i in range(-4,6):
        sigmas.append(math.pow(10,i))
    betas = np.array([1,2])
    alphas = np.array([3,4])
    dataset = []
    for s in sigmas:
        dataset.append(synthetic_datasets(betas, alphas, X, s))
    MSE_Linear = []
    MSE_Quadratic = []
    for d in dataset:
        MSE_Linear.append(compute_betas(d[0],[1])[0])
        MSE_Quadratic.append(compute_betas(d[1],[1])[0])
    fig = plt.figure()
    plt.plot(sigmas,MSE_Linear,marker="o")
    plt.plot(sigmas,MSE_Quadratic,marker="o")

    plt.xlabel("sigma")
    plt.ylabel("MSEs")
    plt.legend(["Linear", "Quadratic"])
    plt.yscale('log')
    plt.xscale('log')
    fig.savefig("mse.pdf")
    
    
        
        

if __name__ == '__main__':
    ### DO NOT CHANGE THIS SECTION ###
    plot_mse()
