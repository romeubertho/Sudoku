from sudoku import Sudoku
import sys
import gmpy

def main():
    board_size = 0
    if len(sys.argv) < 2:
        print("Usage is ./main.py <N:int:perfect_square>")
        exit()
    try:
        board_size = int(sys.argv[1])
        if not gmpy.is_square(board_size):
            print("Number is not a perfect square")
            exit()
    except ValueError:
        print("Argument is not int")
        exit()

    game = [[ 0 for _ in range(board_size) ] for _ in range(board_size)]
    sudoku = Sudoku(game)
    sudoku.solve()
    sudoku.printGame()

if __name__ == "__main__":
    main()
