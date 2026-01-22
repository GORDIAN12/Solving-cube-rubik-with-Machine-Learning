import numpy as np
import random
import math
# Estado resuelto del cubo
SOLVED_STATE = np.array(
    [0]*9 + [1]*9 + [2]*9 + [3]*9 + [4]*9 + [5]*9,
    dtype=np.int64
)

FACES='UDLRFB'

ORDER = ["U", "R", "F", "D", "L", "B"]

faces_geom = {
    # n = normal, u = “arriba/abajo” de la cara, v = “izq/der” de la cara
    # Coordenadas: x=R+, y=U+, z=F+
    "U": {"n": (0, 1, 0),  "u": (0, 0,-1), "v": (1, 0, 0)},
    "D": {"n": (0,-1, 0),  "u": (0, 0, 1), "v": (1, 0, 0)},
    "F": {"n": (0, 0, 1),  "u": (0,-1, 0), "v": (1, 0, 0)},
    "B": {"n": (0, 0,-1),  "u": (0,-1, 0), "v": (-1,0, 0)},
    "R": {"n": (1, 0, 0),  "u": (0,-1, 0), "v": (0, 0,-1)},
    "L": {"n": (-1,0, 0),  "u": (0,-1, 0), "v": (0, 0, 1)},
}

def row_matrix(axis,angle_deg):
    angle=math.radians(angle_deg)
    ax=np.array(axis, dtype=float)
    ax=ax/np.linalg.norm(ax)
    x,y,z=ax
    c=math.cos(angle)
    s=math.sin(angle)
    C=1-c
    return np.array([[c+x*x*C, x*y*(1-c)-z*s, x*z*(1-c)+y*s],
                     [y*x*(1-c)+z*s, c+y*y*C, y*x*(1-c)-z*s],
                     z*x*(1-c)-y*s, z*y*(1-c)+x*s, c+z*z*C])

def permutacion_tablas():
    id_to_pos_norm=[]
    pos_norm_to_id={}
    id=0
    for face in ORDER:
        n=np.array(faces_geom[face]["n"], dtype=float)
        u=np.array(faces_geom[face]['u'], dtype=float)
        v=np.array(faces_geom[face]['v'], dtype=float)
        for row in range(3):
            for col in range(3):
                dc=col-1
                dr=row-1
                pos=tuple((n+dc*v+dr*u).tolist())
                normal=tuple(n.tolist())
                id_to_pos_norm.append((id,pos,normal))
                pos_norm_to_id[(pos,normal)]=id
                id+=1

def generate_scramble(scramble:str):
    moves=[]
    for char in scramble.strip().split():
        face=char[0].upper()
        if face not in FACES:
            raise ValueError(f"Invalid face {face}")

        if len(char)==1:
            turn=1
        else:
            suf=char[1:]
            if suf=="'":
                turn=3
            elif suf=="2":
                turn=2
            else:
                raise ValueError(f"Invalid turn {char}")

        moves.append((face,turn))
    return moves

generate_scramble("R U R' F2")

#Aplicacion de moviemientos usando permutaciones
def apply_perm(state:np.ndarray, perm:np.ndarray)->np.ndarray:
    return state[perm]

def apply_move(state:np.ndarray,face:str,turn:int,permuta:dict)->np.ndarray:
    for _ in range(turn):
        state=apply_perm(state,permuta[face])
    return state

def apply_scramble(state:np.ndarray,scramble:str, permuta:dict)->np.ndarray:
    for face,turn in generate_scramble(scramble):
        state=apply_move(state,face,turn,permuta)
    return state

#generar scrambles aleatorios
def generate_movs(length=3):
    faces=list(FACES)
    suffixs=["","'","2"]
    out=[]
    last_face=None
    for _ in range(length):
        face=random.choice([f for f in faces if f!=last_face])
        suf=random.choice(suffixs)
        out.append(face+suf)
        last_face=face
    return " ".join(out)

scr = generate_movs(5)
print("Scramble:", scr)
print("Parsed:", generate_scramble(scr))
