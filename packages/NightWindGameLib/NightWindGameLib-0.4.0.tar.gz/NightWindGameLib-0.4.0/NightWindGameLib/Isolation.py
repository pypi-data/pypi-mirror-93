class Game:
    def __init__(self, initial, players=()):
        # 创建游戏初始状态，记录两个玩家信息
        self.initial = initial
        self.players = players

    def opponent(self, player):
        # 返回当前玩家的对手玩家
        return self.players[(self.players.index(player) + 1) % 2]

    def moves(self, state):
        # 返回在给定状态下可以采取的行动
        raise NotImplementedError

    def transition(self, state, move):
        # 返回玩家执行给定行动后到达的游戏状态
        raise NotImplementedError

    def terminal_test(self, state):
        # 判断游戏状态是否为终结状态
        return not self.moves(state=state)

    def utility(self, state, player):
        # 返回给定状态对于给定玩家的效用值
        raise NotImplementedError

    def play_game(self, strategies: dict, verbose=False):
        # 实现两个玩家轮流进行游戏的过程
        state = self.initial
        if verbose:
            print("初始状态:")
            print(state)
            print()
        while not self.terminal_test(state):
            player = state.to_move
            move = strategies[player](self, state)
            state = self.transition(state, move)
            if verbose:
                print(f"玩家{player} 行动:{move}")
                print(state)
                print()
        return state


class GameState:
    def __init__(self, board, to_move, score=None):
        self.board = board
        self.to_move = to_move
        self.score = score

    def __repr__(self):
        return self.board.__repr__()


class Board(dict):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.squares = {(x, y) for x in range(1, width + 1)
                        for y in range(1, height + 1)}

    def __repr__(self):
        # 以字符串形式显示棋盘状态
        rows = []
        for y in range(1, self.height + 1):
            row = []
            for x in range(1, self.width + 1):
                row.append(self.get((x, y), "·"))
            rows.append(" ".join(row))
        return "\n".join(rows)

    def blank_squares(self):
        # 返回可以落子的地方
        return self.squares - set(self)

    def new(self):
        # 新建空的棋盘实例， 复制原来棋盘的棋子状态信息
        new_board = self.__class__(width=self.width, height=self.height)
        new_board.update(self)
        return new_board

    def k_in_line(self, k, player, move):
        # 如果玩家落子后连成一条长度为k的线则返回True
        def in_line(move, delta):
            (delta_x, delta_y) = delta
            x, y = move
            n = 0
            while self.get((x, y)) == player:
                n += 1
                x, y = x + delta_x, y + delta_y
            x, y = move
            while self.get((x, y)) == player:
                n += 1
                x, y = x - delta_x, y - delta_y
            n -= 1
            return n >= k

        return any(in_line(move, delta)
                   for delta in ((0, 1), (1, 0), (1, 1), (1, -1)))


class Isolation(Game):
    pass


class IsolationState(GameState):
    def __init__(self, board, player_squares, to_move):
        self.board = board
        self.player_squares = player_squares
        self.to_move = to_move
        super().__init__(board=self.board, to_move=self.to_move)

    def open_moves(self, player):
        return self.board.open_squares(self.player_squares[player])


class IsolationBoard(Board):
    def open_squares(self, square):
        open_squares = []
        for delta in ((0, 1), (1, 0), (1, 1), (1, -1)):
            (delta_x, delta_y) = delta
            x, y = square
            x, y = x + delta_x, y + delta_y
            if self.in_board((x, y)) and not self.get((x, y)):
                open_squares.append((x, y))

            x, y = square
            x, y = x - delta_x, y - delta_y
            if self.in_board((x, y)) and not self.get((x, y)):
                open_squares.append((x, y))

        return open_squares

    def in_board(self, square):
        x, y = square
        return 1 <= x <= self.width and 1 <= y <= self.height
