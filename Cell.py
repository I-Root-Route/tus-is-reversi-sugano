import Const as C


class Cell:
    def __init__(self):
        self.__reset()

    def __setStone(self, stone, x, y):
        # 石を置く。
        # Args:
        #   x (int) : x座標
        #   y (int) : y座標
        self.__cell[x - 1][y - 1] = stone

    def getStone(self, x, y):
        # 指定座標の石を返す
        # Args:
        #   x (int)        : x座標
        #   y (int)        : y座標
        # Returns:
        #   int : BLACK or WHITE のいずれかを返す
        return self.__cell[x - 1][y - 1]

    def getCount(self, stone):
        # 石の個数を返す
        # Args:
        #   stone (int) : 石
        # Returns:
        #   int : 個数を返す
        count = 0
        for i in range(1, 9):
            for j in range(1, 9):
                if self.getStone(i, j) == stone:
                    count += 1
        return count

    def getIsAblePutList(self, stone):
        # 石を置ける場所をリストで返す
        # Args:
        #   stone (int) : 石
        # Returns:
        #   (int,int) list : 石を置ける座標をタプルで表現し、そのリストを返す。
        ans = []
        for i in range(1, 9):
            for j in range(1, 9):
                if self.isAblePut(stone, i, j):
                    ans.append((i, j))

        return ans

    def putStone(self, stone, x, y):
        # 指定した方向に石を置く。その際ひっくり返す。
        # Args:
        #   stone (int)    : 置く石の種類
        #   x (int)        : x座標
        #   y (int)        : y座標
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                f = lambda n: n + i
                g = lambda n: n + j
                if self.__isAblePutDirection(stone, f, g, x, y):
                    self.__setStone(Cell.flip(stone), x, y)
                    self.__putStoneDirection(stone, f, g, x, y)

    def __putStoneDirection(self, stone, f, g, x, y):
        # 指定した方向に石を置く
        # Args:
        #   stone (int)    : 置く石の種類
        #   f (int -> int) : x軸の差分
        #   f (int -> int) : y軸の差分
        #   x (int)        : x座標
        #   y (int)        : y座標
        if self.getStone(x, y) == stone:
            return
        self.__setStone(stone, x, y)
        self.__putStoneDirection(stone, f, g, f(x), g(y))

    def isAblePut(self, stone, x, y):
        # 石を置けるかどうかを判定する
        # Args:
        #   stone (int)    : 置く石の種類
        #   x (int)        : x座標
        #   y (int)        : y座標
        # Returns:
        #   bool : Trueなら置ける。Falseは置けない。
        if self.getStone(x, y) != C.BLANK:
            return False

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                f = lambda x: x + i
                g = lambda y: y + j
                if self.__isAblePutDirection(stone, f, g, x, y):
                    return True
        return False

    def __isAblePutDirection(self, stone, f, g, x, y):
        # 指定した方向に石を置けるかどうかを判定する
        # Args:
        #   stone (int)    : 置く石の種類
        #   f (int -> int) : x軸の差分
        #   f (int -> int) : y軸の差分
        #   x (int)        : x座標
        #   y (int)        : y座標
        # Returns:
        #   bool : Trueなら置ける。Falseは置けない。
        def isOut(m, n):
            # 座標がセルの外に出ているかどうかの判定
            # Args:
            #   m (int) : x座標
            #   n (int) : y座標
            # Returns:
            #   bool : Trueなら外側。Falseなら内側
            return not (1 <= m <= C.SIZE) or not (1 <= n <= C.SIZE)

        def func(m, n):
            # 2個目以降、同色の石が続くかどうかを判定
            # Args:
            #   m (int) : x座標
            #   n (int) : y座標
            # Returns:
            #   bool : Trueなら置ける。Falseなら置けない。
            if isOut(f(m), g(n)):
                return False

            if self.getStone(f(m), g(n)) == stone:
                return True
            elif self.getStone(f(m), g(n)) == Cell.flip(stone):
                return func(f(m), g(n))

        if isOut(f(x), g(y)):
            return False
        if self.getStone(f(x), g(y)) != Cell.flip(stone):
            return False

        return func(f(x), g(y))

    def __reset(self):
        # セルのリセットを行う
        self.__cell = [[C.BLANK for i in range(C.SIZE)] for j in range(C.SIZE)]
        self.__setStone(C.BLACK, 4, 4)
        self.__setStone(C.BLACK, 5, 5)
        self.__setStone(C.WHITE, 5, 4)
        self.__setStone(C.WHITE, 4, 5)

    def createClone(self):
        # 現在のセルのクローンを生成
        # Returns:
        #   Cell : Cellクラスのインスタンス
        ans = Cell()

        for i in range(C.SIZE):
            for j in range(C.SIZE):
                ans.__setStone(self.getStone(i + 1, j + 1), i + 1, j + 1)

        return ans

    @staticmethod
    def flip(stone):
        # ひっくり返した石を返す。
        # Args:
        #   stone (int) : BLACK or WHITEのどちらかを受け取る
        # Returns:
        #   int : BLACK or WHITE のいずれかを返す
        if stone == C.BLACK:
            return C.WHITE
        elif stone == C.WHITE:
            return C.BLACK
        else:
            print("caution!")
            return 0