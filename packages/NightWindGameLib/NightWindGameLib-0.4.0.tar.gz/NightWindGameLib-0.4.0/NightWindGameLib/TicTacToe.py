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


def minimax_search(game: Game, state: GameState):
    player = state.to_move

    def max_value(state):
        # 计算子状态中的最大效用值
        if game.terminal_test(state):
            return game.utility(state=state, player=player)
        v = -float('inf')
        for m in game.moves(state):
            v = max(v, min_value(game.transition(state, m)))
        return v

    def min_value(state):
        # 计算子状态中的最小效用值
        if game.terminal_test(state):
            return game.utility(state=state, player=player)
        v = float('inf')
        for m in game.moves(state):
            v = min(v, max_value(game.transition(state, m)))
        return v

    return max(game.moves(state),
               key=lambda m: min_value(game.transition(state, m)))


def random_player(game, state):
    # 随机玩家，随机从允许行动列表中挑选一个行动
    import random
    if game.moves(state):
        return random.choice(tuple(game.moves(state=state)))
    else:
        return None


def human_player(game, state):
    try:
        x = int(input("请输入你的行动位置的x坐标:"))
        y = int(input("请输入你的行动位置的y坐标:"))
        moves = ()
        moves += (x,)
        moves += (y,)
        while moves not in game.moves(state):
            print("输入行动无效!")
            x = int(input("请重新输入你的行动位置的x坐标:"))
            y = int(input("请重新输入你的行动位置的y坐标:"))
            moves = ()
            moves += (x,)
            moves += (y,)

        return moves
    except ValueError:
        print("输入行动无效!")


def strategic_player(search_algorithm, *args, **kwargs):
    # 策略玩家，使用算法搜索最佳行动
    return lambda game, state: search_algorithm(game, state, *args, **kwargs)


class TicTacToe(Game):
    def __init__(self, width=3, height=3, k=3,
                 players=('X', 'O'), to_move='X'):
        self.k = k
        self.players = players
        self.initial = GameState(board=Board(width, height),
                                 to_move=to_move, score=0)
        super().__init__(initial=self.initial, players=self.players)

    def moves(self, state):
        return state.board.blank_squares()

    def transition(self, state, move):
        if move not in self.moves(state):
            return state

        player = state.to_move
        board = state.board.new()
        board[move] = player
        to_move = self.opponent(player)
        score = 0
        if board.k_in_line(self.k, player=player, move=move):
            score = 1 if player == self.initial.to_move else -1

        return GameState(board=board, to_move=to_move, score=score)

    def terminal_test(self, state):
        return not self.moves(state) or state.score != 0

    def utility(self, state, player):
        if player == self.initial.to_move:
            return state.score
        else:
            return -state.score


def ticTacToe():
    minimax_player = strategic_player(minimax_search)
    tic_tac_toe = TicTacToe(players=('X', 'O'), to_move='X')
    first = input("你想先手还是后手？")
    if first == "先手":
        end = tic_tac_toe.play_game(dict(X=human_player, O=minimax_player),
                                    verbose=True)
        result = tic_tac_toe.utility(end, 'X')
        if result == 1:
            print("你赢了！")
        elif result == 0:
            print("平局！")
        elif result == -1:
            print("你输了！")
    else:
        end = tic_tac_toe.play_game(dict(X=minimax_player, O=human_player),
                                    verbose=True)
        result = tic_tac_toe.utility(end, 'O')
        if result == 1:
            print("你赢了！")
        elif result == 0:
            print("平局！")
        elif result == -1:
            print("你输了！")


if __name__ == "__main__":
    ticTacToe()
