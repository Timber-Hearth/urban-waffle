from Core.Embedding import AutoEmbedding
from Core.Tokenizer import Tokenizer


if __name__ == "__main__":
    tokenizer = Tokenizer()
    auto_embedding = AutoEmbedding()
    auto_embedding.InitEmbedding(tokenzier = tokenizer)
    print("test")