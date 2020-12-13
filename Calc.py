from Reproduction import ReproductionGame, Battle, ProcessTextFile
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import csv


def calc(i):
    my_file = open('records/game.txt')
    process_text_file = ProcessTextFile(my_file, i)
    first_line = process_text_file.get_line()
    line_record = process_text_file.mark_off_lines(first_line[0])
    Battle(line_record, 1).start()


class ResAnalysis(object):
    def __init__(self):
        self.dataframe = pd.read_csv('records/res.csv')
        self.stable_stones = pd.Series(self.dataframe.iloc[:, 4].values)
        self.white_score = pd.Series(self.dataframe.iloc[:, 6].values)
        self.black_score = pd.Series(self.dataframe.iloc[:, 5].values)
        self.white_minus_black = pd.Series(self.dataframe.iloc[:, 7].values)
        self.even_theory = pd.Series(self.dataframe.iloc[:, 9].values)
        self.nb_counts = pd.Series(self.dataframe.iloc[:, 10].values)
        self.openness = pd.Series(self.dataframe.iloc[:, 8].values)

    def calc_cov(self):
        # print(self.stable_stones.corr(self.white_score))
        print(self.even_theory.corr(self.white_score))

    def gen_overall(self):
        count = 0
        for row in self.white_minus_black:
            if row > 0:
                count += 1
            else:
                continue

        return {
            "白の勝率": count / len(self.white_minus_black),
            "白の平均確定石数": np.cumsum(np.array(self.stable_stones))[-1] / len(self.stable_stones),
            "白の平均偶数理論スコア": np.cumsum(np.array(self.even_theory))[-1] / len(self.even_theory),
            "白の平均着手スコア": np.cumsum(np.array(self.nb_counts))[-1] / len(self.nb_counts),
            "白の平均開放度": np.cumsum(np.array(self.openness))[-1] / len(self.openness),
        }


if __name__ == '__main__':
    # データ分析 相関係数の算出とグラフ化
    # print(ResAnalysis().calc_cov())
    # plt.scatter(ResAnalysis().even_theory, ResAnalysis().white_score)
    # plt.show()

    overall_result = ResAnalysis().gen_overall()
    overall_result_list = [
        [overall_result["白の勝率"]],
        [overall_result["白の平均確定石数"]],
        [overall_result["白の平均偶数理論スコア"]],
        [overall_result["白の平均着手スコア"]],
        [overall_result["白の平均開放度"]]
    ]

    with open("records/overall_result.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerows(np.array(overall_result_list).T)

    # データ集めのコード
# for index in range(1, 51):
#     #     try:
#     #         print(calc(index))
#     #     except ValueError as e:
#     #         continue
