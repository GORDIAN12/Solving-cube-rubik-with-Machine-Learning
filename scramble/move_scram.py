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

def rot_matrix(axis,angle_deg):
    angle=math.radians(angle_deg)
    ax=np.array(axis, dtype=float)
    ax=ax/np.linalg.norm(ax)
    x,y,z=ax
    c=math.cos(angle)
    s=math.sin(angle)
    return np.array([
        [c+x*x*(1-c), x*y*(1-c)-z*s, x*z*(1-c)+y*s],
        [y*x*(1-c)+z*s, c+y*y*(1-c), y*z*(1-c)-x*s],
        [z*x*(1-c)-y*s, z*y*(1-c)+x*s, c+z*z*(1-c)]
    ])

def permutacion_tablas():
    # index -> (pos, normal) para tus 54 facelets en orden URFDLB
    idx_to_posnorm = []
    posnorm_to_idx = {}

    idx = 0
    for face in ORDER:
        n = np.array(faces_geom[face]["n"], dtype=int)
        u = np.array(faces_geom[face]["u"], dtype=int)
        v = np.array(faces_geom[face]["v"], dtype=int)
        for row in range(3):
            for col in range(3):
                dc = col - 1
                dr = row - 1
                pos = tuple((n + dc*v + dr*u).tolist())
                normal = tuple(n.tolist())
                idx_to_posnorm.append((pos, normal))
                posnorm_to_idx[(pos, normal)] = idx
                idx += 1

    def perm_for_face(face):
        axis = np.array(faces_geom[face]["n"], dtype=int)
        Rm = rot_matrix(axis, -90)  # clockwise visto desde afuera

        # seleccionar qué capa rota
        if face in ["U", "D"]:
            coord, layer = 1, (1 if face == "U" else -1)
        elif face in ["R", "L"]:
            coord, layer = 0, (1 if face == "R" else -1)
        else:
            coord, layer = 2, (1 if face == "F" else -1)

        perm = np.arange(54, dtype=np.int64)  # perm[new] = old
        for old_idx, (pos, normal) in enumerate(idx_to_posnorm):
            posv = np.array(pos, dtype=float)
            normv = np.array(normal, dtype=float)

            if int(round(posv[coord])) == layer:
                new_pos = Rm.dot(posv)
                new_norm = Rm.dot(normv)

                new_pos = tuple(int(round(x)) for x in new_pos)
                new_norm = tuple(int(round(x)) for x in new_norm)

                new_idx = posnorm_to_idx[(new_pos, new_norm)]
            else:
                new_idx = old_idx

            perm[new_idx] = old_idx

        return perm

    return {f: perm_for_face(f) for f in FACES}

PERM=permutacion_tablas()



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


if __name__ == "__main__":
    scr = generate_movs(5)
    print("Scramble:", scr)
    print("Parsed:", generate_scramble(scr))

    st=apply_scramble(SOLVED_STATE.copy(),scr,PERM)
    print("Estado despues del scramble (20movs)", st[:20])

    for f in FACES:
        t=SOLVED_STATE.copy()
        t=apply_move(t,f,4,PERM)
        assert np.array_equal(t,SOLVED_STATE), f"Fallo de identidad  en {f}"
    print("test 4 giros por cada identidad")
