import unittest
from tests.test_utils import get_sample_pdf_with_labels, get_sample_pdf, get_sample_sdf, get_sample_pdf_with_extra_cols, get_sample_pdf_with_no_text_col ,get_sample_spark_dataframe
from nlu import *

class TestYake(unittest.TestCase):

    def test_yake_model(self):
        #setting meta to true will output scores for keywords. Lower scores are better
        df = nlu.load('yake',verbose=True).predict('What a wonderful day! Arnold schwanenegger is the Terminator and he wants to get to the American chopper', metadata=True)
        print(df.columns)
        print(df)
        print(df[['keywords_classes', 'keywords_score_confidence']])


        df = nlu.load('yake',verbose=True).predict('What a wonderful day! Arnold schwanenegger is the Terminator and he wants to get to the American chopper', metadata=False)
        print(df.columns)
        print(df)
        print(df[['keywords_classes', 'keywords_confidences']])



        df = nlu.load('yake',verbose=True).predict('What a wonderful day! Arnold schwanenegger is the Terminator and he wants to get to the American chopper', output_level='token')
        print(df.columns)
        print(df[['keywords_classes', 'keywords_confidences']])
        df = nlu.load('yake',verbose=True).predict('What a wonderful day! Arnold schwanenegger is the Terminator and he wants to get to the American chopper', output_level='chunk')
        print(df.columns)
        print(df[['keywords_classes', 'keywords_confidences']])
        #Column name of confidence changed if yake at same or not at same output level!
        df = nlu.load('yake',verbose=True).predict('What a wonderful day! Arnold schwanenegger is the Terminator and he wants to get to the American chopper', output_level='document')
        print(df.columns)
        print(df[['keywords_classes', 'keywords_confidences']])

    def test_quick(self):
        p = '/home/loan/tmp/tripadvisor_hotel_reviews.csv'
        df = pd.read_csv(p)
        res = nlu.load('en.ner.aspect_sentiment').predict(df.iloc[10:50].text)


        print(res)
if __name__ == '__main__':
    unittest.main()

