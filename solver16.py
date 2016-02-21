import sys
import heapq

'''
    This program may cost about 10 seconds to get the result,
    so please wait for a while.

    Our heuristic function is calculate the distance position from goal board firstly.
    For example: 
   [[1,  14, 3,  4],    row1    => (0, 0)    (0, -1)    (0, 0)    (0, 0)
    [8,  2,  6,  7],    row2    => (-1, 0)   (0, -1)    (-1, 0)   (-1, 0)
    [9,  5, 11, 12],    row3    => (0, 0)    (-1,-1)    (0, 0)    (0, 0)
    [13, 10, 15, 16]]   row4    => (0, 0)    (0, -1)    (0, 0)    (0, 0)

    Then, for each row, we calculate the maximum of x minus the minimum of x,
    it is 0 + 1 + 1 + 0 = 2;

    Then, for each column, we calculate the maximum of x minus the minimum of y,
    it is 0 + 0 + 0 + 0 = 0;

    So the heuristic function is eaqual to 2.

    The result of 
    
    5 7 8 1
    10 2 4 3
    6 9 11 12
    15 13 14 16

    "L4 R1 D4 R2 L3 D2 U4 L2 D3 L3 U2 R3 L4 U3 R4 D3"
'''


class Board(object):
    
    __slots__ = ('tile_container', 'action_list')

    def __init__(self, tile_container=None):
        self.tile_container = tile_container or []
        self.action_list = []

    def __eq__(self, board):
        for i in range(4):
            for j in range(4):
                if self.tile_container[i][j] != board.tile_container[i][j]:
                    return False
        return True

    def __hash__(self):
        hash_code = 1
        for row in self.tile_container:
            hash_code *= hash(tuple(row))
        return hash_code

    def copy(self):
        # 
        tile_container = []
        for raw in self.tile_container:
            tile_container.append(raw[:])

        new_board = Board(tile_container=tile_container)
        new_board.action_list = self.action_list[:]

        return new_board

    def move_right(self, row):
        self.action_list.append("R%s"%row)
        index = row - 1
        self.tile_container[index] = [self.tile_container[index][-1]]\
                                            + self.tile_container[index][:-1]

    def move_left(self, row):
        index = row - 1
        self.action_list.append("L%s"%row)
        self.tile_container[index] = self.tile_container[index][1:]\
                                        + [self.tile_container[index][0]]

    def move_up(self, column):
        index = column - 1
        self.action_list.append("U%s"%column)
        t0 = self.tile_container[0][index]
        t1 = self.tile_container[1][index]
        t2 = self.tile_container[2][index]
        t3 = self.tile_container[3][index]

        self.tile_container[0][index] = t1
        self.tile_container[1][index] = t2
        self.tile_container[2][index] = t3
        self.tile_container[3][index] = t0


    def move_down(self, column):
        index = column - 1
        self.action_list.append("D%s"%column)
        t0 = self.tile_container[0][index]
        t1 = self.tile_container[1][index]
        t2 = self.tile_container[2][index]
        t3 = self.tile_container[3][index]

        self.tile_container[0][index] = t3
        self.tile_container[1][index] = t0
        self.tile_container[2][index] = t1
        self.tile_container[3][index] = t2

    def _cal_distance_pos(self, p1, p2):
        x = p1[0] - p2[0]
        if x == 3:
            x = -1
        if x == -3:
            x = 1
        y = p1[1] - p2[1]
        if y == 3:
            y = -1
        if y == -3:
            y = 1

        return x,y

    def get_heuristic(self):
        sum_num = 0
        dis_matrix = []
        for i in range(4):
            row = []
            for j in range(4):
                pos = i, j
                number = self.tile_container[i][j]
                goal_pos = ((number-1)/4, (number-1)%4)
                row.append(self._cal_distance_pos(pos, goal_pos))
            dis_matrix.append(row)

        for row in dis_matrix:
            sum_num += max(row, key=lambda x:x[1])[1] - min(row, key=lambda x:x[1])[1]

        for i in range(4):
            colum = [dis_matrix[j][i] for j in range(4)]
            sum_num += max(colum, key=lambda x:x[0])[0] - min(colum, key=lambda x:x[0])[0]
        return sum_num

    def get_f(self):
        return self.get_heuristic() + len(self.action_list)

    def gen_child(self):
        # for row
        for i in range(1, 4+1):
            board = self.copy()
            board.move_left(i)
            yield board
            board = self.copy()
            board.move_right(i)
            yield board

        # for column
        for i in range(1, 4+1):
            board = self.copy()
            board.move_down(i)
            yield board
            board = self.copy()
            board.move_up(i)
            yield board

    @classmethod
    def generate_goal_board(cls):
        board = cls()
        for i in range(4):
            t = [i*4+j for j in range(1,5)]
            board.tile_container.append(t)
        return board

Board.GOAL_BOARD = Board.generate_goal_board()

if __name__ == "__main__":
    print 'This program may cost some time to get the result, so please wait for a while.'
    filename = sys.argv[1]
    tile_container = []
    with open(filename, "r") as f:
        for line in f:
            tile_container.append([int(i) for i in line.split()])

    initial_board = Board(tile_container=tile_container)

    opened = []
    opened_set = set()
    heapq.heapify(opened)
    closed = set()

    heapq.heappush(opened, (initial_board.get_f(), initial_board))
    opened_set.add(initial_board)
    i = 0
    while len(opened):
        _, board = heapq.heappop(opened)
        opened_set.remove(board)
        closed.add(board)

        if board == Board.GOAL_BOARD:
            print " ".join(board.action_list)
            break

        for child_board in board.gen_child():
            if child_board not in closed:
                if child_board in opened_set:
                    if len(child_board.action_list) > len(board.action_list) + 1:
                        heapq.heappush(opened, (child_board.get_f() ,child_board))
                        opened_set.add(child_board)
                elif child_board not in opened_set:
                    heapq.heappush(opened, (child_board.get_f() ,child_board))
                    opened_set.add(child_board)
            else:
                del child_board

