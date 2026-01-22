import kociemba
import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np


#Faces
FACES='UDLRFB'


# Mapeo de movimientos
move_to_id = {
    "U": 0, "U'": 1, "U2": 2,
    "D": 3, "D'": 4, "D2": 5,
    "L": 6, "L'": 7, "L2": 8,
    "R": 9, "R'": 10, "R2": 11,
    "F": 12, "F'": 13, "F2": 14,
    "B": 15, "B'": 16, "B2": 17
}
id_to_move = {v: k for k, v in move_to_id.items()}

NUM_TO_FACE = {0: 'U', 1: 'R', 2: 'F', 3: 'D', 4: 'L', 5: 'B'}
FACE_TO_NUM = {v: k for k, v in NUM_TO_FACE.items()}

# Estado resuelto del cubo
SOLVED_STATE = [
    0, 0, 0, 0, 0, 0, 0, 0, 0,  # U (arriba) - blanco
    1, 1, 1, 1, 1, 1, 1, 1, 1,  # R (derecha) - rojo
    2, 2, 2, 2, 2, 2, 2, 2, 2,  # F (frente) - verde
    3, 3, 3, 3, 3, 3, 3, 3, 3,  # D (abajo) - amarillo
    4, 4, 4, 4, 4, 4, 4, 4, 4,  # L (izquierda) - naranja
    5, 5, 5, 5, 5, 5, 5, 5, 5  # B (atrás) - azul
]


def cube_to_onehot(state54):
    """Convierte el estado del cubo a one-hot encoding"""
    x = torch.zeros(54, 6)
    for i, c in enumerate(state54):
        x[i, c] = 1
    return x.view(-1)  # Retorna vector de tamaño 324 (54*6)


def state_to_kociemba_string(state54):
    """Convierte el estado numérico a string para Kociemba"""
    return "".join(NUM_TO_FACE[c] for c in state54)


def kociemba_string_to_state(cube_str):
    """Convierte string de Kociemba a estado numérico"""
    return [FACE_TO_NUM[c] for c in cube_str]


def apply_move_to_string(cube_str, move):
    """Aplica un movimiento a un cubo en formato string"""
    state = kociemba_string_to_state(cube_str)
    return cube_str


