import numpy as np
import random

# Caras: U, R, F, D, L, B (9 stickers cada una)
U, R, F, D, L, B = 0, 9, 18, 27, 36, 45

ACTIONS = ['U',"U'",'D',"D'",'L',"L'",'R',"R'",'F',"F'",'B',"B'"]
INV = {'U':"U'", "U'":'U',
       'D':"D'", "D'":'D',
       'L':"L'", "L'":'L',
       'R':"R'", "R'":'R',
       'F':"F'", "F'":'F',
       'B':"B'", "B'":'B'}

def solved_state():
    # U=0, R=1, F=2, D=3, L=4, B=5
    return np.array([0]*9 + [1]*9 + [2]*9 + [3]*9 + [4]*9 + [5]*9, dtype=np.int64)

def _rot_face_cw(s, f):
    # 0 1 2      6 3 0
    # 3 4 5  ->  7 4 1
    # 6 7 8      8 5 2
    a = s[f:f+9].copy()
    s[f+0], s[f+1], s[f+2] = a[6], a[3], a[0]
    s[f+3], s[f+4], s[f+5] = a[7], a[4], a[1]
    s[f+6], s[f+7], s[f+8] = a[8], a[5], a[2]

def _rot_face_ccw(s, f):
    # inverse of cw
    a = s[f:f+9].copy()
    s[f+0], s[f+1], s[f+2] = a[2], a[5], a[8]
    s[f+3], s[f+4], s[f+5] = a[1], a[4], a[7]
    s[f+6], s[f+7], s[f+8] = a[0], a[3], a[6]

def _get_row(f, r):
    return [f + 3*r + 0, f + 3*r + 1, f + 3*r + 2]

def _get_col(f, c):
    return [f + 0 + c, f + 3 + c, f + 6 + c]

def _cycle_vals(s, a, b, c, d):
    """a<-b<-c<-d<-a (todos son listas de 3 índices)"""
    tmp = s[a].copy()
    s[a] = s[b]
    s[b] = s[c]
    s[c] = s[d]
    s[d] = tmp

def _cycle_vals_rev(s, a, b, c, d):
    """a<-d<-c<-b<-a (inverso)"""
    tmp = s[a].copy()
    s[a] = s[d]
    s[d] = s[c]
    s[c] = s[b]
    s[b] = tmp

class RubikSim:
    def __init__(self):
        self.state = solved_state()

    def reset(self):
        self.state = solved_state()
        return self.state

    def is_solved(self):
        return np.array_equal(self.state, solved_state())

    def apply(self, move: str):
        s = self.state

        if move == 'U':
            _rot_face_cw(s, U)
            # F top, R top, B top, L top
            _cycle_vals(s, _get_row(F,0), _get_row(R,0), _get_row(B,0), _get_row(L,0))

        elif move == "U'":
            _rot_face_ccw(s, U)
            _cycle_vals_rev(s, _get_row(F,0), _get_row(R,0), _get_row(B,0), _get_row(L,0))

        elif move == 'D':
            _rot_face_cw(s, D)
            # F bottom, L bottom, B bottom, R bottom (ojo orientación estándar)
            _cycle_vals(s, _get_row(F,2), _get_row(L,2), _get_row(B,2), _get_row(R,2))

        elif move == "D'":
            _rot_face_ccw(s, D)
            _cycle_vals_rev(s, _get_row(F,2), _get_row(L,2), _get_row(B,2), _get_row(R,2))

        elif move == 'R':
            _rot_face_cw(s, R)
            # U col2, F col2, D col2, B col0 (B se invierte)
            a = _get_col(U,2)
            b = _get_col(F,2)
            c = _get_col(D,2)
            d = _get_col(B,0)[::-1]
            _cycle_vals(s, a, b, c, d)

        elif move == "R'":
            _rot_face_ccw(s, R)
            a = _get_col(U,2)
            b = _get_col(F,2)
            c = _get_col(D,2)
            d = _get_col(B,0)[::-1]
            _cycle_vals_rev(s, a, b, c, d)

        elif move == 'L':
            _rot_face_cw(s, L)
            # U col0, B col2 (inv), D col0, F col0
            a = _get_col(U,0)
            b = _get_col(B,2)[::-1]
            c = _get_col(D,0)
            d = _get_col(F,0)
            _cycle_vals(s, a, d, c, b)  # orden consistente

        elif move == "L'":
            _rot_face_ccw(s, L)
            a = _get_col(U,0)
            b = _get_col(B,2)[::-1]
            c = _get_col(D,0)
            d = _get_col(F,0)
            _cycle_vals_rev(s, a, d, c, b)

        elif move == 'F':
            _rot_face_cw(s, F)
            # U row2, L col2 (inv), D row0, R col0
            a = _get_row(U,2)
            b = _get_col(L,2)[::-1]
            c = _get_row(D,0)
            d = _get_col(R,0)
            _cycle_vals(s, a, b, c, d)

        elif move == "F'":
            _rot_face_ccw(s, F)
            a = _get_row(U,2)
            b = _get_col(L,2)[::-1]
            c = _get_row(D,0)
            d = _get_col(R,0)
            _cycle_vals_rev(s, a, b, c, d)

        elif move == 'B':
            _rot_face_cw(s, B)
            # U row0, R col2, D row2, L col0 (inv)
            a = _get_row(U,0)
            b = _get_col(R,2)
            c = _get_row(D,2)
            d = _get_col(L,0)[::-1]
            _cycle_vals(s, a, b, c, d)

        elif move == "B'":
            _rot_face_ccw(s, B)
            a = _get_row(U,0)
            b = _get_col(R,2)
            c = _get_row(D,2)
            d = _get_col(L,0)[::-1]
            _cycle_vals_rev(s, a, b, c, d)

        else:
            raise ValueError(f"Movimiento desconocido: {move}")

    def scramble(self, k=10):
        moves = [random.choice(ACTIONS) for _ in range(k)]
        for m in moves:
            self.apply(m)
        return moves

    def pretty(self):
        # map de color a letra
        # (puedes cambiar letras)
        m = {0:'U', 1:'R', 2:'F', 3:'D', 4:'L', 5:'B'}
        s = self.state

        def face_str(f):
            return [
                f"{m[s[f+0]]} {m[s[f+1]]} {m[s[f+2]]}",
                f"{m[s[f+3]]} {m[s[f+4]]} {m[s[f+5]]}",
                f"{m[s[f+6]]} {m[s[f+7]]} {m[s[f+8]]}",
            ]

        Uc = face_str(U)
        Rc = face_str(R)
        Fc = face_str(F)
        Dc = face_str(D)
        Lc = face_str(L)
        Bc = face_str(B)

        # layout tipo cruz
        lines = []
        lines.append("      " + Uc[0])
        lines.append("      " + Uc[1])
        lines.append("      " + Uc[2])
        lines.append(Lc[0] + "   " + Fc[0] + "   " + Rc[0] + "   " + Bc[0])
        lines.append(Lc[1] + "   " + Fc[1] + "   " + Rc[1] + "   " + Bc[1])
        lines.append(Lc[2] + "   " + Fc[2] + "   " + Rc[2] + "   " + Bc[2])
        lines.append("      " + Dc[0])
        lines.append("      " + Dc[1])
        lines.append("      " + Dc[2])

        return "\n".join(lines)

if __name__ == "__main__":
    sim = RubikSim()
    print("Resuelto:\n", sim.pretty())

    moves = sim.scramble(8)
    print("\nScramble:", " ".join(moves))
    print(sim.pretty())

    # deshacer scramble
    for m in reversed(moves):
        sim.apply(INV[m])

    print("\nDeshecho. ¿Resuelto?:", sim.is_solved())
    print(sim.pretty())
