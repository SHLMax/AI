import os
import math
from pathlib import Path

#These first two functions require os operations and so are completed for you
#Completed for you
def load_training_data(vocab, directory):
    """ Create the list of dictionaries """
    top_level = os.listdir(directory)
    dataset = []
    for d in top_level:
        if d[-1] == '/':
            label = d[:-1]
            subdir = d
        else:
            label = d
            subdir = d+"/"
        files = os.listdir(directory+subdir)
        for f in files:
            bow = create_bow(vocab, directory+subdir+f)
            dataset.append({'label': label, 'bow': bow})
    return dataset

#Completed for you
def create_vocabulary(directory, cutoff):
    """ Create a vocabulary from the training directory
        return a sorted vocabulary list
    """

    top_level = os.listdir(directory)
    vocab = {}
    for d in top_level:
        subdir = d if d[-1] == '/' else d+'/'
        files = os.listdir(directory+subdir)
        for f in files:
            with open(directory+subdir+f,'r', encoding = 'utf-8') as doc:
                for word in doc:
                    word = word.strip()
                    if not word in vocab and len(word) > 0:
                        vocab[word] = 1
                    elif len(word) > 0:
                        vocab[word] += 1
    return sorted([word for word in vocab if vocab[word] >= cutoff])

#The rest of the functions need modifications ------------------------------
#Needs modifications
def create_bow(vocab, filepath):
    """ Create a single dictionary for the data
        Note: label may be None
    """
    bow = {}
    # TODO: add your code here
    c = 0
    lines = []
    with open(filepath,'r',encoding='utf-8') as file:
        for line in file: 
            line = line.strip() #or some other preprocessing
            lines.append(line) #storing everything in memory!

    for e in lines:
        if (e in vocab):
            bow[e] = lines.count(e)   
        else:
            c = c + 1
            bow[None] = c
    return bow

#Needs modifications
def prior(training_data, label_list):
    """ return the prior probability of the label in the training set
        => frequency of DOCUMENTS
    """

    smooth = 1 # smoothing factor
    logprob = {}
    # TODO: add your code here
    
    total_num = len(training_data)
    for n in label_list:
        num_file = 0
        for e in training_data:
            if(e['label'] == n):
                num_file = num_file + 1
        P = ( num_file + smooth ) / (total_num + smooth + 1)
        logprob[n] = math.log(P)
    return logprob

#Needs modifications
def p_word_given_label(vocab, training_data, label):
    """ return the class conditional probability of label over all words, with smoothing """

    smooth = 1 # smoothing factor
    word_prob = {}
    # TODO: add your code here
    total_words = 0
    num_none = 0
    for a in training_data:
        if(a['label'] == label):
            total_words = total_words + sum(a['bow'].values())
            if(None in a['bow']):
                num_none = num_none + a['bow'][None]
    
    for w in vocab:
        num_words = 0
        for e in training_data:
            if(e['label'] == label and w in e['bow'].keys()):
                num_words = num_words + e['bow'][w]
            
            p = (num_words + smooth) / (total_words + smooth * (len(vocab) + 1))
            word_prob[w] = math.log(p)
    p_none = (num_none + smooth) / (total_words + smooth * (len(vocab) + 1))
    word_prob[None] = math.log(p_none)
    return word_prob


##################################################################################
#Needs modifications
def train(training_directory, cutoff):
    """ return a dictionary formatted as follows:
            {
             'vocabulary': <the training set vocabulary>,
             'log prior': <the output of prior()>,
             'log p(w|y=2016)': <the output of p_word_given_label() for 2016>,
             'log p(w|y=2020)': <the output of p_word_given_label() for 2020>
            }
    """
    retval = {}
    label_list = os.listdir(training_directory)
    # TODO: add your code here
    vocab = create_vocabulary(training_directory, cutoff)
    training_data = load_training_data(vocab, training_directory)
    retval['vocabulary'] = vocab
    retval['log prior'] = prior(training_data, label_list)
    retval['log p(w|y=2016)'] = p_word_given_label(vocab, training_data, '2016')
    retval['log p(w|y=2020)'] = p_word_given_label(vocab, training_data, '2020')
    
    
    return retval

#Needs modifications
def classify(model, filepath):
    """ return a dictionary formatted as follows:
            {
             'predicted y': <'2016' or '2020'>,
             'log p(y=2016|x)': <log probability of 2016 label for the document>,
             'log p(y=2020|x)': <log probability of 2020 label for the document>
            }
    """
    retval = {}
    # TODO: add your code here
    lines = []
    with open(filepath,'r',encoding='utf-8') as file:
        for line in file: 
            line = line.strip() #or some other preprocessing
            lines.append(line) #storing everything in memory!
    prior_2020 = model['log prior']['2020']
    prior_2016 = model['log prior']['2016']    
    p_y_2016 = 0
    p_y_2020 = 0
    vocab = model['vocabulary']

    for a in lines:
        if(a in vocab):
            p_y_2016 = p_y_2016 + model['log p(w|y=2016)'][a]
        else:
            p_y_2016 = p_y_2016 + model['log p(w|y=2016)'][None]
    for a in lines:
        if(a in vocab):
            p_y_2020 = p_y_2020 + model['log p(w|y=2020)'][a]
        else:
            p_y_2020 = p_y_2020 + model['log p(w|y=2020)'][None]
            
    log_p_2016 = prior_2016 + p_y_2016
    log_p_2020 = prior_2020 + p_y_2020

    retval['log p(y=2016|x)'] = log_p_2016
    retval['log p(y=2020|x)'] = log_p_2020
    if(log_p_2016 > log_p_2020):
        retval['predicted y'] = '2016'
    else:
        retval['predicted y'] = '2020'
    return retval






