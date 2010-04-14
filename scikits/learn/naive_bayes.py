# Author: Vincent Michel <vincent.michel@inria.fr>
# License: BSD Style.
import numpy as np

class GNB(object):
    """
    Gaussian Naive Bayes (GNB)

    Parameters
    ----------
    X : array-like, shape = [nsamples, nfeatures]
        Training vector, where nsamples in the number of samples and
        nfeatures is the number of features.
    y : array, shape = [nsamples]
        Target vector relative to X

    Attributes
    ----------
    proba_y : array, shape = nb of classes
              probability of each class.
    theta : array of shape nb_class*nb_features
            mean of each feature for the different class
    sigma : array of shape nb_class*nb_features
            variance of each feature for the different class


    Methods
    -------
    fit(X, Y) : self
        Fit the model

    predict(X) : array
        Predict using the model.

    predict_proba(X) : array
        Predict the proba of each class using the model.

    Examples
    --------
    >>> X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    >>> Y = np.array([1, 1, 1, 2, 2, 2])
    >>> clf = GNB()
    >>> clf.fit(X, Y)    #doctest: +ELLIPSIS
    <scikits.learn.naive_bayes.GNB object at 0x...>
    >>> print clf.predict([[-0.8, -1]])
    [1]

    See also
    --------

    """

    def fit(self, X, y):
        theta = []
        sigma = []
        proba_y = []
        uniy = np.unique(y)
        for yi in uniy:
            theta.append(np.mean(X[y==yi,:],0))
            sigma.append(np.var(X[y==yi,:],0))
            proba_y.append(np.float(np.sum(y==yi))/np.size(y))
        self.theta = np.array(theta)
        self.sigma = np.array(sigma)
        self.proba_y = np.array(proba_y)
        self.uniy = uniy
        return self


    def predict(self, X):
        y_pred = self.uniy[np.argmax(self.predict_proba(X),1)]
        return y_pred


    def predict_proba(self, X):
        joint_log_likelihood = []
        for i in range(np.size(self.uniy)):
            jointi = np.log(self.proba_y[i])
            n_ij = np.sum(-0.5*np.log(np.pi*self.sigma[i,:]))
            n_ij = n_ij*np.ones(np.size(X,0))
            n_ij -= np.sum((X - self.theta[i,:])**2,1)
            n_ij += np.sum(2*self.sigma[i,:])*np.ones(np.size(X,0))
            joint_log_likelihood.append(jointi+n_ij)
        joint_log_likelihood = np.array(joint_log_likelihood).T
        proba = np.exp(joint_log_likelihood)
        proba = proba/np.sum(proba,1)[:,np.newaxis]
        return proba

