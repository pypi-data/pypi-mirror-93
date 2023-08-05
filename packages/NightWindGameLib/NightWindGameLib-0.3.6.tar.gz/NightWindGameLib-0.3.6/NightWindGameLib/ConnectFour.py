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


def minimax_search(game: Game, state: GameState, depth_limit, eval_fn):
    player = state.to_move

    def max_value(state, depth):
        # 计算子状态中的最大效用值
        if game.terminal_test(state):
            return game.utility(state=state, player=player)
        if depth > depth_limit:
            return eval_fn(game, state, player)

        v = -float('inf')
        for m in game.moves(state):
            v = max(v, min_value(game.transition(state, m), depth + 1))
        return v

    def min_value(state, depth):
        # 计算子状态中的最小效用值
        if game.terminal_test(state):
            return game.utility(state=state, player=player)
        if depth > depth_limit:
            return eval_fn(game, state, player)

        v = float('inf')
        for m in game.moves(state):
            v = min(v, max_value(game.transition(state, m), depth + 1))
        return v

    return max(game.moves(state),
               key=lambda m: min_value(game.transition(state, m), 1))


def random_player(game, state):
    # 随机玩家，随机从允许行动列表中挑选一个行动
    import random
    if game.moves(state):
        return random.choice(tuple(game.moves(state=state)))
    else:
        return None


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


def novice_evaluation(game, state, player):
    import random
    return random.choice([float('inf'), -float('inf')])


def improved_evaluation(game, state: GameState, player):
    value = 0
    board = state.board
    center_x, center_y = (board.width + 1) / 2, (board.height + 1) / 2
    for s, p in board.items():
        distance = abs(s[0] - center_x) + abs(s[1] - center_y)
        if p == player:
            value -= distance
        else:
            value += distance

    return value


class ConnectFour(TicTacToe):
    def __init__(self, width=7, height=6, k=4,
                 players=('X', 'O'), to_move='X'):
        super().__init__(width=width, height=height, k=k,
                         players=players, to_move=to_move)

    def moves(self, state):
        return [(x, y) for (x, y) in state.board.blank_squares()
                if y == state.board.height or (x, y + 1) in state.board]


def connectFour():
    novice_player = strategic_player(minimax_search,
                                     depth_limit=4,
                                     eval_fn=novice_evaluation)
    improved_player = strategic_player(minimax_search,
                                       depth_limit=4,
                                       eval_fn=improved_evaluation)
    connect_four = ConnectFour(players=('X', 'O'), to_move='X')
    end = connect_four.play_game(dict(X=improved_player, O=novice_player),
                                 verbose=True)
    print(connect_four.utility(end, 'X'))


if __name__ == "__main__":
    connectFour()

