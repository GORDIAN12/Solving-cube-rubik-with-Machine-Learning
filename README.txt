# Solving Cube Rubik with Python and Machine Learning
3D simulator of a Rubik's Cube that generates a random scramble and solves it
using different approaches: regression (invert moves), IDDFS search, and a
trained Machine Learning model with PyTorch.

---

## Characteristics

- 3D Rubik's Cube simulator
- Automatic scramble generation
- Resolution using:
  - Regression (invert movements)
  - IDDFS search
  - Trained Machine Learning model
- Step-by-step animation of scramble and solution
- Modular and easy-to-extend code

---

## Algorithms Used

### 1. Regression
Inverts the original scramble to return the cube to its solved state.
Useful to validate the simulation and animation.

### 2. IDDFS
Depth-first search with iterative deepening.
Ensures finding the optimal solution if the depth limit is sufficient.

### 3. Machine Learning Model
A model trained with PyTorch that predicts the sequence of movements
to solve the cube from a given state.

---

## Technologies

- Python 3.10
- PyTorch
- Raylib / Pyray
- NumPy
- Object-Oriented Programming
- Search Algorithms

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/GORDIAN12/Solving-cube-rubik-with-Machine-Learning.git
cd Solving-cube-rubik-with-Machine-Learning
