import Const as C
# import Print as P


class EvenTheory(object):
    def __init__(self):
        self.total_score_black = 0
        self.total_score_white = 0
        self.total_score_black_list = []
        self.total_score_white_list = []

    @staticmethod
    def get_stones_in_contact_with_blanks(g):
        temp_neighbors = []
        neighbors = []

        if g.getCount(C.BLACK) + g.getCount(C.WHITE) < 34:
            # 偶数理論は終盤の戦略のため、計算量抑制の観点から合計が40石以下の時は使用しない
            return None
        blank_list = []
        for i in range(1, 9):
            for j in range(1, 9):
                if g.getStone(i, j) == C.BLANK:
                    blank_list.append((i, j))

        # あるブランクの隣がブランクだったらin_contactに格納 -> ブランクの塊を検出する
        for position in blank_list:
            in_contact = [position]
            x = position[0]
            y = position[1]
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    elif (x + i, y + j) in blank_list:
                        in_contact.append((x + i, y + j))
            blank_list.remove(position)
            temp_neighbors.append(in_contact)

        for position in temp_neighbors:  # 単独のブランクは無視する
            if len(position) == 1:
                temp_neighbors.remove(position)

        for group in temp_neighbors:  # 互いに素でないグループは合体させる
            for i in range(len(temp_neighbors)):
                if not set(group).isdisjoint(set(temp_neighbors[i])):
                    pos = list(set(group + temp_neighbors[i]))
                    if pos not in neighbors:
                        neighbors.append(pos)

        for i in range(len(neighbors)):  # ある集合が別の集合の部分集合の時、それを削除する
            for j in range(len(neighbors)):
                if set(neighbors[i]) > set(neighbors[j]):
                    neighbors[j] = []

        for _ in range(2):  # 上のforループで生成された空リストを削除する
            for pos in neighbors:
                if not pos:
                    neighbors.remove(pos)

        return neighbors

    def update_theory_score(self, g, x, y, t):
        even_score = -1
        odd_score = 1
        move = (x, y)
        result = self.get_stones_in_contact_with_blanks(g)
        if result is None:
            return None
        else:
            for res in result:
                if move in res:
                    if len(res) % 2 == 0:
                        if t == C.BLACK:
                            self.total_score_black += even_score
                            self.total_score_white -= even_score
                        elif t == C.WHITE:
                            self.total_score_white += even_score
                            self.total_score_black -= even_score
                    elif len(res) % 2 == 1:
                        if t == C.BLACK:
                            self.total_score_black += odd_score
                            self.total_score_white -= odd_score
                        elif t == C.WHITE:
                            self.total_score_white += odd_score
                            self.total_score_black -= odd_score

        self.total_score_black_list.append(self.total_score_black)
        self.total_score_white_list.append(self.total_score_white)
        return {"黒偶数": self.total_score_black_list, "白偶数": self.total_score_white_list}


class TheLawOfTheMove(object):
    def __init__(self):
        self.nb_put_list_black = []
        self.nb_put_list_white = []

    def nb_able_put_list(self, g, t):
        able_put_list = g.getIsAblePutList(t)

        if t == C.BLACK:
            self.nb_put_list_black.append(len(able_put_list))
        elif t == C.WHITE:
            self.nb_put_list_white.append(len(able_put_list))

        if len(self.nb_put_list_black) - len(self.nb_put_list_white) == 2:
            self.nb_put_list_black[-1] = self.nb_put_list_black[-1] + self.nb_put_list_black[-2]
            del self.nb_put_list_black[-2]
            self.nb_put_list_white.append(0)
        elif len(self.nb_put_list_black) - len(self.nb_put_list_white) == -2:
            self.nb_put_list_white[-1] = self.nb_put_list_white[-1] + self.nb_put_list_white[-2]
            del self.nb_put_list_white[2]
            self.nb_put_list_white.append(0)

        return {"黒着手": self.nb_put_list_black, "白着手": self.nb_put_list_white}


class StableStones(object):
    def __init__(self):
        self.stable_stones_black = []
        self.stable_stones_white = []
        self.nb_stable_stones_black_list = []
        self.nb_stable_stones_white_list = []
        self.nb_stable_stones_score_list = []
        self.edge_left = [(1, i) for i in range(1, C.SIZE + 1)]
        self.edge_right = [(C.SIZE, i) for i in range(1, C.SIZE + 1)]
        self.edge_top = [(i, 1) for i in range(1, C.SIZE + 1)]
        self.edge_bottom = [(i, C.SIZE) for i in range(1, C.SIZE + 1)]
        self.edges = [self.edge_left, self.edge_right, self.edge_top, self.edge_bottom]

    def update_stable_stone(self, g):
        blank_score = [0 for _ in range(len(self.edges))]
        filled_edges = []
        if g.getCount(C.BLACK) + g.getCount(C.WHITE) < 35:
            return None

        for i, pos in enumerate(self.edges):
            for coordinate in pos:
                if g.getStone(coordinate[0], coordinate[1]) == C.BLANK:
                    blank_score[i] = 1
                    break

        for i in range(len(self.edges)):
            if blank_score[i] == 0:
                filled_edges.append(self.edges[i])

        for pos in filled_edges:
            for coordinate in pos:
                if g.getStone(coordinate[0], coordinate[1]) == C.BLACK:
                    if coordinate not in self.stable_stones_black:
                        self.stable_stones_black.append(coordinate)
                elif g.getStone(coordinate[0], coordinate[1]) == C.WHITE:
                    if coordinate not in self.stable_stones_white:
                        self.stable_stones_white.append(coordinate)
        self.nb_stable_stones_black_list.append(len(self.stable_stones_black))
        self.nb_stable_stones_white_list.append(len(self.stable_stones_white))
        return {"黒確定": self.nb_stable_stones_black_list, "白確定": self.nb_stable_stones_white_list}


class Openness(object):
    def __init__(self):
        self.open_cell_list_black = []
        self.open_cell_list_white = []

    def openness(self, cell, stone, pos_x, pos_y, t):
        c = cell.createClone()
        cNext = cell.createClone()

        openCell = 0
        cellList = []

        cNext.putStone(stone, pos_x, pos_y)

        # P.NormalPrint().printCell(c)
        # P.NormalPrint().printCell(cNext)

        for i in range(8):
            for j in range(8):
                if c.getStone(i, j) != cNext.getStone(i, j) and c.getStone(i, j) != C.BLANK:
                    cellList.append((i, j))

        stone_list = []

        for k in cellList:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue

                    f = lambda n: n + i
                    g = lambda n: n + j

                    if (f(k[0]), g(k[1])) not in stone_list:
                        stone_list.append((f(k[0]), g(k[1])))

        for x, y in stone_list:
            if cNext.getStone(x, y) == C.BLANK:
                openCell += 1

        if t == C.BLACK:
            self.open_cell_list_black.append(openCell)
        elif t == C.WHITE:
            self.open_cell_list_white.append(openCell)

        if len(self.open_cell_list_black) - len(self.open_cell_list_white) == 2:
            self.open_cell_list_black[-1] = self.open_cell_list_black[-1] + self.open_cell_list_black[-2]
            del self.open_cell_list_black[-2]
            self.open_cell_list_white.append(0)
        elif len(self.open_cell_list_black) - len(self.open_cell_list_white) == -2:
            self.open_cell_list_white[-1] = self.open_cell_list_white[-1] + self.open_cell_list_white[-2]
            del self.open_cell_list_white[2]
            self.open_cell_list_black.append(0)

        return {"黒開放度": self.open_cell_list_black, "白開放度": self.open_cell_list_white}
