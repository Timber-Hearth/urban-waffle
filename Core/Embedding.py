from math import exp
from random import uniform
from typing import List
import random
from Core.Tokenizer import Tokenizer


class AutoEmbedding:
    dim = 3
    start_min_rendom = -0.5
    start_max_rendom = 0.5
    pull_distance = 0.1
    window = 2
    negative_count = 2
    
    epoch = 100000
    learning_rate = 0.001
    
    pos_flag: int = 1
    neg_flag: int = 0
    pos_pairs: List = []
    neg_pairs: List = []
    
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
        self.pos_pairs = []
        self.neg_pairs = []
                
    def VocaPull(self):
        for i in range(self.epoch):
            self.pos_pairs = []
            self.neg_pairs = []
            for single_sentence in self.tokenizer.sentences:
                words = single_sentence.split(" ")
                self.SetPosNeg(words=words)
            self.UpdateVocaVector()
                
    def SetPosNeg(self, words: List[str]):
        for i, v in enumerate(words):
            slice_start: int = i - self.window if i - self.window > 0 else 0
            slice_end: int = i + self.window if i + self.window <= len(words) else len(words)
            in_window_tokens: list = words[slice_start : slice_end + 1]
            current_core_index: int = self.tokenizer.word_to_idx.get(v)
            
            neg_list: List = self.tokenizer.GetNegWords(do_not_include_this=in_window_tokens, neg_size=self.negative_count)
            neg_list = self.tokenizer.ListWordToIndex(neg_list)
            for out_of_window in neg_list:
                self.neg_pairs.append([current_core_index, out_of_window, self.neg_flag])

            in_window_tokens.remove(v)
            
            in_window_index: List[int] = self.tokenizer.ListWordToIndex(in_window_tokens)
            for in_window in in_window_index:
                self.pos_pairs.append([current_core_index, in_window, self.pos_flag])
                
    def UpdateVocaVector(self):
        update_targets: List[List[int, int, int]] = self.neg_pairs + self.pos_pairs
        for item in update_targets:
            center: List[int, int, int] = self.emb[item[0]]
            target: List[int, int, int] = self.emb[item[1]]
            flag: int = item[2]
            
            dot = sum(center[i] * target[i] for i in range(self.dim))
            sigmoid = 1 / (1 + exp(-dot))
            
            delta = sigmoid - flag
            
            for i in range(self.dim):
                center[i] -= self.learning_rate * (delta * target[i])
                target[i] -= self.learning_rate * (delta * center[i])