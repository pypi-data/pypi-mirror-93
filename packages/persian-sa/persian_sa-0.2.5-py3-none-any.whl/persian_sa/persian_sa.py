from __future__ import division, print_function, unicode_literals
import sklearn
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import numpy as np
import pickle, os



np.random.seed(42)
svm_model = os.path.join(os.path.dirname(__file__), './data/svmmodel.pkl')
preprocessing_pipline = os.path.join(os.path.dirname(__file__), './data/preprocessingpipline.pkl')

svm_model = pickle.load(open(svm_model, 'rb'))
preprocess_pipeline = pickle.load(open(preprocessing_pipline, 'rb'))



class persian_sa():
    '''
        Predicts sentiment of a given Persian text.
        Returns class number if return_class_label is set True.
            1 - "0" for Negative!
            2 - "1" for Positive!
    '''

    def predict_sentiment(predict_obj, return_class_label = False):
        p_class = svm_model.predict(preprocess_pipeline.transform([predict_obj]).toarray())
        if return_class_label:
            return p_class[0]
        return "Positive!" if p_class[0] > 0 else "Negative!"


