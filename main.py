from Core.Embedding import AutoEmbedding
from Core.Tokenizer import Tokenizer


if __name__ == "__main__":
    tokenizer = Tokenizer()
    auto_embedding = AutoEmbedding(tokenizer=tokenizer)
    auto_embedding.VocaPull()
    auto_embedding.save_embeddings("embeddings.json")