from matplotlib import pyplot as plt
import pandas as pd


if __name__ == '__main__':
    dataset = pd.read_csv('records/data.csv')
    X = dataset.iloc[:, 0].values
    open_cell = dataset.iloc[:, 1].values
    even = dataset.iloc[:, 2].values
    law = dataset.iloc[:, 3].values
    stables = dataset.iloc[:, 4].values
    black_scores = dataset.iloc[:, 5].values
    white_scores = dataset.iloc[:, 6].values
    black_fin_score = dataset.iloc[-1, 5]
    white_fin_score = dataset.iloc[-1, 6]
    plt.plot(X, open_cell, marker='o', color='red', label="Openness Score")
    plt.plot(X, even, marker='v', color='blue', label="Even Theory Score")
    plt.plot(X, law, marker='x', color='green', label='Law Of The Move Score')
    plt.plot(X, stables, marker='v', color='purple', label="Stable Stones Score")
    plt.title(f"Scores of Each Method. FinalResult -> BLACK: {black_fin_score} vs WHITE: {white_fin_score}")
    plt.xlabel("Game Progress")
    plt.ylabel("BLACK------------------------------SCORE------------------------------WHITE")
    plt.legend()
    plt.show()
