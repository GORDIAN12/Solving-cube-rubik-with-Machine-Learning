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
    """
    Regresa lo mismo que generate_random_movements:
    [ (angle, axis, layer), (angle, axis, layer), ... ]
    """
    rotation_queue = []
    actions = scramble_to_actions(scramble)

    for action in actions:
        if action not in config.rubik_moves:
            raise KeyError(f"No existe '{action}' en config.rubik_moves")
        rotation_queue.append(config.rubik_moves[action])

    return rotation_queue
