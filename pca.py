from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt


def load_and_center_dataset(filename):
    # TODO: add your code here
    data = np.load(filename)
    centered_data = data - np.mean(data, axis=0)
    return centered_data
    
def get_covariance(dataset):
    # TODO: add your code here
    covariance = np.zeros((len(dataset[0]),len(dataset[0])))
    for i in range(len(dataset)):
        a = dataset[i, :].reshape(1,len(dataset[0]))
        b = a.reshape(len(dataset[0]),1)
        covariance = covariance + np.dot(b,a)
    return covariance/(len(dataset) - 1)

def get_eig(S, m):
    # TODO: add your code here
    w,v = eigh(S,eigvals=(len(S)-m, len(S)-1))
    w[::-1].sort()
    diag_eig = np.diag(w)
    v = np.flip(v, axis=1)
    return diag_eig, v

def get_eig_perc(S, perc):
    # TODO: add your code here
    eigen = eigh(S, eigvals_only=True)
    sum_eigen = sum(eigen)
    max_eigen = max(eigen)
    eigen_perc = sum_eigen * perc
    w,v = eigh(S,subset_by_value = (eigen_perc, max_eigen+1))
    w[::-1].sort()
    diag = np.diag(w)
    v = np.flip(v,axis=1)
    return diag, v

def project_image(img, U):
    # TODO: add your code here
    col = len(U[0])
    row = len(U)
    count = np.zeros((row,1))
    for i in range(col):
        a = U[:,i].reshape(row, 1)
        b = np.dot(np.transpose(a), img)
        c = b* a
        count = count + c
    return count

def display_image(orig, proj):
    # TODO: add your code here
    og_image = orig.reshape(32,32)
    pj_image = proj.reshape(32,32)
    og_image = np.transpose(og_image)
    pj_image = np.transpose(pj_image)
    fig, axs = plt.subplots(nrows=1, ncols=2)
    axs[0].set_title('Original')
    axs[1].set_title('Projection')
    image1 = axs[0].imshow(og_image,aspect = 'equal')
    image2 = axs[1].imshow(pj_image,aspect = 'equal')
    fig.colorbar(image1, ax = axs[0])
    fig.colorbar(image2, ax = axs[1])
    return plt.show()