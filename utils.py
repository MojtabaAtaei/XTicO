from termcolor import colored
import random
from inputimeout import TimeoutOccurred,inputimeout
from os import system,name
from functools import wraps

board = list(range(1,10))
player, computer ='X', 'O'
win_combinations = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
mov1,mov2,mov3 = [1,2,7,9],[5],[2,4,6,8]
moves = (random.sample(mov1,len(mov1)),random.sample(mov2,len(mov2)),random.sample(mov3,len(mov3)))

def decorator_display(func):
    @wraps(func)
    def wrapper(player_score,computer_score,round,*args,**kwargs):
        def color_word(word,color):
            w = colored(word,color,attrs=['bold'])
            return w
        def color_line(sz: int):
            cl = ((colored('-','blue',attrs=['bold'])+colored('-','white',attrs=['bold'])) * sz)
            return cl
        
        if round == 1:
            print(color_line(8),
                  color_word('W','red')+color_word('E','blue')+color_word('L','cyan')+
                  color_word('C','green')+color_word('O','yellow')+
                  color_word('M','blue')+color_word('E','white'),
                  color_line(9)
                )
        else:
            print(color_line(21)+colored('-','blue',attrs=['bold']))
        
        print(17 * ' ',color_word('X','red')+color_word('Tic','white')+color_word('O','blue'))
        print(color_line(21)+colored('-','blue',attrs=['bold']))
        func(*args,**kwargs)
        print(colored(f'{chr(9098)}','blue',attrs=['bold']),colored(f'round: {colored(round,'cyan',attrs=['bold'])}','white',attrs=['bold']),'\n',end='')
    return wrapper

@decorator_display
def display_board():
    """
    Displays the current game board using Unicode box-drawing characters
    and colored symbols. Empty cells show their corresponding numbers,
    while the player and computer moves are represented by X and O.
    """
    j = 1
    print(f'            {chr(9556)}'
        +colored(f'{chr(9552)*4}','white')+colored(f'{chr(9574)}','white')+
                          colored(f'{chr(9552)*5}','white')+colored(f'{chr(9574)}','white')+
                          colored(f'{chr(9552)*5}','white')+colored(f'{chr(9559)}','white'))
    if j == 1 or j == 4 or j == 7:
        if j == 4 or j == 7:
            print(f'            ',end='')
        else:
            print(f'            {chr(9553)}',end='')
    for i in board:
        end = colored(f' {chr(9553)} ','white',attrs=['bold'])
        if j % 3 == 0:
            if j == 6 or j == 3:
                end = ( f' {chr(9553)}'+ '\n' + f'            {chr(9568)}' +
                       colored(f'{chr(9552)*4}','white')+colored(f'{chr(9580)}','white')+
                    colored(f'{chr(9552)*5}','white')+colored(f'{chr(9580)}','white')+
                    colored(f'{chr(9552)*5}','white')+colored(f'{chr(9571)}','white')+
                    '\n' + f'            {chr(9553)}')
            else:
                end = (f' {chr(9553)}'+'\n'+ f'            {chr(9562)}' +colored(f'{chr(9552)*4}','white')+colored(f'{chr(9577)}','white')+
                    colored(f'{chr(9552)*5}','white')+colored(f'{chr(9577)}','white')+
                    colored(f'{chr(9552)*5}','white')+colored(f'{chr(9565)}','white')+
                    '\n')

        if i == 'X':   
            print(colored(f' {chr(10008)} ','blue',attrs=['bold']),end=end)
        elif i =='O':
            print(colored(f' {chr(9675)} ','red',attrs=['bold']),end=end)
        else :
            print(colored(f' {i} ','black',attrs=['bold']),end=end)
        j += 1


def make_computer_move():
    """
    Determines and makes the computer's next move.
    The computer first looks for a winning move, then tries to block the
    player's winning move, and finally selects an available position
    from its preferred moves.
    """
    PC_move = -1
    for i in range(1,10):
        if make_move(board,computer,i,True)[1]:
            PC_move = i
            break
        if PC_move == -1:
            for j in range(1,10):
                if make_move(board,player,j ,True)[1]:
                    PC_move = j
                    break
        if PC_move == -1:
            for move_group in moves:
                for m in move_group:
                    if PC_move == -1 and is_valid(board,m):
                        PC_move = m
                        break
    return make_move(board,computer,PC_move)


def make_move(br,pl,mov,undo = False):
    """
    Places a player's mark on the selected cell and checks whether the move
    results in a win.

    When undo is True, the move is temporarily applied for evaluation and
    then restored.

    Returns:
        tuple[bool, bool]: A pair indicating whether the move was valid
        and whether it resulted in a win.
    """
    if is_valid(br,mov):
        br[mov-1] = pl
        is_winner = check_winner(br,pl)
        if undo:
            br[mov-1] = mov
        return True, is_winner
    return False,False
        


def is_valid(br,mov):
    """
     Checks whether a move is within the valid range and the selected cell
    is still empty.

    Returns:
        bool: True if the move is valid, otherwise False. 
    """
    if mov in range(1,10) and isinstance(br[mov-1],int):
        return True
    return False


def check_winner(br,mov):
    """
    Checks whether the specified player has completed any winning
    combination on the board.

    Returns:
        bool: True if the player has won, otherwise False.
    """
    is_winner = True
    for tup in win_combinations:
        is_winner = True
        for j in tup:
            if br[j] != mov:
                is_winner = False
                break
        if is_winner:
            break
    return is_winner


class InvalidMoveError(Exception):
    """Raised when the player attempts an invalid move, such as choosing an occupied cell."""
    pass

def play_again(player_score,computer_score,pl_again):
    """
    Asks the player whether they want to start another round.
    If no response is given within 60 seconds, the game ends.
    When the player chooses to continue, the board is reset.
    """
    pl_again = None
    while True:
        try:
            if pl_again == None:
                pl_again = inputimeout(colored('Do you want to play again? (y/n)(60 seconds) : ','white',attrs=['bold']),timeout= 60)
            match pl_again.lower():
                case 'n' | 'no' :
                    if name == 'nt':
                        system('cls')
                    else:
                        system('clear')
                    print(colored('Thanks for playing 💯','green',attrs=['bold']),'\n',colored(f'Your score: {player_score}','yellow'),'\n',colored(f'Computer score: {computer_score}','blue'),sep='')
                    ex = input(colored('\n   Press Enter to exit!  ','blue',attrs=['bold'])) 
                    return pl_again
                case 'y' | 'yes':
                    board.clear()
                    board.extend(range(1,10))
                    return pl_again
                case _:
                    raise ValueError()
        except TimeoutOccurred:
            pl_again = 'n'
        except :
                print(colored('Please enter a valid value ❗️','red','on_grey',attrs=['bold','blink']))
                pl_again = None


def random_move(br):
    """
    Selects a random empty cell from the current board.

    This is used when the player does not enter a move before the timeout.
    """
    l = []
    for i in br:
        if isinstance(i,int):
            l.append(i)
    move = random.choice(l)
    return move


def check_draw(br):
    """
    Checks whether the board is full, indicating a draw if no winner
    has already been detected.

    Returns:
        bool: True if the board is full, otherwise False.
    """
    for i in range(1,10):
        if i in br:
            return False
    return True

        