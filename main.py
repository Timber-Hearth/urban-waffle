from Core.Embedding import AutoEmbedding
from Core.Tokenizer import Tokenizer
from visualize_embedding import prepare_embedding_plot_data, plot_embeddings_3d



if __name__ == "__main__":
    tokenizer = Tokenizer()
    auto_embedding = AutoEmbedding(tokenizer=tokenizer)
    auto_embedding.VocaPull()
    
    words, coords = prepare_embedding_plot_data(tokenizer, auto_embedding.emb, top=100)
    plot_embeddings_3d(words, coords)