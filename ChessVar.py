# Author: Jesus Rodriguez
# GitHub username: J-Rodriguez10
# Date: 5/29/24
# Description: This program writes a class named ChessVar for playing an abstract board game that is a variant of
# chess--atomic chess.

class ChessVar:
    """
    This class created the game board and keeps track of chess pieces, player turn, and state of the game.
    """

    def __init__(self):
        """
        Initializes the chess game. Creates the board, game state, and turns private data members.
        """
        self._board = self._create_board()
        self._game_state = "UNFINISHED"
        self._turn = "WHITE"

        self._white_king_pos = "e1"
        self._black_king_pos = "e8"

    def _create_board(self):
        """
        Create the chess board with the chess pieces in place. The chess board should be
        """
        # using a dictionary instead of a 2D array since its easier to move around board given a key instead of indexes
        board = {}

        # white pieces
        board['a1'] = Rook('white', 'a1')
        board['b1'] = Knight('white', 'b1')
        board['c1'] = Bishop('white', 'c1')
        board['d1'] = Queen('white', 'd1')
        board['e1'] = King('white', 'e1')
        board['f1'] = Bishop('white', 'f1')
        board['g1'] = Knight('white', 'g1')
        board['h1'] = Rook('white', 'h1')
        for letter in 'abcdefgh':
            board[letter + '2'] = Pawn('white', letter + '2')

        # black pieces
        board['a8'] = Rook('black', 'a8')
        board['b8'] = Knight('black', 'b8')
        board['c8'] = Bishop('black', 'c8')
        board['d8'] = Queen('black', 'd8')
        board['e8'] = King('black', 'e8')
        board['f8'] = Bishop('black', 'f8')
        board['g8'] = Knight('black', 'g8')
        board['h8'] = Rook('black', 'h8')
        for letter in 'abcdefgh':
            board[letter + '7'] = Pawn('black', letter + '7')

        # populating emtpy squares
        for letter in "abcdefgh":
            for num in "3456":
                board[f"{letter}{num}"] = None

        return board

    def print_board(self):
        """
        Prints the current state of the chess board.
        """

        print(" | a b c d e f g h |  ")
        print("=====================")

        for num in "87654321":
            print(f"{num}|", end="")
            for letter in "abcdefgh":

                if self._board[f"{letter}{num}"] is None:
                    ascii_art = "·"
                else:
                    ascii_art = self._board[f"{letter}{num}"].get_ascii_art()

                print(" " + ascii_art, end="")
            print(f" |{num}")

        print("=====================")
        print(" | a b c d e f g h |  ")

    def get_game_state(self):
        """
        Returns the current state of the game "returns 'UNFINISHED', 'WHITE_WON', 'BLACK_WON'".
        """
        return self._game_state

    def make_move(self, move_from, move_to):
        """
        Takes in two strings that represents the placement on a chess board (like "b2" or " b4") and moves
        that given chess piece from move_from to move_to. Before making the move, it checks to see if that chess piece
        move is valid. If it is, it will move the piece and possibly cause an "explosion". If it isn't, it will return
        False.
        """

        # 0) check if game is still active
        if self.get_game_state() != "UNFINISHED":
            return False

        # 1) gather data
        move_from = move_from.lower()
        move_to = move_to.lower()

        # 2) validate the move
        # - checking if coordinates are within bounds
        if move_from not in self._board or move_to not in self._board:
            return False

        # - checking if position at move_from has a chess piece and whether it's that color's turn
        chess_piece = self.get_piece_at(move_from)
        if chess_piece is None or chess_piece.get_color() != self._turn:
            return False

        # - final check: checking to see if movement pattern is valid for that given chess piece
        if not chess_piece.is_move_valid(move_from, move_to, self._board):
            return False

        # 3) handle move: either an explosion will happen or the piece just made a simple move
        opposing_piece = self.get_piece_at(move_to)

        # - there is an opposing piece and that chess piece is an opposite colors
        if opposing_piece and opposing_piece.get_color() != self._turn:
            # guard clause to prevent kings from exploding:
            if isinstance(chess_piece, King):
                return False

            self._handle_explosion(move_from, move_to)  # explosion happened
        else:
            self._board[move_from] = None
            self._board[move_to] = chess_piece
            chess_piece.set_position(move_to)
            if isinstance(chess_piece, King):
                self._update_king_position(chess_piece.get_color(), move_to)

        # 4) toggle turn and update
        self._turn = "BLACK" if self._turn == "WHITE" else "WHITE"
        self._update_game_state()

        # 5) confirm move
        return True

    def get_piece_at(self, position):
        """
        Returns the chess piece at a given position. Will return None if there are no pieces at that position.
        """
        return self._board[f"{position.lower()}"]

    def _update_game_state(self):
        """
        Updates the game state to one of these conditions: "UNFINISHED", "WHITE_WON", or "BLACK_WON"
        """
        is_white_king_alive = isinstance(self.get_piece_at(self._white_king_pos), King)
        is_black_king_alive = isinstance(self.get_piece_at(self._black_king_pos), King)

        if not is_white_king_alive:
            self._game_state = "BLACK_WON"
        elif not is_black_king_alive:
            self._game_state = "WHITE_WON"
        else:
            self._game_state = "UNFINISHED"

    def _update_king_position(self, color, new_position):
        """
        Updates the position of a given King
        """
        new_position.lower()

        if color == "WHITE":
            self._white_king_pos = new_position
        else:
            self._black_king_pos = new_position

    def _handle_explosion(self, move_from, explosion_origin):
        """
        This function explodes the captured and the capturee, as well as the 8 squares around the capture origin. Pawns
        are not affected by the explosion radius, unless they were involved in the capture.
        """
        origin_letter, origin_number = explosion_origin
        exploded_squares = []

        # iterating over the 3x3 area and adding that square's key to the exploded_squares list
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x, y) != (0,0):
                    new_letter = chr(ord(origin_letter) + x)
                    new_number = str(int(origin_number) + y)
                    key = new_letter + new_number
                    if key in self._board:
                        exploded_squares.append(key)

        # removing the 8 squares around the origin (unless it's a pawn)
        for key in exploded_squares:
            chess_piece = self.get_piece_at(key)
            if chess_piece and not isinstance(chess_piece, Pawn):
                self._board[key] = None

        # removing initiator and enemy's chess piece
        self._board[move_from] = None
        self._board[explosion_origin] = None


class Piece:
    """
    This class represent a generic chess piece. These private base data members will be shared with more specific chess
    pieces like king, queen, and pawn for instance.
    """
    def __init__(self, color, position):
        """
        Constructor for the Piece class. This will instantiate the following private data members: color (the color
        of a given chess piece) and a position (the chess piece's position on the chess board)
        """
        self._color = color.upper()
        self._position = position.lower()

    def get_color(self):
        """
        Returns the color of a given chess piece.
        """
        return self._color

    def set_position(self, new_pos):
        """
        Updates the old position to a new position for a chess piece.
        """
        self._position = new_pos.lower()

    def get_ascii_art(self):
        """
        Returns the ascii art associated with that specific chess piece and color.
        """
        raise NotImplementedError("You forgot to implement the 'get_ascii_art()' function")

    def is_move_valid(self, move_from, move_to, board):
        """
        Returns a boolean that tells whether a move from move_from to move_to is valid. This function should be
        overridden.If it isn't, the function should return the built-in "NotImplementedError" exception.
        """
        raise NotImplementedError("You forgot to implement the 'is_move_valid' function")


class King(Piece):
    """
    This class represents the King chess piece.
    Inherited att:
    self._color - the color of the King chess piece
    self._position - the position of the King on the board
    """

    def get_ascii_art(self):
        """
        Returns the ascii art associated with that specific chess piece and color.
        """
        if self._color == "BLACK":
            return "♚"
        else:
            return "♔"

    def is_move_valid(self, move_from, move_to, board):
        """
        Returns a boolean that tells whether a move from move_from to move_to is valid.
        """
        # destructuring the data to make it easier to work with
        old_letter, old_number = move_from
        new_letter, new_number = move_to

        # refining the data to make it easier to work with
        old_number = int(old_number)
        new_number = int(new_number)
        old_unicode = ord(old_letter)
        new_unicode = ord(new_letter)

        # finding acceptable movement
        x_direction = abs(new_unicode - old_unicode)
        y_direction = abs(new_number - old_number)

        # checking to see if the movement is one square in any direction
        if x_direction <= 1 and y_direction <= 1:

            # finally checking to make sure that the destination is clear or belongs to opposing enemy's chess piece
            destination_piece = board.get(move_to)
            if destination_piece is None or destination_piece.get_color() != self._color:
                return True

        return False


class Queen(Piece):
    """
    This class represents the Queen chess piece.
    Inherited att:
    self._color - the color of the Queen chess piece
    self._position - the position of the Queen on the board
    """

    def get_ascii_art(self):
        """
        Returns the ascii art associated with that specific chess piece and color.
        """
        if self._color == "BLACK":
            return "♛"
        else:
            return "♕"

    def is_move_valid(self, move_from, move_to, board):
        """
        Returns a boolean that tells whether a move from move_from to move_to is valid.
        """
        # destructuring the data to make it easier to work with
        old_letter, old_number = move_from
        new_letter, new_number = move_to

        # refining the data to make it easier to work with
        old_number = int(old_number)
        new_number = int(new_number)
        old_unicode = ord(old_letter)
        new_unicode = ord(new_letter)

        # finding acceptable movement
        x_direction = abs(new_unicode - old_unicode)
        y_direction = abs(new_number - old_number)

        # checking to make sure that path is clear:

        # 1) checking for diagonal movement - logic from bishop
        if x_direction == y_direction:
            file_step = 1 if new_unicode > old_unicode else -1
            rank_step = 1 if new_number > old_number else -1
            for i in range(1, x_direction):
                intermediate_file = chr(old_unicode + i * file_step)
                intermediate_rank = old_number + i * rank_step
                if board[f"{intermediate_file}{intermediate_rank}"] is not None:
                    return False

        # 2) checking for vertical movement - logic from rook
        elif old_letter == new_letter:
            step = 1 if new_number > old_number else -1
            for num in range(old_number + step, new_number, step):
                if board[f"{old_letter}{num}"] is not None:
                    return False

        # 3) checking for horizontal movement - logic from rook
        elif old_number == new_number:
            step = 1 if new_unicode > old_unicode else -1
            for unicode_val in range(old_unicode + step, new_unicode, step):
                letter = chr(unicode_val)
                if board[f"{letter}{old_number}"] is not None:
                    return False
        else:
            return False

        # finally checking to make sure that the destination square is clear or belongs to opposing enemy's chess piece
        destination_piece = board.get(move_to)
        if destination_piece is None or destination_piece.get_color() != self._color:
            return True

        return False


class Bishop(Piece):
    """
    This class represents the Bishop chess piece.
        Inherited att:
    self._color - the color of the Bishop chess piece
    self._position - the position of the Bishop on the board
    """

    def get_ascii_art(self):
        """
        Returns the ascii art associated with that specific chess piece and color.
        """
        if self._color == "BLACK":
            return "♝"
        else:
            return "♗"

    def is_move_valid(self, move_from, move_to, board):
        """
        Returns a boolean that tells whether a move from move_from to move_to is valid.
        """

        # destructuring the data to make it easier to work with
        old_letter, old_number = move_from
        new_letter, new_number = move_to

        # refining the data to make it easier to work with
        old_number = int(old_number)
        new_number = int(new_number)
        old_unicode = ord(old_letter)
        new_unicode = ord(new_letter)

        # finding acceptable movement
        x_direction = abs(new_unicode - old_unicode)
        y_direction = abs(new_number - old_number)

        # bishops only move diagonally
        if old_letter != new_letter and old_number != new_number:

            # finding the step direction for the letter(x-axis) or number(y-axis)
            letter_step = 1 if new_unicode > old_unicode else -1
            number_step = 1 if new_number > old_number else -1

            # check each square along the path for any other pieces
            for i in range(1, x_direction):
                # forming the proper key
                key_letter = chr(old_unicode + i * letter_step)
                key_number = old_number + i * number_step
                # checking to see if square is skip-able
                if board[f"{key_letter}{key_number}"] is not None:
                    return False

            # finally checking the destination square
            destination_piece = board.get(move_to)
            if destination_piece is None or destination_piece.get_color() != self._color:
                return True

        return False


class Knight(Piece):
    """
    This class represents the Knight chess piece.
    Inherited att:
    self._color - the color of the Knight chess piece
    self._position - the position of the Knight on the board
    """

    def get_ascii_art(self):
        """
        Returns the ascii art associated with that specific chess piece and color.
        """
        if self._color == "BLACK":
            return "♞"
        else:
            return "♘"

    def is_move_valid(self, move_from, move_to, board):
        """
        Returns a boolean that tells whether a move from move_from to move_to is valid.
        """
        # destructuring the data to make it easier to work with
        old_letter, old_number = move_from
        new_letter, new_number = move_to

        # refining the data to make it easier to work with
        old_number = int(old_number)
        new_number = int(new_number)
        old_unicode = ord(old_letter)
        new_unicode = ord(new_letter)

        # finding acceptable movement
        x_direction = abs(new_unicode - old_unicode)
        y_direction = abs(new_number - old_number)

        if (x_direction == 1 and y_direction == 2) or (x_direction == 2 and y_direction == 1):
            # checking to see if destination place is empty or if it's occupied by enemy chess piece
            if board.get(move_to) is None or board.get(move_to).get_color() != self._color:
                return True

        return False


class Rook(Piece):
    """
    This class represents the Rook chess piece.
    Inherited att:
    self._color - the color of the Rook chess piece
    self._position - the position of the Rook on the board
    """

    def get_ascii_art(self):
        """
        Returns the ascii art associated with that specific chess piece and color.
        """
        if self._color == "BLACK":
            return "♜"
        else:
            return "♖"

    def is_move_valid(self, move_from, move_to, board):
        """
        Returns a boolean that tells whether a move from move_from to move_to is valid.
        """
        # destructuring the data to make it easier to work with
        old_letter, old_number = move_from
        new_letter, new_number = move_to

        # refining the data to make it easier to work with
        old_number = int(old_number)
        new_number = int(new_number)
        old_unicode = ord(old_letter)
        new_unicode = ord(new_letter)

        # making sure that the Rook is NOT traveling diagonally
        if old_letter != new_letter and old_number != new_number:
            return False

        # iterating over the movement path, checking to see if path is clear:

        # - vertical:
        if old_letter == new_letter:
            step = 1 if new_number > old_number else -1

            # iterating vertically - direction depends on step value
            # 1 means up, -1 means down
            for num in range(old_number + step, new_number, step):
                if board[f"{old_letter}{num}"] is not None:
                    return False

        # - horizontal:
        else:
            step = 1 if new_unicode > old_unicode else -1

            # iterating horizontally via unicode - direction depends on step value
            # 1 means right, -1 means left
            for unicode_val in range(old_unicode + step, new_unicode, step):
                # reverting unicode back to a letter to create the proper key
                letter = chr(unicode_val)

                if board[f"{letter}{old_number}"] is not None:
                    return False

        # iteration ends just before the destination to handle the final edge case properly
        destination_piece = board[move_to]

        if destination_piece is not None and destination_piece.get_color() == self._color:
            return False

        return True


class Pawn(Piece):
    """
    This class represents the Pawn chess piece.
    Inherited att:
    self._color - the color of the Pawn chess piece
    self._position - the position of the Pawn on the board
    """
    def get_ascii_art(self):
        """
        Returns the ascii art associated with that specific chess piece and color.
        """
        if self._color == "BLACK":
            return "♟"
        else:
            return "♙"

    def is_move_valid(self, move_from, move_to, board):
        """
        Returns a boolean that tells whether a move from move_from to move_to is valid.
        """
        # destructuring the data to make it easier to work with
        old_letter, old_number = move_from
        new_letter, new_number = move_to

        # refining the data to make it easier to work with
        old_number = int(old_number)
        new_number = int(new_number)
        old_unicode = ord(old_letter)
        new_unicode = ord(new_letter)

        # finding acceptable x and y directions the chess piece plans to move
        x_direction = abs(old_unicode - new_unicode)
        y_dist = 1 if self._color == "WHITE" else -1
        y_direction = old_number + y_dist

        # checks if pawn is moving vertically to a square that has no chess piece
        if x_direction == 0 and y_direction == new_number and board[move_to] is None:
            return True

        # checking if pawn is moving two squares forward from its starting position, while also making sure that there
        # are no chess pieces in the square that's being skipped
        starting_rank = 2 if self._color == "WHITE" else 7
        if x_direction == 0 and old_number == starting_rank and new_number == old_number + 2 * y_dist:
            skipped_square = old_letter + str(old_number + y_dist)
            if board[move_to] is None and board[skipped_square] is None:
                return True

        # checks if pawn is performing a diagonal capture
        if x_direction == 1 and y_direction == new_number:
            # double-checking to see if the diagonal piece belongs to enemy color
            if board[move_to] is not None and board[move_to].get_color() != self._color:
                return True

        return False


def main():
    """
    Testing the functions and classes
    """
    game = ChessVar()
    game.print_board()

    print(game.make_move('d2', 'd4'))  # output True
    print(game.make_move('g7', 'g5'))  # output True
    print(game.make_move('c1', 'g5'))  # output True
    print(game.make_move('e7', 'e5'))  # output True
    print(game.make_move('d4', 'e5'))  # output True
    print(game.make_move('d7', 'd5'))  # output True
    print(game.make_move('d1', 'd5'))  # output True
    print(game.make_move('d8', 'd1'))  # output True

    print(game.make_move('e1', 'd1'))  # output False - king cannot initiate capture

    print(game.make_move('g1', 'h3'))  # output True

    # finishing move here - black should win
    print(game.make_move('d1', 'e1'))  # output True


    game.print_board()
    print(game.get_game_state())  # output UNFINISHED


if __name__ == "__main__":
    main()