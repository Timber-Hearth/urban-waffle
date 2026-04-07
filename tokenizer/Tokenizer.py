from io import TextIOWrapper
from typing import List

class Tokenizer:
    data_location = "data/corpus.txt"

    def __init__(self):
        self.words: List[str] = []
        self.sentence: List[str] = []
        self.__SetTokens()
    
    def GetTokens(self):
        if not self.words:
            self.__SetTokens()
        return self.words
            
    def __SetTokens(self):
        def __SetWords():
            with open(self.data_location, "r", encoding="utf-8") as f:
                words_result: List[str] = f.read().split()
                words_result[0] = words_result[0].lstrip('\ufeff')
                if words_result:
                    self.words = words_result
            
        def __SetSentence():
            with open(self.data_location, "r", encoding="utf-8") as f:
                sentences_result: List[str] = f.readlines()
                if sentences_result:
                    self.sentences = sentences_result
            
        __SetWords()
        __SetSentence()
        