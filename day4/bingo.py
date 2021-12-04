def load_game(filename):
    lines = open(filename).readlines()
    draws = [int(n) for n in lines[0].split(",")]
    lines = lines[1:]
    boards = []
    while len(lines) > 5:
        block = " ".join(lines[:6])
        boards.append([int(n) for n in block.split()])
        lines = lines[6:]
    return draws, boards

def play_bingo(draws, boards):
    for draw in draws:
        for board in boards:
            mark(draw, board)
            if has_won(board):
                return draw, board
    return None, None

def last_remaining_board(draws, boards):
    for draw in draws:
        i = 0
        while i < len(boards):
            mark(draw, boards[i])
            if has_won(boards[i]):
                if len(boards) == 1:
                    return draw, boards[0]
                del(boards[i])
            else:
                i += 1
    return None, None

def mark(draw, board):
    for pos, number in enumerate(board):
        if number == draw:
            board[pos] = -1

def has_won(board):
    return any(sum(board[pos] for pos in range(5*row, 5*(row+1))) == -5 for row in range(5)) or \
        any(sum(board[pos] for pos in range(col, col + 25, 5)) == -5 for col in range(5))

def score(draw, board):
    return draw * sum(b for b in board if b > 0)

def main():
    draws, boards = load_game("bingo.example")
    winning_draw, winning_board = play_bingo(draws, boards)    
    print("Score of winning board is:", score(winning_draw, winning_board))
    last_draw, last_board = last_remaining_board(draws, boards)
    print("Score of last remaining board is:", score(last_draw, last_board))

if __name__ == "__main__":
    main()
