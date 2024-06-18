import os
import chess.pgn 
from state import State

def get_dataset(num_samples = None):
    X,Y = [],[]
    gn = 0
    for fn in os.listdir("data"):
        pgn = open(os.path.join("data",fn))
        while 1:
            try:
                game = chess.pgn.read_game(pgn)
            except Exception:
                break
            
            gn += 1
            result = {"1/2-1/2" : 0, "1-0" : 1, "0-1" : -1}[game.headers['Result']]
            # print(result)

            board = game.board()
            for i,move in enumerate(game.mainline_moves()):
                # print(i)
                board.push(move)
                ser = State(board).serialize()[:,:,0]
                # print(ser)
                # print(board.shredder_fen())
                X.append(ser)
                Y.append(result)
            print(f"parsing {gn} games and got {len(X)} samples")
            if num_samples is not None and len(X)>num_samples:
                return X,Y
            

if __name__ == "__main__":
    X,Y = get_dataset(1000)