
import numpy as np
from sklearn.feature_extraction import text
from sklearn.model_selection import train_test_split
import pandas as pd

RANDOM_SEED = 5


class NaiveBayes(object):
    def __init__(self):
        pass

    def likelihood_ratio(self, ratings_stars):  # [5pts]
        '''
        Args:
            rating_stars is a python list of numpy arrays that is length <number of labels> x 1
            
            Example rating_stars for Five-label NB model:
    
            ratings_stars = [ratings_1, ratings_2, ratings_3, ratings_4, ratings_5] -- length 5

            ratings_1: N_ratings_1 x D
                where N_ratings_1 is the number of reviews that gave an Amazon
                product a 1-star rating and D is the number of features (we use the word count as the feature)
            ratings_2: N_ratings_2 x D
                where N_ratings_2 is the number of reviews that gave an Amazon
                product a 2-star rating and D is the number of features (we use the word count as the feature)
            ratings_3: N_ratings_3 x D
                where N_ratings_3 is the number of reviews that gave an Amazon
                product a 3-star rating and D is the number of features (we use the word count as the feature)
            ratings_4: N_ratings_4 x D
                where N_ratings_4 is the number of reviews that gave an Amazon
                product a 4-star rating and D is the number of features (we use the word count as the feature)
            ratings_5: N_ratings_5 x D
                where N_ratings_5 is the number of reviews that gave an Amazon
                product a 5-star rating and D is the number of features (we use the word count as the feature)
            
            If you look at the end of this python file, you will see a docstring that contains more examples!
            
        Return:
            likelihood_ratio: <number of labels> x D matrix of the likelihood ratio of different words for different class of speeches
        '''
        
        # ratings_1=ratings_stars[0]
        # ratings_2=ratings_stars[1]
        # ratings_3=ratings_stars[2]
        # ratings_4=ratings_stars[3]
        # ratings_5=ratings_stars[4]

        # total=0
        # for label in ratings_stars:
        #     sum_label=np.sum(label,axis=0)
        #     #sum_label = np.sum(label, axis=0) + 1
        #     total+=np.sum(sum_label)+1
        #denom=np.sum(ratings_1)+np.sum(ratings_2)+np.sum(ratings_3)+np.sum(ratings_4)+np.sum(ratings_5)
        D=ratings_stars[0].shape[1]
        num_label=len(ratings_stars)
        # print(num_label)
        # print(D)
        likelihood_ratio=np.zeros([num_label,D])
        numerator=[]
        for label in ratings_stars:
            numerator.append(label.copy())
        for label in range(num_label):
            sum_label = np.sum(ratings_stars[label], axis=0) + 1
            likelihood_ratio[label,:]=(sum_label/sum(sum_label))
        #print(likelihood_ratio)
        return likelihood_ratio
        
        #raise NotImplementedError

    def priors_prob(self, ratings):  # [5pts]
        '''
        Args:
            rating_stars is a python list of numpy arrays that is length <number of labels> x 1
            
            Example rating_stars for Five-label NB model:
    
            ratings_stars = [ratings_1, ratings_2, ratings_3, ratings_4, ratings_5] -- length 5

            ratings_1: N_ratings_1 x D
                where N_ratings_1 is the number of reviews that gave an Amazon
                product a 1-star rating and D is the number of features (we use the word count as the feature)
            ratings_2: N_ratings_2 x D
                where N_ratings_2 is the number of reviews that gave an Amazon
                product a 2-star rating and D is the number of features (we use the word count as the feature)
            ratings_3: N_ratings_3 x D
                where N_ratings_3 is the number of reviews that gave an Amazon
                product a 3-star rating and D is the number of features (we use the word count as the feature)
            ratings_4: N_ratings_4 x D
                where N_ratings_4 is the number of reviews that gave an Amazon
                product a 4-star rating and D is the number of features (we use the word count as the feature)
            ratings_5: N_ratings_5 x D
                where N_ratings_5 is the number of reviews that gave an Amazon
                product a 5-star rating and D is the number of features (we use the word count as the feature)
            
            If you look at the end of this python file, you will see a docstring that contains more examples!
            
        Return:
            priors_prob: 1 x <number of labels> matrix where each entry denotes the prior probability for each class
        '''
        num_labels=len(ratings)
        total=0
        for label in ratings:
            total+=np.sum(label)
        #print(np.sum(ratings[0]),np.sum(ratings[1]))
        #print(total)
        numerator=[]
        for label in ratings:
            numerator.append(label.copy())
        #print(numerator)
        
        priors_prob=np.zeros([1,num_labels])

        for i in range(num_labels):
            priors_prob[:,i]=(np.sum(ratings[i])/total)

        #print(priors_prob,priors_prob.shape, priors_prob.flatten())
        return priors_prob.flatten()
        #raise NotImplementedError

    # [5pts]
    def analyze_star_rating(self, likelihood_ratio, priors_prob, X_test):
        '''
        Args:
            likelihood_ratio: <num labels> x D matrix of the likelihood ratio of different words for different class of news
            priors_prob: 1 x <num labels> matrix where each entry denotes the prior probability for each class
            X_test: N_test x D bag of words representation of the N_test number of news that we need to analyze its sentiment
        Return:
             1 x N_test list where each entry is a class label specific for the Naive Bayes model
        '''
        
        N_test=X_test.shape[0]
        num_labels=likelihood_ratio.shape[0]
        #array=np.zeros([1,N_test])
        array=np.zeros(N_test)
        #print(array.shape)
        empty=np.zeros(num_labels)
        #print(empty)
        
        for i in range(N_test):
            for x in range(num_labels):
                prod=np.prod(likelihood_ratio[x,:]**X_test[i])
                probability=prod*priors_prob[x]
                empty[x]=probability
            #print(empty)
            max=np.argmax(empty)
            array[i]=max
        return array

        #print(N_test)
        
        #raise NotImplementedError


'''
ADDITIONAL EXAMPLES for ratings_stars

ratings_stars: Python list that contains the labels per corresponding Naive Bayes models.

The length of ratings will change depending on which Naive Bayes model we are training.
You are highly encouraged to use a for-loop to iterate over ratings!
------------------------------------------------------------------------------------------------------------------------
Two-label NB model:
ratings_stars = [ratings_less_than_or_equal_to_2, ratings_greater_or_equal_to_3] -- length 2

ratings_less_than_or_equal_to_2: N_ratings_less_than_or_equal_to_2 x D
    where N_ratings_less_than_or_equal_to_2 is the number of reviews that gave an Amazon
    product a 1 or 2-star rating and D is the number of features (we use the word count as the feature)

ratings_greater_or_equal_to_3: N_ratings_greater_or_equal_to_3 x D
    where N_ratings_greater_or_equal_to_3 is the number of reviews that gave an Amazon
    product a 3, 4, or 5-star rating and D is the number of features (we use the word count as the feature)
------------------------------------------------------------------------------------------------------------------------
Three-label NB model:
ratings_stars = [ratings_less_than_or_equal_to_2, ratings_3, ratings_greater_or_equal_to_4] -- length 3

ratings_less_than_or_equal_to_2: N_ratings_less_than_or_equal_to_2 x D
    where N_ratings_less_than_or_equal_to_2 is the number of reviews that gave an Amazon
    product a 1 or 2-star rating and D is the number of features (we use the word count as the feature)

ratings_3: N_ratings_3 x D
    where N_ratings_3 is the number of reviews that gave an Amazon
    product a rating a 3-star and D is the number of features (we use the word count as the feature)

ratings_greater_or_equal_to_4: N_ratings_greater_or_equal_to_4 x D
    where N_ratings_greater_or_equal_to_4 is the number of reviews that gave an Amazon
    product a 4 or 5-star rating and D is the number of features (we use the word count as the feature)
------------------------------------------------------------------------------------------------------------------------
Four-label NB model:
ratings_stars = [ratings_less_than_or_equal_to_2, ratings_3, ratings_4, ratings_5] -- length 4

ratings_less_than_or_equal_to_2: N_ratings_less_than_or_equal_to_2 x D
    where N_ratings_less_than_or_equal_to_2 is the number of reviews that gave an Amazon
    product a 1 or 2-star rating and D is the number of features (we use the word count as the feature)

ratings_3: N_ratings_3 x D
    where N_ratings_3 is the number of reviews that gave an Amazon
    product a 3-star rating and D is the number of features (we use the word count as the feature)

ratings_4: N_ratings_4 x D
    where N_ratings_4 is the number of reviews that gave an Amazon
    product a 4-star rating and D is the number of features (we use the word count as the feature)

ratings_5: N_ratings_5 x D
    where N_ratings_5 is the number of reviews that gave an Amazon
    product a 5-star rating and D is the number of features (we use the word count as the feature)
------------------------------------------------------------------------------------------------------------------------
Five-label NB model:
ratings_stars = [ratings_1, ratings_2, ratings_3, ratings_4, ratings_5] -- length 5

ratings_1: N_ratings_1 x D
    where N_ratings_1 is the number of reviews that gave an Amazon
    product a 1-star rating and D is the number of features (we use the word count as the feature)

ratings_2: N_ratings_2 x D
    where N_ratings_2 is the number of reviews that gave an Amazon
    product a 2-star rating and D is the number of features (we use the word count as the feature)

ratings_3: N_ratings_3 x D
    where N_ratings_3 is the number of reviews that gave an Amazon
    product a 3-star rating and D is the number of features (we use the word count as the feature)

ratings_4: N_ratings_4 x D
    where N_ratings_4 is the number of reviews that gave an Amazon
    product a 4-star rating and D is the number of features (we use the word count as the feature)

ratings_5: N_ratings_5 x D
    where N_ratings_5 is the number of reviews that gave an Amazon
    product a 5-star rating and D is the number of features (we use the word count as the feature)
------------------------------------------------------------------------------------------------------------------------

*** Note, the variables inside the list are just placeholders. Do not reference with these variable names! ***
'''