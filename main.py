from game import game
from termcolor import colored

def main():
    """Entry point for XTicO."""
    try:
        game()
    except KeyboardInterrupt:
        print(colored("\n\n     Game interrupted. See you next time! 👋\n" ,'blue',attrs=['bold']))
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == '__main__':
    main()