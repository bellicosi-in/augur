from state import State
import torch
from train import Net
import chess.svg
import time
import traceback


class Valuator(object):
    def __init__(self):
        vals = torch.load("nets/value.pth")
        self.model = Net()
        self.model.load_state_dict(vals)

    def __call__(self,s):
        brd = s.serialize()[None]
        output = self.model(torch.tensor(brd).float())
        return float(output.data[0][0])
    

def explore_leaves(s,v):
    ret = []
    for e in s.edges():
        s.board.push(e)
        ret.append((v(s),e))
        s.board.pop()
    return ret

v = Valuator()
s = State()

from flask import Flask,Response,request

app = Flask(__name__)

@app.route("/")
def hello():
    ret = '<html><head>'
    ret += '<style>input{ font-size: 30px;} button {font-size: 30px;}</style>'
    ret += '</head><body>'
    ret += '<img width = 600 src = "/board.svg?%f"></img><br/>' %time.time()
    ret += '<form action = "/move"><input name = "move" type = "text"></input><input type = "submit" value = "Move"></form><br/>'
    return ret

@app.route("/board.svg")
def board():
    return Response(chess.svg.board(board = s.board), mimetype = 'image/svg+xml')

def computer_move():
    move = sorted(explore_leaves(s,v), key = lambda x:x[0], reverse = s.board.turn)[0]
    print(move)
    s.board.push(move[1])

@app.route("/move")
def move():
    if not s.board.is_game_over():
        move = request.args.get('move',default = "")
        if move is not None and move!= "":
            print("human moves",move)
            try:
                s.board.push_san(move)
                computer_move()
            except Exception:
                traceback.print_exc()
        else:
            print("Game is over!")
        return hello()

if __name__ == "__main__":
    app.run(debug = True)




# if __name__ == "__main__":
    

#     # self play
#     while not s.board.is_game_over():
#         l = sorted(explore_leaves(s,v), key = lambda x: x[0], reverse = s.board.turn)
#         move = l[0]``
#         print(move)
#         s.board.push(move[1])
#     print(s.board.result())