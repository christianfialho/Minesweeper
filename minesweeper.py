"""
Minesweeper game and hopefully solver. We shall see.
Author: Christian Fialho 

Much code from CSE251 course, Luc Comoeu
"""

import random

class bcolors:
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC   = '\33[3m'
    BLINK    = '\33[5m'
    BLINK2   = '\33[6m'
    SELECTED = '\33[7m'

    BLACK  = '\33[30m'
    RED    = '\33[31m'
    GREEN  = '\33[32m'
    YELLOW = '\33[33m'
    BLUE   = '\33[34m'
    VIOLET = '\33[35m'
    BEIGE  = '\33[36m'
    WHITE  = '\33[37m'

    BLACKBG  = '\33[40m'
    REDBG    = '\33[41m'
    GREENBG  = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG   = '\33[44m'
    VIOLETBG = '\33[45m'
    BEIGEBG  = '\33[46m'
    WHITEBG  = '\33[47m'

    GREY    = '\33[90m'
    RED2    = '\33[91m'
    GREEN2  = '\33[92m'
    YELLOW2 = '\33[93m'
    BLUE2   = '\33[94m'
    VIOLET2 = '\33[95m'
    BEIGE2  = '\33[96m'
    WHITE2  = '\33[97m'

    GREYBG    = '\33[100m'
    REDBG2    = '\33[101m'
    GREENBG2  = '\33[102m'
    YELLOWBG2 = '\33[103m'
    BLUEBG2   = '\33[104m'
    VIOLETBG2 = '\33[105m'
    BEIGEBG2  = '\33[106m'
    WHITEBG2  = '\33[107m'

tiles = {
    "UNKNOWN": f"{bcolors.UNDERLINE}{              bcolors.GREYBG                 }  {bcolors.ENDC}",
    "0"      : f"{bcolors.UNDERLINE}{              bcolors.BLACKBG                }  {bcolors.ENDC}",
    "1"      : f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.BLACKBG}{bcolors.YELLOW}1 {bcolors.ENDC}",
    "2"      : f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.BLACKBG}{bcolors.GREEN }2 {bcolors.ENDC}",
    "3"      : f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.BLACKBG}{bcolors.BLUE  }3 {bcolors.ENDC}",
    "4"      : f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.BLACKBG}{bcolors.VIOLET}4 {bcolors.ENDC}",
    "5"      : f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.BLACKBG}{bcolors.RED   }5 {bcolors.ENDC}",
    "6"      : f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.BLACKBG}{bcolors.BEIGE }6 {bcolors.ENDC}",
    "7"      : f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.BLACKBG}{bcolors.GREY  }7 {bcolors.ENDC}",
    "8"      : f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.BLACKBG}{bcolors.WHITE }8 {bcolors.ENDC}",
    "BOOM"   : f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.REDBG  }{bcolors.BLACK }✹ {bcolors.ENDC}",
    "MINE"   : f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.GREYBG }{bcolors.RED2 }✹ {bcolors.ENDC}",
    "FLAG"   : f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.GREYBG }{bcolors.WHITE   }⚑ {bcolors.ENDC}",
    "MISFLAG": f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.REDBG  }{bcolors.GREY  }⚑ {bcolors.ENDC}"
}

class Board():

    directions = (
        (1, 0),   # E
        (1, 1),   # SE
        (0, 1),   # S
        (-1, 1),  # SW
        (-1, 0),  # W
        (-1, -1), # NW
        (0, -1),   # N
        (1, -1)   # NE
    )

    def __init__(self, size, n_mines):
        """ Create the instance and the board arrays """
        self.size = size
        self.n_mines = n_mines
        self.board_actual = [[0 for _ in range(size[1])] for _ in range(size[0])] 
        self.board_apparent = [['UNKNOWN' for _ in range(size[1])] for _ in range(size[0])]
        self.unturned_tiles = size[0]*size[1]
        self.playing = True
        self.mode = 'MINE'
        self.is_made = False

    def place_mines(self,safe_r,safe_c):
        """ Place all of the mines into the board """
        for i in range(self.n_mines):
            mine_placed = False
            while not mine_placed:
                row = random.randint(0, self.size[0] - 1)
                col = random.randint(0, self.size[1] - 1)
                if (self.board_actual[row][col] != 9) and not ((safe_r-1 <= row <= safe_r+1) and (safe_c-1 <= col <= safe_c+1)):
                    self.board_actual[row][col] = 9
                    mine_placed = True
                    for dir in self.directions:
                        r = row+dir[0]
                        c = col+dir[1]
                        if 0 <= r < self.size[0] and 0 <= c < self.size[1]:
                            if self.board_actual[r][c] < 9:
                                self.board_actual[r][c] += 1

    def display(self):
        """ Display the board with highlighting """
        print()
        buffer = (3 + self.size[1]*3 - 11 - 9)//2 * ' '
        print(f"{buffer}MINESWEEPER{buffer}{' Mode:' + tiles[self.mode]}")
        print()
        print("   ",end="")
        for col in range(self.size[1]):
            print(f"{col:<3}",end="")
        print()
        for row in range(self.size[0]):
            print(f"{row:>2}| ",end="")
            for col in range(self.size[1]):
                print(tiles[self.board_apparent[row][col]],end=" ")
            print()

    def turn_tile(self,row,col):
        if self.board_apparent[row][col] == 'UNKNOWN':
            # print(row,col)
            n = self.board_actual[row][col]
            if n == 9:
                self.game_over(row,col)
            else:
                self.board_apparent[row][col] = str(n)
                self.unturned_tiles -= 1
                if self.unturned_tiles <= self.n_mines:
                    self.game_over()
                if n == 0:
                    for dir in self.directions:
                        r = row+dir[0]
                        c = col+dir[1]
                        if 0 <= r < self.size[0] and 0 <= c < self.size[1]:
                            self.turn_tile(r,c)

    def flag_tile(self,row,col):
        if self.board_apparent[row][col] == 'UNKNOWN':
            self.board_apparent[row][col] = 'FLAG'
        elif self.board_apparent[row][col] == 'FLAG':
            self.board_apparent[row][col] = 'UNKNOWN'
        
    def touch_tile(self,row,col):
        if (self.board_apparent[row][col] == 'UNKNOWN' or 
            self.board_apparent[row][col] == 'FLAG'):
            if self.mode == 'MINE':
                self.turn_tile(row,col)
            else:
                self.flag_tile(row,col)
        elif int(self.board_apparent[row][col])>0:
            self.multi_touch(row,col)

    def n_neighbors_like(self,row,col,like='UNKNOWN'):
        n = 0
        for dir in self.directions:
            r = row+dir[0]
            c = col+dir[1]
            if 0 <= r < self.size[0] and 0 <= c < self.size[1]:
                if self.board_apparent[r][c] == like:
                    n += 1
        return n

    def multi_touch(self,row,col):
        tiles_changed = 0
        flags = self.n_neighbors_like(row,col,like='FLAG')
        if flags == self.board_actual[row][col]:
            for dir in self.directions:
                r = row+dir[0]
                c = col+dir[1]
                if 0 <= r < self.size[0] and 0 <= c < self.size[1]:
                    if self.board_apparent[r][c] == 'UNKNOWN':
                        self.turn_tile(r,c)
                        tiles_changed += 1
        else:
            unknowns = self.n_neighbors_like(row,col,like='UNKNOWN')
            if flags + unknowns == self.board_actual[row][col]:
                for dir in self.directions:
                    r = row+dir[0]
                    c = col+dir[1]
                    if 0 <= r < self.size[0] and 0 <= c < self.size[1]:
                        if self.board_apparent[r][c] == 'UNKNOWN':
                            self.flag_tile(r,c)
                            tiles_changed += 1
        return tiles_changed > 0

    def toggle_mode(self):
        if self.mode == 'MINE':
            self.mode = 'FLAG'
        else:
            self.mode = 'MINE'

    def game_over(self,row=None,col=None):
        if row == None:
            disp = self.board_apparent
            for row in range(self.size[0]):
                for col in range(self.size[1]):
                    if disp[row][col]=='UNKNOWN':
                        disp[row][col] = 'FLAG'
                print()
            print("\t\tYou won!")
            print()
        else:
            real = self.board_actual
            disp = self.board_apparent
            disp[row][col] = 'BOOM'
            for row in range(self.size[0]):
                for col in range(self.size[1]):
                    if disp[row][col]=='FLAG' and real[row][col]!=9:
                        disp[row][col] = 'MISFLAG'
                    if disp[row][col]=='UNKNOWN' and real[row][col]==9:
                        disp[row][col] = 'MINE'
                print()
            print("\t\tYou lose!")
            print()
        self.playing = False
        
    def simple_solver_step(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self.multi_touch(row,col):
                    return True
        
    def play(self):
        # print()
        # print("Instructions: enter a column, followed by a space, followed by a row")
        # print("enter M to toggle between Mine and Flag modes")
        # print(bcolors.BLINK2+"\t\tPress Enter"+bcolors.ENDC)
        # _ = input()

        self.display()
        while self.playing:
            ip = input("Col row > ").upper()
            if ip:
                if ip[0] == "\\":
                    eval(ip[1:])
                elif ip == "M":
                    print("toggled")
                    self.toggle_mode()
                elif ip == "S":
                    print(f"Steps solved: {self.simple_solver_step()*1}")
                else:
                    coords = ip.split()
                    col = int(coords[0])
                    row = int(coords[1])
                    if not self.is_made:
                        self.place_mines(safe_r=row,safe_c=col)
                        self.is_made = True
                    if 0<=row<self.size[0] and 0<=col<self.size[1]:
                        self.touch_tile(row,col)
            self.display()
            if not self.playing:
                if input("Press Enter to play again, Q to quit > ").upper()=="Q":
                    self.playing = False
                else:
                    self.__init__(self.size,self.n_mines)
                    self.display()
            

def main():
    m,n,mines = 16,9,8
    print("How many colums, row and mines?")
    ip = input("Default: 16 x 9, 8 > ")
    if ip:
        stgs = list(map(lambda x: int(x), ip.split()))
        m,n,mines = stgs[0],stgs[1],stgs[2]

    board = Board((n,m),mines)
    board.play()

if __name__ == '__main__':
    main()
