import random
import copy
import time
class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = True
        count = 0
        move = []
        move_succ = []
        move_done = (0,0)
        move_ori = (0,0)
        move_succ = self.succ(state,0)
        score = 0
        for row in range(5):
             for col in range(5):
                 if state[row][col] != ' ':
                     count = count + 1
        if count == 8 and self.game_value(state) != 1 and self.game_value(state) != -1:
            drop_phase = False
        if not drop_phase:
            for ((r,c),(r1,c1)) in move_succ: 
                curr_state = copy.deepcopy(state)
                curr_state[r][c] = self.my_piece
                curr_state[r1][c1] = ' '
                newScore = self.max_value(curr_state, 2, 0)
            if newScore >=score:
                score = newScore
                move_done = (r,c)
                move_ori = (r1,c1)
                move.insert(0, move_done)
                move.insert(1, move_ori)
            return move

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        
        for (r,c) in move_succ:
            curr_state = copy.deepcopy(state)
            curr_state[r][c] = self.my_piece
            newScore = self.max_value(curr_state, 2, 0)
            if newScore >=score:
                score = newScore
                move_done = (r,c)
        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, move_done)
        return move
     

    def succ(self, state, turn):
        move1 = []
        move = []
        i = 0
        for row in range(5):
            for col in range(5): 
               if(state[row][col] != ' '):
                   move1.insert(i, (row,col))
                   i = i + 1
        if i != 8:
           for row in range(5):
               for col in range(5):
                   if(row,col) not in move1:
                       move.append((row,col))
        else: 
               for (r,c) in move1:
                   if turn == 0 and state[r][c] == self.my_piece:
                           if(r+1,c) not in move1 and 0<= r+1 <= 4 and 0<= c <= 4:
                               move.append(((r+1,c),(r,c)))
                           if(r+1,c+1) not in move1 and 0<= r+1 <= 4 and 0<= c+1 <= 4:
                               move.append(((r+1,c+1),(r,c)))
                           if(r+1,c-1) not in move1 and 0<= r+1 <= 4 and 0<= c-1 <= 4:
                               move.append(((r+1,c-1),(r,c)))
                           if(r,c+1) not in move1 and 0<= r <= 4 and 0<= c+1 <= 4:
                               move.append(((r,c+1),(r,c)))
                           if(r,c-1) not in move1 and 0<= r <= 4 and 0<= c-1 <= 4:
                               move.append(((r,c-1),(r,c)))    
                           if(r-1,c+1) not in move1 and 0<= r-1 <= 4 and 0<= c+1 <= 4:
                               move.append(((r-1,c+1),(r,c)))    
                           if(r-1,c) not in move1 and 0<= r-1 <= 4 and 0<= c <= 4:
                               move.append(((r-1,c),(r,c)))    
                           if(r-1,c-1) not in move1 and 0<= r-1 <= 4 and 0<= c-1 <= 4:
                               move.append(((r-1,c-1),(r,c)))
                   if turn == 1 and state[r][c] == self.opp:
                           if(r+1,c) not in move1 and 0<= r+1 <= 4 and 0<= c <= 4:
                               move.append(((r+1,c),(r,c)))
                           if(r+1,c+1) not in move1 and 0<= r+1 <= 4 and 0<= c+1 <= 4:
                               move.append(((r+1,c+1),(r,c)))
                           if(r+1,c-1) not in move1 and 0<= r+1 <= 4 and 0<= c-1 <= 4:
                               move.append(((r+1,c-1),(r,c)))
                           if(r,c+1) not in move1 and 0<= r <= 4 and 0<= c+1 <= 4:
                               move.append(((r,c+1),(r,c)))
                           if(r,c-1) not in move1 and 0<= r <= 4 and 0<= c-1 <= 4:
                               move.append(((r,c-1),(r,c)))   
                           if(r-1,c+1) not in move1 and 0<= r-1 <= 4 and 0<= c+1 <= 4:
                               move.append(((r-1,c+1),(r,c)))  
                           if(r-1,c) not in move1 and 0<= r-1 <= 4 and 0<= c <= 4:
                               move.append(((r-1,c),(r,c)))  
                           if(r-1,c-1) not in move1 and 0<= r-1 <= 4 and 0<= c-1 <= 4:
                               move.append(((r-1,c-1),(r,c)))
        return move   

    def heuristic_game_value(self, state):
        max_move = []
        score_max = 0

        count_max = 0

        if self.game_value(state) == 0:
           for row in range(5):
             for col in range(5):
                 if state[row][col] == self.my_piece:
                     count_max = count_max + 1
                     max_move.append((row,col))
                 
           if count_max == 0:
              score_max = 0
          
           if count_max == 1:
              score_max = 0.25
                  
           if count_max == 2:
              if -1 <= max_move[0][0] - max_move[1][0] <=1 and -1 <= max_move[0][1] - max_move[1][1] <= 1:
                 score_max = 0.5
              else:
                 score_max = 0.25 
           
           if count_max == 3:      
              if -1 <= max_move[0][0] - max_move[1][0] <=1 and -1 <= max_move[0][1] - max_move[1][1] <= 1:
                 if max_move[2][0] - max_move[1][0] == max_move[1][0] - max_move[0][0] and max_move[2][1] - max_move[1][1] == max_move[1][1] - max_move[0][1]:  
                    score_max = 0.75
                 else:
                    score_max = 0.5 
              elif -1 <= max_move[0][0] - max_move[2][0] <=1 and -1 <= max_move[0][1] - max_move[2][1] <= 1:  
                 score_max = 0.5 
              elif -1 <= max_move[1][0] - max_move[2][0] <=1 and -1 <= max_move[1][1] - max_move[2][1] <= 1:
                 score_max = 0.5
              else:
                 score_max = 0.25
            
           if count_max == 4: 
              if -1 <= max_move[0][0] - max_move[1][0] <=1 and -1 <= max_move[0][1] - max_move[1][1] <= 1:
                 if max_move[2][0] - max_move[1][0] == max_move[1][0] - max_move[0][0] and max_move[2][1] - max_move[1][1] == max_move[1][1] - max_move[0][1]:    
                    score_max = 0.75
                 elif max_move[3][0] - max_move[1][0] == max_move[1][0] - max_move[0][0] and max_move[3][1] - max_move[1][1] == max_move[1][1] - max_move[0][1]:    
                    score_max = 0.75
                 else:
                    score_max = 0.5 
              if -1 <= max_move[0][0] - max_move[2][0] <=1 and -1 <= max_move[0][1] - max_move[2][1] <= 1:
                 if max_move[3][0] - max_move[2][0] == max_move[2][0] - max_move[0][0] and max_move[3][1] - max_move[2][1] == max_move[2][1] - max_move[0][1]:    
                    score_max = 0.75
                 else:
                    if score_max != 0.75:
                       score_max = 0.5
              if -1 <= max_move[1][0] - max_move[2][0] <=1 and -1 <= max_move[1][1] - max_move[2][1] <= 1:
                 if max_move[3][0] - max_move[2][0] == max_move[2][0] - max_move[1][0] and max_move[3][1] - max_move[2][1] == max_move[2][1] - max_move[1][1]:    
                    score_max = 0.75
                 else:
                    if score_max != 0.75:
                       score_max = 0.5
              if score_max == 0:
                if -1 <= max_move[0][0] - max_move[3][0] <=1 and -1 <= max_move[0][1] - max_move[3][1] <= 1:
                   score_max == 0.5
                elif -1 <= max_move[1][0] - max_move[3][0] <=1 and -1 <= max_move[1][1] - max_move[3][1] <= 1:
                        score_max == 0.5
                elif -1 <= max_move[2][0] - max_move[3][0] <=1 and -1 <= max_move[2][1] - max_move[3][1] <= 1:
                        score_max == 0.5
                else:
                   score_max == 0.25
           
                   
        score = score_max
        return score       
                 
                 
    def max_value(self, state, d, turn):
        count = 0
        for row in range(5):
             for col in range(5):
                 if state[row][col] != ' ':
                     count = count + 1
        i = d
        if self.game_value(state) == 1:
           return 1;
        if self.game_value(state) == -1:
           return -1;
        elif d == 0:
           return self.heuristic_game_value(state);
        elif turn == 0 and count !=8:
           move = self.succ(state,0)
           score = []
           for (r,c) in move:
               curr_state = copy.deepcopy(state)
               curr_state[r][c] = self.my_piece
               d = i - 1;
               score.append(self.max_value(curr_state, d, 1))
           return max(score)
        elif turn == 0 and count == 8:
           move = self.succ(state,0)
           score = []
           for ((r,c),(r1,c1)) in move:
               curr_state = copy.deepcopy(state)
               curr_state[r][c] = self.my_piece
               curr_state[r1][c1] = ' '
               d = i - 1;
               score.append(self.max_value(curr_state, d, 1))
           return max(score)
        elif turn == 1 and count != 8:
           move = self.succ(state,1)
           score = []
           for (r,c) in move:
               curr_state = copy.deepcopy(state)
               curr_state[r][c] = self.opp
               d = i - 1;
               score.append(self.max_value(curr_state, d, 0))
           return min(score)
        elif turn == 1 and count == 8:
           move = self.succ(state,1)
           score = []
           for ((r,c),(r1,c1)) in move:
               curr_state = copy.deepcopy(state)
               curr_state[r][c] = self.opp
               curr_state[r1][c1] = ' '
               d = i - 1;
               score.append(self.max_value(curr_state, d, 0))
           return min(score)
        
             
    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 3x3 square corners wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for r in range(2):
            for c in range(2):
                if state[r][c] != ' ' and state[r][c] == state[r+1][c+1] == state[r+2][c+2] == state[r+3][c+3]:
                    return 1 if state[r][c]==self.my_piece else -1
        # check / diagonal wins
        for r in range(2):
            for c in range(2):
                if state[3+r][c] != ' ' and state[3+r][c] == state[2+r][c+1] == state[1+r][c+2] == state[r][c+3]:
                    return 1 if state[3+r][c]==self.my_piece else -1
        # check 3x3 square corners wins
        for r in range(3):
            for c in range(3):
                if state[r][c] != ' ' and state[r][c] == state[r][c+2] == state[r+2][c] == state[r+2][c+2]:
                    return 1 if state[r][c]==self.my_piece else -1
        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
