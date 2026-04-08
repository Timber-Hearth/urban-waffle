from io import TextIOWrapper
from typing import Dict, List

class Tokenizer:
    data_location = "data/corpus.txt"

    def __init__(self):
        self.words: List[str] = []
        self.sentences: List[str] = []
        self.words_count: Dict = {}
        self.vocabulary: List[str] = []
        
        self.__SetTokens()
        self.__SetWordCount()
        self.__SetVocabulary()
        
        self.word_to_idx = { word: idx for idx, word in enumerate(self.vocabulary) }
        self.idx_to_word = { idx: word for idx, word in enumerate(self.vocabulary) }
    
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
                sentences_result = [line.rstrip("\n") for line in sentences_result]
                if sentences_result:
                    self.sentences = sentences_result
                if "\ufeff" in self.sentences[0]:
                    self.sentences[0] = self.sentences[0].lstrip("\ufeff")
            
        __SetWords()
        __SetSentence()
        
    def __SetWordCount(self):
        if not self.words or not self.sentences:
            self.__SetTokens()
        else:
            for item in self.words:
                if item in self.words_count:
                    self.words_count[item] += 1
                else:
                    self.words_count[item] = 1
    
    def __SetVocabulary(self):
        self.vocabulary = list(self.words_count.keys())
        a = 10
        
    def ListWordToIndex(self, targets: List[str]) -> List:
        result = []
        for v in targets:
            result.append(self.word_to_idx.get(v))
        return result