import numpy as np 

class Preprocessor:
    def __init__ (self, dataset):
        self._n_photons = np.sum(dataset, axis=1)
        self._mean = np.mean (dataset.T, axis=0)
        self._std = np.std (dataset.T, axis=0)
        
    def transform (self, X):
        return_x = ((X.T - self._mean)/(self._std + 1))
        return return_x.T
    
    def transform_normalized (self, X):
        return_x = ((X.T - self._mean)/(self._std + 1))/(self._n_photons + 1e-7)
        return return_x.T
    
    def transform_normalized_2 (self, X):
        from scipy.special import softmax
        return_x = X.T
        return_x = ((return_x - self._mean)/(self._std + 1))
        
        return_x = softmax(return_x, axis=0)
        
        return return_x.T

class Preprocessor2D:
    def __init__ (self, dataset):
        self._n_photons = np.sum(dataset, axis=-1)
        self._mean = np.mean (dataset, axis=(1,2,3))
        self._std = np.std (dataset, axis=(1,2,3))

    def transform (self, X, softmax_it=False, normalize_it=False):
        if normalize_it:
            return_x = X[::,::,::,::] / (self._n_photons[::,::,::, None] + 1e-10)
            self._mean = np.mean (return_x, axis=(1,2,3))
            self._std = np.std (return_x, axis=(1,2,3))
        else:
            return_x = X

        return_x = (return_x[::,::,::,::] - self._mean[::, None, None, None])/(self._std[::, None, None, None] + 1)

        if softmax_it:
            from scipy.special import softmax
            return_x = softmax(return_x, axis=-1)

        return return_x