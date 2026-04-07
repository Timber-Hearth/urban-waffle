from random import uniform
from typing import List

from Core.Tokenizer import Tokenizer


class AutoEmbedding:
    dim = 3
    start_min_rendom = -0.5
    start_max_rendom = 0.5
    
    def __init__(self):
        self.emb: List[List[float]] = []
        
    def InitEmbedding(self, tokenzier: Tokenizer):
        if not tokenzier.vocabulary:
            print("tokenzier.vocabulary not set")
        else:
            for item in tokenzier.vocabulary:
                v1 = uniform(self.start_min_rendom, self.start_max_rendom)
                v2 = uniform(self.start_min_rendom, self.start_max_rendom)
                v3 = uniform(self.start_min_rendom, self.start_max_rendom)
                self.emb.append([v1, v2, v3])