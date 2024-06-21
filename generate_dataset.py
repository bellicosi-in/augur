import os
import chess.pgn 
import numpy as np
from state import State

def get_dataset(num_samples = None):
    X,Y = [],[]
    gn = 0
    values = {'1/2-1/2':0, '0-1':-1, '1-0':1}
    for fn in os.listdir("data"):
        pgn = open(os.path.join("data",fn))
        while 1:
            try:
                game = chess.pgn.read_game(pgn)
            except Exception:
               continue 
            
            # gn += 1
            result = game.headers['Result']
            # print(result)
            if result not in values:
                continue
            value = values[result]
            board = game.board()
            for i,move in enumerate(game.mainline_moves()):
                # print(i)
                board.push(move)
                ser = State(board).serialize()[:,:,0]
                # print(ser)
                # print(board.shredder_fen())
                X.append(ser)
                Y.append(value)
            print(f"parsing {gn} games and got {len(X)} samples")
            if num_samples is not None and len(X)>num_samples:
                return X,Y
            gn += 1
        X = np.array(X)
        Y = np.array(Y)
        return X,Y 

if __name__ == "__main__":
    X,Y = get_dataset(100000)

    np.savez("processed/dataset_100k.npz",X,Y) 
    
    print("file saved")