import config
import numpy as np
"""
def generate_random_movements(n):
    rotation_queue=[]

    for _ in range(n):
        action=np.random.choice(list(config.rubik_moves.keys()))
        rotation_queue.append(config.rubik_moves[action])
    return rotation_queue
"""
import config
from scramble import move_scram  # tu archivo move_scram.py

def scramble_to_actions(scramble: str):
    """
    "U2 R2 D U2 B'" -> ['U','U','R','R','D','U','U',"B'"]
    """
    actions = []
    parsed = move_scram.generate_scramble(scramble)  # [('U',2), ...]
    for face, turn in parsed:
        if turn == 1:
            actions.append(face)
        elif turn == 2:
            actions.extend([face, face])
        elif turn == 3:
            actions.append(face + "'")
        else:
            raise ValueError(f"Turn inválido: {turn}")
    return actions


def rotation_queue_from_scramble(scramble: str):
    rotation_queue = []
    parsed = move_scram.generate_scramble(scramble)  # [('U',2),...]

    for face, turn in parsed:
        if turn == 1:
            actions = [face]
        elif turn == 2:
            actions = [face, face]       # U2 -> U U
        elif turn == 3:
            actions = [face + "'"]       # U' (antihorario)
        else:
            raise ValueError(f"Turn inválido: {turn}")

        for action in actions:
            rotation_queue.append(config.rubik_moves[action])

    return rotation_queue

def invert_move(move: str) -> str:
    if move.endswith("2"):
        return move          # U2 → U2
    if move.endswith("'"):
        return move[0]       # U' → U
    return move + "'"        # U → U'


def invert_scramble(scramble: str) -> str:
    moves = scramble.strip().split()
    inverted = [invert_move(m) for m in reversed(moves)]
    return " ".join(inverted)
