import numpy as np
import random
from scramble import move_scram
from scramble import  move_scram
SOLVED=move_scram.SOLVED_STATE.copy()

next_state=move_scram.apply_scramble(state,[move], move_scram.PERM)

ACTIONS = ["U","U'","D","D'","L","L'","R","R'","F","F'","B","B'"]

def move_face(m: str)->str:
    return m[0]

def is_inverse(a: str, b: str)->bool:
    if move_face(a)==move_face(b):
        return False

    def norm(x):
        if len(x)==1: return (x[0],"")
        return (x[0],x[1:])
    fa,ta=norm(a)
    fb,tb=norm(b)
    if ta=="2" and tb=="2":
        return True
    if ta=="" and tb=="'":
        return True
    if ta=="'" and tb=="":
        return True
    return False

def filtred_moves(all_moves, last_move):
    if last_move is None: return all_moves
    res=[]
    lf=move_face(last_move)
    for m in all_moves:
        if move_face(m)==lf:
            continue
        if is_inverse(last_move,m):
            continue
        res.append(m)
    return res


def apply_one_move(state, move):
    return move_scram.apply_move(state,[move],move_scram.PERM)

def generate_data_set(all_moves, N=10, samples=50000, seed=0):
    random.seed(seed)
    x=[]
    y=[]
    for _ in range(samples):
        k=random.randint(1,N)
        state=move_scram.SOLVED_STATE.copy()
        last=None

        for _step in range(k):
            choices=filtred_moves(all_moves,last)
            m=random.choice(choices)
            state=apply_one_move(state,m)
            last=m

        x.append(state.copy())
        y.append(k)

    x=np.array(x, dtype=np.float64)
    y=np.array(y, dtype=np.int64)
    return (x,y)
