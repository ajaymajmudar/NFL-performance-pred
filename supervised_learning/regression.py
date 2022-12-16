from re import X
import numpy as np
from numpy.linalg import inv
from sklearn.utils.extmath import weighted_mode


class Regression(object):

    def __init__(self):
        pass

    def rmse(self, pred, label):  # [5pts]
        '''
        This is the root mean square error.
        Args:
            pred: numpy array of length N * 1, the prediction of labels
            label: numpy array of length N * 1, the ground truth of labels
        Return:
            a float value
        '''
        length=pred.shape[0]
        #print(length)
        quantity=np.square(pred-label)
        value=np.sqrt(np.mean(quantity))

        return value 



        # raise NotImplementedError

    def construct_polynomial_feats(self, x, degree):  # [5pts]
        """
        Args:
            x: N x D numpy array, where N is number of instances and D is the
               dimensionality of each instance.
            degree: the max polynomial degree
        Return:
            feat: 
                For 1-D array, numpy array of shape Nx(degree+1), remember to include
                the bias term. feat is in the format of:
                [[1.0, x1, x1^2, x1^3, ....,],
                 [1.0, x2, x2^2, x2^3, ....,],
                 ......
                ]
                
                For D-dimensional array: numpy array of shape N x (degree+1) x D, remember to include
                  the bias term.

                Example: print(feat)
                For an input where N=3, D=2, and degree=3...

                [[[ 1.0        1.0]
                  [ x_{1,1}    x_{1,1}]
                  [ x_{1,1}^2  x_{1,2}^2]
                  [ x_{1,1}^3  x_{1,2}^3]]

                 [[ 1.0        1.0]
                  [ x_{2,1}    x_{2,2}]
                  [ x_{2,1}^2  x_{2,2}^2]
                  [ x_{2,1}^3  x_{2,2}^3]]

                 [[ 1.0        1.0]
                  [ x_{3,1}    x_{3,2}]
                  [ x_{3,1}^2  x_{3,2}^2]
                  [ x_{3,1}^3  x_{3,2}^3]]]

        """
        #print(x)
        add_coldim=x[:,np.newaxis]
        return np.concatenate([add_coldim**i for i in range(degree+1)], axis=1) #along vertical axis


        #raise NotImplementedError

    def predict(self, xtest, weight):  # [5pts]
        """
        Args:
            xtest: NxD numpy array, where N is number
                   of instances and D is the dimensionality of each
                   instance
            weight: Dx1 numpy array, the weights of linear regression model
        Return:
            prediction: Nx1 numpy array, the predicted labels
        """
        
        
        prediction=np.dot(xtest,weight)
        return prediction 
        #raise NotImplementedError

    # =================
    # LINEAR REGRESSION
    # Hints: in the fit function, use close form solution of the linear regression to get weights.
    # For inverse, you can use numpy linear algebra function
    # For the predict, you need to use linear combination of data points and their weights (y = theta0*1+theta1*X1+...)

    def linear_fit_closed(self, xtrain, ytrain):  # [5pts]
        """
        Args:
            xtrain: N x D numpy array, where N is number of instances and D is the dimensionality of each instance
            ytrain: N x 1 numpy array, the true labels
        Return:
            weight: Dx1 numpy array, the weights of linear regression model
        """
        
        #weight=np.dot(np.linalg.pinv(xtrain),ytrain)
        xt=np.transpose(xtrain)
        x=xtrain
        xtx=np.dot(xt,x)
        inverse=np.linalg.pinv(xtx)
        inverse_xt=np.dot(inverse,xt)
        weight=np.dot(inverse_xt,ytrain)
        return weight
        #raise NotImplementedError

    def linear_fit_GD(self, xtrain, ytrain, epochs=5, learning_rate=0.001):  # [5pts]
        """
        Args:
            xtrain: NxD numpy array, where N is number
                    of instances and D is the dimensionality of each
                    instance
            ytrain: Nx1 numpy array, the true labels
        Return:
            weight: Dx1 numpy array, the weights of linear regression model
        """
        raise NotImplementedError

    def linear_fit_SGD(self, xtrain, ytrain, epochs=100, learning_rate=0.001):  # [5pts]
        """
        Args:
            xtrain: NxD numpy array, where N is number
                    of instances and D is the dimensionality of each
                    instance
            ytrain: Nx1 numpy array, the true labels
        Return:
            weight: Dx1 numpy array, the weights of linear regression model
        """
        raise NotImplementedError

    # =================
    # RIDGE REGRESSION

    def ridge_fit_closed(self, xtrain, ytrain, c_lambda):  # [5pts]
        """
        Args:
            xtrain: N x D numpy array, where N is number of instances and D is the dimensionality of each instance
            ytrain: N x 1 numpy array, the true labels
            c_lambda: floating number
        Return:
            weight: Dx1 numpy array, the weights of ridge regression model
        """
        
        #(x^tx+lambda*I)^-1 z^t*y
        xTx=np.dot(np.transpose(xtrain),xtrain)
        I=np.eye(xtrain.shape[1])
        inverse=np.linalg.pinv(xTx+np.dot(c_lambda,I))
        xTy=np.dot(np.transpose(xtrain),ytrain)
        weight=np.dot(inverse,xTy)
        return weight
        #raise NotImplementedError

    def ridge_fit_GD(self, xtrain, ytrain, c_lambda, epochs=500, learning_rate=1e-7):  # [5pts]
        """
        Args:
            xtrain: NxD numpy array, where N is number
                    of instances and D is the dimensionality of each
                    instance
            ytrain: Nx1 numpy array, the true labels
            c_lambda: floating number
        Return:
            weight: Dx1 numpy array, the weights of linear regression model
        """
        raise NotImplementedError

    def ridge_fit_SGD(self, xtrain, ytrain, c_lambda, epochs=100, learning_rate=0.001):  # [5pts]
        """
        Args:
            xtrain: NxD numpy array, where N is number
                    of instances and D is the dimensionality of each
                    instance
            ytrain: Nx1 numpy array, the true labels
        Return:
            weight: Dx1 numpy array, the weights of linear regression model
        """
        raise NotImplementedError

    def ridge_cross_validation(self, X, y, kfold=10, c_lambda=100):  # [8 pts]
        """
        Args: 
            X : NxD numpy array, where N is the number of instances and D is the dimensionality of each instance
            y : Nx1 numpy array, true labels
            kfold: Number of folds you should take while implementing cross validation.
            c_lambda: Value of regularization constant
        Returns:
            meanErrors: Float average rmse error
        Hint: np.concatenate might be helpful.
        Look at 3.5 to see how this function is being used.
        # For cross validation, use 10-fold method and only use it for your training data (you already have the train_indices to get training data).
        # For the training data, split them in 10 folds which means that use 10 percent of training data for test and 90 percent for training.
        """
        
        N=X.shape[0]
        weight=self.ridge_fit_closed(X,y,c_lambda)
        percent=kfold/100
        training_indices=int(percent*N) 

        #predict=self.predict(X[training_indices:,:],weight)
        predict=self.predict(np.vsplit(X,kfold),weight)
        #meanErrors=self.rmse(predict,y[training_indices:, :])
        meanErrors=self.rmse(predict,np.vsplit(y,kfold))
        return meanErrors
        #raise NotImplementedError
