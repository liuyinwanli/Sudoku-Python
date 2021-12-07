import copy
class Solver:
    def __init__(self):
        self.colDict = dict()
        self.rowDict = dict()
        self.sudoku = list()
        self.ans = list()
    def solve(self):
        self.initSudoku()
        self.displaySudoku()
        self.initDL()
        if self.solveDL(copy.deepcopy(self.rowDict),copy.deepcopy(self.colDict)):
            print("++++++++++++++++++++++成功+++++++++++++++++++++")
            self.solveSudoku()
            self.displaySudoku()
    def solveSudoku(self):
        for answer in self.ans:
            li = self.rowDict[answer]
            x = li[0]//9
            y = li[0]%9
            num = answer%9
            self.sudoku[x][y] = num + 1
    def initSudoku(self):
        with open("./data.txt") as f:
            row = list()
            for line in f.readlines():
                row = []
                for num in line.strip().split(" "):
                    row.append(int(num))
                self.sudoku.append(row)
    def displaySudoku(self):
        for line in self.sudoku:
            for element in line:
                print(element,end = " ")
            print()
    def initColDict(self):
        for index in range(0,9*9*4):
            self.colDict[index] = list()
    def addRow(self,x,y,num):
        locs = self.loc(x,y,num)
        self.rowDict[locs[0]] = locs[1:]
        for index in locs[1:]:
            self.colDict[index].append(locs[0])

    def loc(self,x,y,num):
        return [(x*9+y)*9+num,x*9+y,81*1+x*9+num,81*2+y*9+num,81*3+((x//3)*3+y//3)*9+num]
    def initDL(self):
        self.initColDict()
        for x in range(0,9):
            for y in range(0,9):
                num = self.sudoku[x][y]
                if num == 0:
                    for index in range(0,9):
                        self.addRow(x,y,index)
                else:
                    self.addRow(x,y,num-1)
    def catchRowsByRow(self,row_key,RD,CD):
        ret = set()
        for col_key in RD[row_key]:
            for r_k in CD[col_key]:
                ret.add(r_k)
        return ret
    def pro(self,C):
        less = 81*9
        index = 0
        for key in C.keys():
            if len(C[key]) < less:
                less = len(C[key])
                index = key
        return index
    def solveDL(self,RD,CD):
        R = None
        C = None
        flag = False
        if len(RD) == 0 and len(CD) == 0:
            flag = True
        elif self.isNull(CD):
            falg = False
        else:
            proRow = self.pro(CD)
            for row_key in CD[proRow]:
                R = copy.deepcopy(RD)
                C = copy.deepcopy(CD)
                rows = self.catchRowsByRow(row_key,R,C)
                for row in rows:
                    for col in R[row]:
                        C[col].remove(row)
                for row in rows:
                    del R[row]
                for col_key in RD[row_key]:
                    del C[col_key]
                flag = self.solveDL(R,C)
                if flag:
                    self.ans.append(row_key)
                    break
        return flag
    def isNull(self,CC):
        ret = False
        for col in CC.values():
            if len(col) == 0:
                ret = True
        return ret
if __name__ == "__main__":
    solve = Solver()
    solve.solve()
