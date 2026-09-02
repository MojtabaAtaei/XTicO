from termcolor import colored
from os import system,name
board = list(range(1,10))
player, computer ='X', 'O'
win_combinations = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
moves = ((1,3,7,9),(5,),(2,4,6,8))

def display_board():
    j = 1
    for i in board:
        end = '  '
        if j % 3 == 0:
            end = '\n\n'
        if i == 'X':
            print(colored(f'[{i}]','red'),end=end)
        elif i =='O':
            print(colored(f'[{i}]','blue'),end=end)
        else :
            print(colored(f'[{i}]','black'),end=end)
        j += 1


def make_computer_move():
    PC_move = -1
    for i in range(1,10):
        if make_move(board,computer,1,True)[1]:
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
    if is_valid(br,mov):
        br[mov-1] = pl
        is_winner = check_winner(br,pl)
        if undo:
            br[mov-1] = mov
        return True, is_winner
    return False,False
        


def is_valid(br,mov):
    if mov in range(1,10) and isinstance(br[mov-1],int):
        return True
    return False


def check_winner(br,mov):
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


def has_empty():
    return board.count('X') + board.count('O') != 9


if __name__ == '__main__':
    while has_empty():
        if name == 'nt':
            system('cls')
        else:
            system('clear')
        print('Player: X  |  Computer: O')
        display_board()
        move = int(input('Enter your move 👀(1-9): '))
        mov, win = make_move(board,player,move)
        if not mov :
            print(colored('Invalid move, try again 📱!', 'red'))
            continue
        if win:
            print(colored('You win 🎉!', 'green'))
            break
        elif make_computer_move()[1]:
            print(colored('Computer wins 🤖', 'yellow'))
            break


    display_board()