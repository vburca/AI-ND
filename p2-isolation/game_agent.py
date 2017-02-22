"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return wtf(game, player)

def wtf(game, player):
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    board_size = game.width * game.height

    if game.move_count < board_size * .3:
        return own_moves
    elif game.move_count < board_size * .7:
        return own_moves / (board_size + opp_moves)
    else:
        return move_prev_diff_weighted(game, player)

def conditional_score1(game, player):
    board_size = game.width * game.height

    # if covered less than 30%
    if game.move_count < board_size * .2:
        return len(game.get_legal_moves(player))
    else:
        return move_prev_diff_weighted(game, player, 2)

def move_diff_weighted(game, player, weight=1):
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - weight * opp_moves)

opp_moves_previous = 0
def move_prev_diff_weighted(game, player, weight=1):
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves + weight * (opp_moves_previous - opp_moves))

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        global opp_moves_previous
        opp_moves = len(game.get_legal_moves(game.get_opponent(self)))

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        if len(legal_moves) == 0:
            return (-1, -1)

        # just for safety, grab a random move from the legal ones initially
        best_move = random.choice(legal_moves)

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring

            if self.iterative:
                depth = 1
                # dummy initialization
                best_score = 0
                # cutoff condition: realistically, since we maximize, it could only get to +inf
                while (best_score is not float("-inf")) and (best_score is not float("inf")):
                    best_score, best_move = max((best_score, best_move), self.search(game, depth))
                    depth += 1
            else:
                _, best_move = self.search(game)
        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def search(self, game, depth=None):
        if depth is None:
            depth = self.search_depth
        if self.method == 'minimax':
            return self.minimax(game, depth)
        else:
            return self.alphabeta(game, depth)

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # initialize dummy best move
        best_move = (-1, -1)
        # initialize dummy best score
        best_score = float("-inf")

        if depth == 0:
            return (self.score(game, self), best_move)

        if maximizing_player:
            best_score = float("-inf") # this is for clarity purposes, since it's already -inf
            for move in game.get_legal_moves(self):
                score = self.__min_value_mm(game.forecast_move(move), depth - 1)
                # check if we get a better score for the current move
                # if we do, update the best_score and the best_move with the current move
                if score > best_score:
                    best_score = score
                    best_move = move
        else: # else, if we are the minimizing player, do the same thing but minimize the scores
            best_score = float("inf")
            for move in game.get_legal_moves(self):
                score = self.__max_value_mm(game.forecast_move(move), depth - 1)
                # check if we get a better score for the current move
                # if we do, update the best_score and the best_move with the current move
                if score < best_score:
                    best_score = score
                    best_move = move

        return (best_score, best_move)

    def __max_value_mm(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # if we reached a "terminal" state in terms of the depth we wanted to
        # look at, return the current score at this node
        if depth == 0:
            return self.score(game, self)

        # assume best score is -inf, and try to maximize it
        best_score = float("-inf")

        for move in game.get_legal_moves():
            # here we maximize the best score across the other possible branching min-nodes
            best_score = max(best_score, self.__min_value_mm(game.forecast_move(move), depth - 1))

        return best_score

    def __min_value_mm(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # if we reached a "terminal" state in terms of the depth we wanted to
        # look at, return the current score at this node
        if depth == 0:
            return self.score(game, self)

        # assume best score is +inf, and try to minimize it
        best_score = float("inf")

        for move in game.get_legal_moves():
            # here we minimize the best score across the other possible branching max-nodes
            best_score = min(best_score, self.__max_value_mm(game.forecast_move(move), depth - 1))

        return best_score

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # initialize dummy best move
        best_move = (-1, -1)
        # initialize dummy best score
        best_score = float("-inf")

        if depth == 0:
            return (self.score(game, self), best_move)

        if maximizing_player:
            best_score = float("-inf") # this is for clarity purposes, since it's already -inf
            for move in game.get_legal_moves(self):
                score = self.__min_value_ab(game.forecast_move(move), depth - 1, alpha, beta)
                # check if we get a better score for the current move
                # if we do, update the best_score and the best_move with the current move
                if score > best_score:
                    best_score = score
                    best_move = move

                if best_score >= beta:
                    return (best_score, best_move)
                alpha = max(alpha, best_score)
        else: # else, if we are the minimizing player, do the same thing but minimize the scores
            best_score = float("inf")
            for move in game.get_legal_moves(self):
                score = self.__max_value_ab(game.forecast_move(move), depth - 1, alpha, beta)
                # check if we get a better score for the current move
                # if we do, update the best_score and the best_move with the current move
                if score < best_score:
                    best_score = score
                    best_move = move

                if best_score <= alpha:
                    return (best_score, best_move)
                beta = min(beta, best_score)

        return (best_score, best_move)

    def __max_value_ab(self, game, depth, α, β):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # if we reached a "terminal" state in terms of the depth we wanted to
        # look at, return the current score at this node
        if depth == 0:
            return self.score(game, self)

        # assume best score is -inf, and try to maximize it
        best_score = float("-inf")

        for move in game.get_legal_moves():
            # here we maximize the best score across the other possible branching min-nodes
            best_score = max(best_score, self.__min_value_ab(game.forecast_move(move), depth - 1, α, β))

            # check if we can prune the remaining nodes
            if best_score >= β:
                # if our best score is higher than the maximum score that the above min-node would
                # consider, prune the remaining nodes
                return best_score

            # update the α value, useful for potential lower min-nodes
            α = max(α, best_score)

        return best_score

    def __min_value_ab(self, game, depth, α, β):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # if we reached a "terminal" state in terms of the depth we wanted to
        # look at, return the current score at this node
        if depth == 0:
            return self.score(game, self)

        # assume best score is +inf, and try to minimize it
        best_score = float("inf")

        for move in game.get_legal_moves():
            # here we minimize the best score across the other possible branching max-nodes
            best_score = min(best_score, self.__max_value_ab(game.forecast_move(move), depth - 1, α, β))

            # check if we can prune the remaining nodes
            if best_score <= α:
                # if our best score is lower than the minimum score that the above max-node would
                # consider, prune the remaining nodes
                return best_score

            # update the β value, useful for potential lower max-nodes
            β = min(β, best_score)

        return best_score
