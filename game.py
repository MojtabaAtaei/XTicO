from utils import *

def game():
    """Runs the main game loop."""
    pl_again = 'y'
    computer_score = 0
    player_score = 0
    round = 1

    while pl_again.lower() in ('y', 'yes'):
        if name == 'nt':
            system('cls')
        else:
            system('clear')

        print(colored(f'Player score: {colored(player_score,'white',attrs=['bold'])}','blue',),colored('    |   ','yellow',attrs=['bold']),
              colored(f'Computer score: {colored(computer_score,'white',attrs=['bold'])}','red'))
        print(colored(f'Player symbol: {colored(chr(10008),'white')}','blue',),colored('   |   ','yellow',attrs=['bold']),
              colored(f'Computer symbol: {colored(chr(9675),'white',attrs=['bold'])}','red',))
        display_board(player_score,computer_score,round)

        while True:
            try:
                move = inputimeout(prompt=colored('\nEnter your move 👀(1-9)(60 seconds): ','white',attrs=['bold']),timeout= 60)
                move = int(move)
                mov, win = make_move(board,player,move)
                if not mov :
                    raise InvalidMoveError
                break
            except ValueError:
                print(colored('Please enter a number between 1 and 9 ❗️','red','on_grey',attrs=['bold','blink']))
            except InvalidMoveError:
                print(colored('Invalid move, try again 📱!', 'red',attrs=['bold']))
            except TimeoutOccurred:
                move = random_move(board)
                mov, win = make_move(board,player,move)
                break

        if win:
            player_score += 1
            if name == 'nt':
                system('cls')
            else:
                system('clear')
            display_board(player_score,computer_score,round)
            print(colored('You win 🎉', 'green','on_blue',attrs=['bold']),'\n')
            pl_again = play_again(player_score,computer_score,pl_again)
            match pl_again.lower():
                case 'n' | 'no':
                    break
            round += 1

        elif make_computer_move()[1]:
            computer_score += 1
            
            if name == 'nt':
                system('cls')
            else:
                system('clear')
            display_board(player_score,computer_score,round)
            print(colored('Computer wins 🤖', 'yellow',attrs=['bold']),'\n')
            pl_again = play_again(player_score,computer_score,pl_again)
            match pl_again.lower():
                case 'n' | 'no':
                    break
            round += 1

        elif check_draw(board):
            if name == 'nt':
                system('cls')
            else:
                system('clear')
            display_board(player_score,computer_score,round)
            print(colored('It\'s a draw 🌀','cyan',attrs=['bold']),'\n')
            pl_again = play_again(player_score,computer_score,pl_again)
            match pl_again.lower():
                case 'n' | 'no':
                    break
            round += 1


if __name__ == '__main__':
    game()