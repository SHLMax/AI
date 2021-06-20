import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.


def get_data_loader(training = True):
    """
    TODO: implement this function.

    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) or the test set (if training = False)
    """
    custom_transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])

    train_set = datasets.MNIST('./data', train=True, download=True,transform=custom_transform)
    test_set = datasets.MNIST('./data', train=False,transform=custom_transform)
    trainloader =  torch.utils.data.DataLoader(train_set, batch_size = 50)
    testloader = torch.utils.data.DataLoader(test_set, batch_size = 50)
    if training == True:
        return trainloader
    else:
        return testloader

def build_model():
    """
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
    """
    model = nn.Sequential(
      nn.Flatten(),
      nn.Linear(28*28, 128),
      nn.ReLU(),
      nn.Linear(128, 64),
      nn.ReLU(),
      nn.Linear(64, 10),
    )  
    return model



def train_model(model, train_loader, criterion, T):
    """
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
    """
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    model.train()
    for epoch in range(T):
        running_loss = 0.0
        correct = 0
        for i, (data,target) in enumerate(train_loader):
            opt.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, target)
            loss.backward()
            running_loss += loss.item()
            opt.step()
            predicted = outputs.argmax(dim=1,keepdim = True)
            correct += predicted.eq(target.view_as(predicted)).sum().item()
            
        print("Train Epoch: {} Accuracy: {}/{}({:.2f}%) Loss: {:.3f}".format(epoch, correct, len(train_loader.dataset), 100*correct/len(train_loader.dataset), running_loss/1200))



def evaluate_model(model, test_loader, criterion, show_loss = True):
    """
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - cropy-entropy 

    RETURNS:
        None
    """
    
    model.eval()
    correct = 0
    running_loss = 0.0
    total = 0
    with torch.no_grad():
        for data, labels in test_loader:
            outputs = model(data)
            loss = criterion(outputs, labels)
            _, predicted = torch.max(outputs.data, 1) 
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            running_loss += loss.item()
        if(show_loss == True):
            print("Average loss: {:.4f}".format(running_loss/len(test_loader.dataset)))
            print("Accuracy: {:.2f}%".format(100*correct/total))
        else:
            print("Accuracy: {:.2f}%".format(100*correct/total))

def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1


    RETURNS:
        None
    """
    outputs =  model(test_images[index])
    prob = F.softmax(outputs,dim = 1)
    value, index = torch.topk(prob,3)
    class_names = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    print(""+class_names[index[0][0]] + ": {:.2f}%".format(100*float(value.data[0][0])))
    print(""+class_names[index[0][1]] + ": {:.2f}%".format(100*float(value.data[0][1])))
    print(""+class_names[index[0][2]] + ": {:.2f}%".format(100*float(value.data[0][2])))

    
if __name__ == '__main__':
    '''
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    '''
    criterion = nn.CrossEntropyLoss()
