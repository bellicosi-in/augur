from state import State
import torch
from train import Net
import chess.svg
import time
import traceback
import base64
import os


class Valuator(object):
    def __init__(self):
        vals = torch.load("nets/value.pth")
        self.model = Net()
        self.model.load_state_dict(vals)

    def __call__(self,s):
        brd = s.serialize()[None]
        output = self.model(torch.tensor(brd).float())
        return float(output.data[0][0])
    


# MINIMAX ALGORITHM
MAXVAL = 10000
class ClassicValuator(object):
    values = {chess.PAWN : 1,
              chess.KNIGHT : 3,
              chess.BISHOP : 3,
              chess.ROOK: 5,
              chess.QUEEN: 9,
              chess.KING: 0
              }
    def __init__(self):
        pass

# apparently a simple value function based on pieces
    def __call__(self,s):
        if s.board.is_variant_win():
            if s.turn == chess.WHITE:
                return MAXVAL
            else:
                return -MAXVAL
            
            if s.board.is_variant_loss():
                if s.turn == chess.WHITE:
                    return -MAXVAL
                else:
                    return MAXVAL
        val = 0
        pm = s.board.piece_map()
        for x in pm:
            tval = self.values[pm[x].piece_type]
            if pm[x].color == chess.WHITE:
                val += tval
            else:
                val -= tval
        return val
        

def computer_minimax(s,v, depth = 2):
    if depth == 0 or s.board.is_game_over():
        return v(s)
    turn = s.board.turn
    if turn == chess.WHITE:
        ret = -MAXVAL
    else:
        ret = MAXVAL
    for e in s.edges():
        s.board.push(e)
        tval = computer_minimax(s,v,depth-1)
        if turn == chess.WHITE:
            ret = max(ret,tval)
        else:
            ret = min(ret,tval)
        s.board.pop()
    return ret
        


def explore_leaves(s,v):
    ret = []
    for e in s.edges():
        s.board.push(e)
        ret.append((v(s),e))
        s.board.pop()
    return ret

v = ClassicValuator()
s = State()

def to_svg(s):
    return base64.b64encode(chess.svg.board(board = s.board).encode('utf-8')).decode('utf-8')

from flask import Flask,Response,request

app = Flask(__name__)

@app.route("/")
def hello():
   ret = open("index.html").read()
   return ret.replace('start',s.board.fen()) 


def computer_move(s,v):
    move = sorted(explore_leaves(s,v), key = lambda x:x[0], reverse = s.board.turn)
    print("top 3")
    for i, m in enumerate(move[0:3]):
        print(" ",m)
    s.board.push(move[0][1])


@app.route("/selfplay")
def selfplay():
    s = State()

    ret = '<html><head>'
    # selfplay
    while not s.board.is_game_over():
        computer_move(s,v)
        ret += '<img width=600 height=600 src="data:image/svg+xml;base64,%s"></img><br/>' % to_svg(s)
    print(s.board.result())

    return ret


@app.route("/move")
def move():
    if not s.board.is_game_over():
        move = request.args.get('move',default = "")
        if move is not None and move!= "":
            print("human moves",move)
            try:
                s.board.push_san(move)
                computer_move(s,v)
            except Exception:
                traceback.print_exc()
            response = app.response_class(
                response = s.board.fen(),
                status = 200
            )
            return response
        else:
            print("Game is over!")
            response = app.response_class(
                response = "game over",
                status = 200
            )
            return response
        print("hello ran")
        return hello()

if __name__ == "__main__":
    if os.getenv("SELFPLAY") is not None:
        s= State()
        while not s.board.is_game_over():
            computer_move(s,v)
            print(s.board)
        print(s.board.result())
    else:
        app.run(debug = True)




# if __name__ == "__main__":
    

#     # self play
#     while not s.board.is_game_over():
#         l = sorted(explore_leaves(s,v), key = lambda x: x[0], reverse = s.board.turn)
#         move = l[0]``
#         print(move)
#         s.board.push(move[1])
#     print(s.board.result())