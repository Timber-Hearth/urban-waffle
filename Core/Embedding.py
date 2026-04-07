from random import uniform
from typing import List
from Core.Tokenizer import Tokenizer


class AutoEmbedding:
    dim = 3
    start_min_rendom = -0.5
    start_max_rendom = 0.5
    pull_distance = 0.1
    window = 2
    
    pos_pairs: List[int] = []
    
    def __init__(self, tokenizer: Tokenizer):
        self.emb: List[List[float]] = []
        self.tokenizer: Tokenizer = tokenizer
        if not tokenizer.vocabulary:
            print("tokenzier.vocabulary not set")
        else:
            self.tokenizer = tokenizer
            for item in tokenizer.vocabulary:
                v1 = uniform(self.start_min_rendom, self.start_max_rendom)
                v2 = uniform(self.start_min_rendom, self.start_max_rendom)
                v3 = uniform(self.start_min_rendom, self.start_max_rendom)
                self.emb.append([v1, v2, v3])
        self.pos_pairs = [0] * len(self.tokenizer.words)
                
    def VocaPull(self):
        for single_sentence in self.tokenizer.sentences:
            self.UpdatePos(sentence=single_sentence)
        a = 10
                
    def UpdatePos(self, sentence: str):
        words = sentence.split(" ")
        for i, word in enumerate(words):
            if (self.window - i) ** 2 >= 0:
                for q in range(self.window):
                    index_value = self.tokenizer.word_to_idx.get(words[i - q], -1)
                    if index_value != -1:
                        self.pos_pairs[index_value] = 1
            else:
                for q in range(self.window):
                    index_value = self.tokenizer.word_to_idx.get(words[i - q], -1)
                    if index_value != -1:
                        self.pos_pairs[index_value] = 1