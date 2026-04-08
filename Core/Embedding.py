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
            words = single_sentence.split(" ")
            self.UpdatePos(words=words)
            self.UpdateNeg(words=words)
        a = 10
                
    def UpdatePos(self, words: List[str]):
        positive_pairs = []
        for i, v in enumerate(words):
            slice_start: int = i - self.window if i - self.window > 0 else 0
            slice_end: int = i + self.window if i + self.window <= len(words) else len(words)
            in_window_tokens: list = words[slice_start : slice_end + 1]
            in_window_tokens.remove(v)
            
            in_window_index: List[int] = self.tokenizer.ListWordToIndex(in_window_tokens)
            current_core_index: int = self.tokenizer.word_to_idx.get(v)
            
            positive_pairs.append([current_core_index, in_window_index])
            
    def UpdateNeg(self, words: List[str]):
        pass