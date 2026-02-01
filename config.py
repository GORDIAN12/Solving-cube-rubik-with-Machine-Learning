import numpy as np
import pyray as pr

rubik_moves = {
    'U': (np.radians(90.), np.array([0, 1, 0]), 2),
    'U\'': (np.radians(-90.), np.array([0, 1, 0]), 2),
    'D': (np.radians(90.), np.array([0, 1, 0]), 0),
    'D\'': (np.radians(-90.), np.array([0, 1, 0]), 0),
    'L': (np.radians(90.), np.array([1, 0, 0]), 0),
    'L\'': (np.radians(-90.), np.array([1, 0, 0]), 0),
    'R': (np.radians(-90.), np.array([1, 0, 0]), 2),
    'R\'': (np.radians(90.), np.array([1, 0, 0]), 2),
    'F': (np.radians(90.), np.array([0, 0, 1]), 2),
    'F\'': (np.radians(-90.), np.array([0, 0, 1]), 2),
    'B': (np.radians(-90.), np.array([0, 0, 1]), 0),
    'B\'': (np.radians(90.), np.array([0, 0, 1]), 0),

    'U2': (np.radians(180.), np.array([0, 1, 0]), 2),
    'D2': (np.radians(180.), np.array([0, 1, 0]), 0),

    'L2': (np.radians(180.), np.array([1, 0, 0]), 0),
    'R2': (np.radians(180.), np.array([1, 0, 0]), 2),

    'F2': (np.radians(180.), np.array([0, 0, 1]), 2),
    'B2': (np.radians(180.), np.array([0, 0, 1]), 0),

}

window_w, window_h = 1200, 1000
fps=120
camera=pr.Camera3D([18.0,16.0,18.0],[0.0,0.0,0.0], [0.0,1.0,0.0],45.0,0)