import numpy as np
import re
import csv
import time
from concurrent.futures import ProcessPoolExecutor

import Const as C
from Cell import Cell
from Analyze import Openness, TheLawOfTheMove, EvenTheory, StableStones

openness = Openness()
the_law_of_the_move = TheLawOfTheMove()
even_theory = EvenTheory()
stable_stones = StableStones()


def calc_score(dic, key1, key2, base):
    black_score_list = dic[key1]
    white_score_list = dic[key2]
    final_result = []
    if base == "black":
        final_result = np.array(black_score_list) - np.array(white_score_list)
    elif base == "white":
        final_result = np.array(white_score_list) - np.array(black_score_list)
    return list(final_result)


class ProcessTextFile(object):
    def __init__(self, text_file, line_index):
        self.text_file = text_file
        self.line = []
        self.line_index = line_index

    def get_line(self):
        for i, line in enumerate(self.text_file):
            if i == self.line_index - 1:
                self.line.append(line)
                break
        return self.line
        # for line in self.text_file:
        #     self.line.append(line)
        # return self.line

    @staticmethod
    def mark_off_lines(single_line):
        coordinates = re.split('(..)', single_line)[1::2]
        return coordinates


class ReproductionGame(object):
    def __init__(self, record):
        self.__cell = Cell()
        self.turn = C.BLACK
        self.record = record
        self.b = []
        self.w = []

    def play(self):
        while True:
            if not self.__cell.getIsAblePutList(self.turn):
                self.turn = Cell.flip(self.turn)
                if not self.__cell.getIsAblePutList(self.turn):
                    return self.__gameSet()
                continue

            while True:
                x = int(self.record[0][0])
                y = int(self.record[0][1])
                if self.__cell.isAblePut(self.turn, x, y):
                    openness_list = openness.openness(self.createCellClone(), self.turn, x, y, self.turn)
                    even_list = even_theory.update_theory_score(self, x, y, self.turn)
                    self.__cell.putStone(self.turn, x, y)
                    self.record.pop(0)
                    move_list = the_law_of_the_move.nb_able_put_list(self, self.turn)
                    stables_list = stable_stones.update_stable_stone(self)
                    if self.getCount(C.BLACK) + self.getCount(C.WHITE) >= 35:
                        self.b.append(self.getCount(C.BLACK))
                        self.w.append(self.getCount(C.WHITE))
                    self.turn = Cell.flip(self.turn)
                    if len(self.record) == 0:
                        array_conc_pre = [
                            list(range(1, len(calc_score(stables_list, "黒確定", "白確定", "white")) + 1)),
                            calc_score(openness_list, "黒開放度", "白開放度", "black"),
                            calc_score(even_list, "黒偶数", "白偶数", "white"),
                            calc_score(move_list, "黒着手", "白着手", "white"),
                            calc_score(stables_list, "黒確定", "白確定", "white"),
                            self.b,
                            self.w,
                            np.array(self.w) - np.array(self.b),
                            np.cumsum(np.array(openness_list["黒開放度"])) - np.cumsum(np.array(openness_list["白開放度"])),
                            np.cumsum(np.array(even_list["白偶数"])) - np.cumsum(np.array(even_list["黒偶数"])),
                            np.cumsum(np.array(move_list["白着手"])) - np.cumsum(np.array(move_list["黒着手"])),
                        ]
                        array_conc_ndarray = np.array(array_conc_pre)
                        ndarray_T = array_conc_ndarray.T
                        # print(ndarray_T)
                        # with open('records/data.csv', 'w') as f:
                        with open('records/res.csv', 'a') as f:
                            writer = csv.writer(f)
                            writer.writerows([ndarray_T[-1]])

                    break
                else:
                    print("ERROR!")
                    print("座標 (x,y) = " + str(x) + "," + str(y) + " に石を置けません...")

    def __gameSet(self):
        b = self.__cell.getCount(C.BLACK)
        w = self.__cell.getCount(C.WHITE)
        return C.BLACK if w < b else C.WHITE if w > b else C.BLANK

    def createCellClone(self):
        # Gameが持つCellのクローンを返す
        # Returns:
        #   Cell : フィールド__cellのクローン
        return self.__cell.createClone()

    def getStone(self, x, y):
        # 指定座標の石を返す
        # Args:
        #   x (int)        : x座標
        #   y (int)        : y座標
        # Returns:
        #   int : BLACK or WHITE のいずれかを返す
        return self.__cell.getStone(x, y)

    def getStonePos(self, pos):
        return self.__cell.getStone(pos[0], pos[1])

    def getIsAblePutList(self, stone):
        # 石を置ける場所をリストで返す
        # Args:
        #   stone (int) : 石
        # Returns:
        #   (int,int) list : 石を置ける座標をタプルで表現し、そのリストを返す。
        return self.__cell.getIsAblePutList(stone)

    def getCount(self, stone):
        # 石の個数を返す
        # Args:
        #   stone (int) : 石
        # Returns:
        #   int : 個数を返す
        return self.__cell.getCount(stone)


class Battle:
    def __init__(self, record, N):
        self.record = record
        self.N = N

    def start(self):
        s = time.time()

        with ProcessPoolExecutor(max_workers=8) as executor:
            futures = []

            for _ in range(self.N):
                g = ReproductionGame(
                    self.record
                )
                future = executor.submit(g.play)
                futures.append(future)

        b = 0
        w = 0
        d = 0

        for e in futures:
            r = e.result()

            if r == C.BLACK:
                b += 1
            elif r == C.WHITE:
                w += 1
            else:
                d += 1

        print(" RESULT OF " + str(self.N) + " BATTLES")
        print("")
        print(f"BLACK : {b} wins")
        print(" | win rate : " + str((b / (b + w + d)) * 100) + "%")
        print("")
        print(f"WHITE: {w} wins")
        print(" | win rate : " + str((w / (b + w + d)) * 100) + "%")
        print("")
        print("DRAW")
        print(" | " + str(d) + " times...")

        elapsedTime = time.time() - s
        print()
        print("elapsed time : " + str(elapsedTime) + " [sec]")


if __name__ == '__main__':
    line_i = input("game.txtにある行番号を指定してください: ")
    my_file = open('records/game.txt')
    process_text_file = ProcessTextFile(my_file, int(line_i))
    first_line = process_text_file.get_line()
    line_record = process_text_file.mark_off_lines(first_line[0])
    Battle(line_record, 1).start()
