import copy
import time
MIN_PLAYER = 0
MAX_PLAYER = 1

''' 
### Iterative Deepening Negamax with Alpha-Beta Pruning: 
    http://stackoverflow.com/questions/13549594/iterative-deepening-negamax-with-alpha-beta-pruning
    

    We used basic Alpha-Beta Pruning algorithm. We setup backup value and 
    constrain the depth=5 in case there is not enough time.
    For backup value, we calculate the open moves for each state.
'''



class Board(object):
    __slots__ = ["number_container", "move"]
    def __init__(self):
        self.number_container = [] # list of list
        self.move = None # a tuple, contain i, j

    def get_score(self):
        number_open_moves = self.number_open_moves()
        min_number = float("infinity")
        for child_board in self.possible_board():
            value = number_open_moves - child_board.number_open_moves()
            min_number = min(min_number, value)
        return min_number

    def number_open_moves(self):
        open_moves = 0
        for i in xrange(Board.N):
            for j in xrange(Board.N):
                if self.number_container[i][j] == 1:
                    continue
                board = self.copy()
                board.number_container[i][j] = 1
                if not board.is_lose():
                    open_moves += 1
                # board.display()
        return open_moves

    def possible_board(self):
        for i in xrange(Board.N):
            for j in xrange(Board.N):
                board = self.copy()
                if board.number_container[i][j] == 0:
                    board.number_container[i][j] = 1
                    board.move = i,j
                    if not board.is_lose():
                        yield board

    def copy(self):
        return copy.deepcopy(self)

    # for debug only, delete this one;
    def display(self):
        for number_ls in self.number_container:
            # print "debug:%s"%number_ls
            string = ""
            for number in number_ls:
                if number == 0:
                    string += " _ "
                else:
                    string += " x "
            print string

    def __str__(self):
        string = ""
        for raw in self.number_container:
            for number in raw:
                if number == 0:
                    string += "."
                else:
                    string += "x"
        return string

    def is_losing(self):
        return self.number_open_moves() == 0

    def is_lose(self):
        N = self.__class__.N
        ## check row
        # self.display()
        for row in self.number_container:
            # print "row:%s"%row
            if all(row):
                return True

        ## check column
        for i in range(N):
            column = [_row[i] for _row in self.number_container]
            # print "column:%s"%column
            if all(column):
                return True

        ## check right down diagonal
        r_d = [self.number_container[i][i] for i in range(N)]
        # print "diagonal:%s"%r_d
        if all(r_d):
            return True

        ## check left down diagonal
        l_d = [self.number_container[i][N-i-1] for i in range(N)]
        # print "diagonal:%s"%l_d
        if all(l_d):
            return True

    @classmethod
    def parse_from_input(cls, n, input_str=".x......x"):
        board = cls()
        cls.N = n
        row = []
        for _str in input_str:
            if _str == ".":
                row.append(0)
            elif _str == "x":
                row.append(1)

            if len(row) == n:
                board.number_container.append(row)
                row = []

        return board

def alpha_beta(alpha, beta, board, player, depth=0, timeout=-1, start_time=0):
    time_used = time.time() - start_time
    if depth == 5 or (timeout!=-1 and (timeout - time_used) < 0.1):
        if player == MAX_PLAYER:
            return board.get_score()
        else:
            return -board.get_score()
            
    if board.is_losing():
        if player == MAX_PLAYER:
            return Board.N*Board.N
        else:
            return -Board.N*Board.N

    score = 0
    for child_board in board.possible_board():
        time_used = time.time() - start_time
        if (timeout!=-1 and (timeout - time_used) < 0.1):
            break

        if Board.N < 5:
            score = score + alpha_beta(alpha, beta, child_board, player^1, depth=depth+1, 
                                                    timeout=timeout, start_time=start_time)
        else:
            score = alpha_beta(alpha, beta, child_board, player^1, depth=depth+1, 
                                                    timeout=timeout, start_time=start_time)
        if player == MAX_PLAYER:
            if score > alpha:
                alpha = score
            if alpha >= beta:
                break
        else:
            if score < beta:
                beta = score
            if alpha >= beta:
                break

    if player == MAX_PLAYER:
        return alpha
    else:
        return beta


if __name__ == "__main__":
    import sys
    import time
    start_time = time.time()
    n, input_board, timeout = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
    board = Board.parse_from_input(n, input_str=input_board)
    print "Thinking! Please wait...\n"
    best_score = float("-infinity")
    best_board = None

    for child_board in board.possible_board():
        time_used = time.time() - start_time
        if (timeout!=-1 and (timeout - time_used) < 0.1):
            break

        score = alpha_beta(float('-infinity'), float('infinity'), 
                                            child_board,
                                            MAX_PLAYER,
                                            timeout=timeout,
                                            start_time=start_time)
        if best_score < score:
            best_score = score
            best_board = child_board


    print "Hmm, I'd recommend putting your pebble at row %s, column %s."%(best_board.move[0]+1, best_board.move[1]+1)
    print "New board:"
    print(best_board)
    print "time usage:%s"%(time.time() - start_time)








