import argparse
import sys
from typing import List

try:
    import matplotlib.pyplot as plt
    from matplotlib import font_manager, rc
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
except ImportError:
    print("matplotlib가 설치되어 있지 않습니다. 설치하려면: pip install matplotlib")
    sys.exit(1)

from Core.Tokenizer import Tokenizer
from Core.Embedding import AutoEmbedding


def set_korean_font():
    candidates = ["Malgun Gothic", "AppleGothic", "NanumGothic", "Batang", "Arial Unicode MS"]
    available_fonts = {f.name for f in font_manager.fontManager.ttflist}
    for font_name in candidates:
        if font_name in available_fonts:
            rc("font", family=font_name)
            return font_name
    return None


def plot_embeddings_3d(words: List[str], coords: List[List[float]], title: str = "Embedding 3D Visualization"):
    chosen_font = set_korean_font()
    if chosen_font:
        plt.rcParams["axes.unicode_minus"] = False
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    zs = [c[2] for c in coords]

    ax.scatter(xs, ys, zs, s=40, c="blue", alpha=0.8)
    for word, x, y, z in zip(words, xs, ys, zs):
        ax.text(x, y, z, word, size=9, zorder=1, color="black")

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.tight_layout()
    plt.show()


def build_example_embeddings(tokenizer: Tokenizer, model: AutoEmbedding, train: bool, epochs: int):
    if train:
        model.epoch = epochs
        model.VocaPull()
    return model.emb


def prepare_embedding_plot_data(tokenizer: Tokenizer, embeddings: List[List[float]], top: int = 20, words: List[str] = None):
    if not embeddings or len(tokenizer.vocabulary) == 0:
        raise ValueError("임베딩 또는 vocabulary가 비어 있습니다.")

    selected_words: List[str] = []
    selected_coords: List[List[float]] = []

    if words:
        for word in words:
            if word in tokenizer.word_to_idx:
                idx = tokenizer.word_to_idx[word]
                selected_words.append(word)
                selected_coords.append(embeddings[idx])
            else:
                raise ValueError(f"단어를 찾을 수 없음: {word}")
    else:
        for idx, word in enumerate(tokenizer.vocabulary[:top]):
            selected_words.append(word)
            selected_coords.append(embeddings[idx])

    if any(len(coord) != 3 for coord in selected_coords):
        raise ValueError("현재 시각화는 3차원 임베딩만 지원합니다. dim=3으로 설정하세요.")

    return selected_words, selected_coords


def main():
    parser = argparse.ArgumentParser(description="AutoEmbedding 시각화 스크립트")
    parser.add_argument("--top", type=int, default=20, help="시각화할 상위 단어 개수")
    parser.add_argument("--train", action="store_true", help="학습을 수행한 뒤 임베딩을 시각화")
    parser.add_argument("--epochs", type=int, default=1, help="학습 epoch 수 (train 옵션 사용 시)")
    parser.add_argument("--words", nargs="*", help="시각화할 특정 단어 목록")
    args = parser.parse_args()

    tokenizer = Tokenizer()
    model = AutoEmbedding(tokenizer)

    if args.train:
        print(f"학습 시작: epoch={args.epochs}")
        build_example_embeddings(tokenizer, model, train=True, epochs=args.epochs)
    else:
        print("학습 없이 현재 임베딩을 시각화합니다.")

    vocabulary = tokenizer.vocabulary
    embeddings = model.emb

    if not embeddings or len(vocabulary) == 0:
        print("임베딩 또는 vocabulary가 비어 있습니다.")
        return

    selected_words = []
    selected_coords = []

    if args.words:
        for word in args.words:
            if word in tokenizer.word_to_idx:
                idx = tokenizer.word_to_idx[word]
                selected_words.append(word)
                selected_coords.append(embeddings[idx])
            else:
                print(f"단어를 찾을 수 없음: {word}")
    else:
        for idx, word in enumerate(vocabulary[: args.top]):
            selected_words.append(word)
            selected_coords.append(embeddings[idx])

    if any(len(coord) != 3 for coord in selected_coords):
        print("현재 시각화는 3차원 임베딩만 지원합니다. dim=3으로 설정하세요.")
        return

    print(f"시각화할 단어 수: {len(selected_words)}")
    plot_embeddings_3d(selected_words, selected_coords, title="AutoEmbedding 3D Visualization")


if __name__ == "__main__":
    main()
