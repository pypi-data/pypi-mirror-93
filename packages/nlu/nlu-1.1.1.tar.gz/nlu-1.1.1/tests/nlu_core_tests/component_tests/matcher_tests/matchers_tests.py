import unittest
from tests.test_utils import get_sample_pdf_with_labels, get_sample_pdf, get_sample_sdf, get_sample_pdf_with_extra_cols, get_sample_pdf_with_no_text_col ,get_sample_spark_dataframe
from nlu import *

class MatcherTests(unittest.TestCase):

    def test_date_matcher(self):
        pipe = nlu.load('match.datetime', verbose=True )
        df = pipe.predict('2020 was a crazy year but wait for October 1. 2020')
        print(df.columns)

        #others to test :
        # 'en.match.pattern'
        # 'en.match.chunks'

    def test_pattern_matcher(self):
        pipe = nlu.load('match.pattern', verbose=True )
        df = pipe.predict('2020 was a crazy year but wait for October 1. 2020')
        print(df.columns)


    def test_chunk_matcher(self):
        pipe = nlu.load('match.chunks', verbose=True )
        df = pipe.predict('2020 was a crazy year but wait for October 1. 2020')
        print(df.columns)


    def test_quick(self):
        # Type 1 Error, Somehow input columns are wrong in elmma, but only for non EN!
        tricky_refs = [
            "bh.lemma" ,
            "am.lemma" ,
            "bn.lemma" ,
            "ja.lemma" ,

        ]
        # res = nlu.load('am.lemma', verbose=True).predict("C̄hạn chxb ney t̄hạ̀w læa yel lī̀")
        res = nlu.load('bh.lemma', verbose=True).predict("C̄hạn chxb ney t̄hạ̀w læa yel lī̀")

        print(res)
        # exit()
        # for r in refs :
        #     res =nlu.load(r).predict("Hello world I love you <3")
        #     print(f"REF : {r}  =  {res}" )
        # print(res)
if __name__ == '__main__':
    unittest.main()

