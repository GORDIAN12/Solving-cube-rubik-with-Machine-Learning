# Solving cube rubik with Python and Machine Learning.

Simulator 3D about cube rubik that generate a random scramble and solving using differents approachs
regression, search IDDFS and a model  trainer with Pytorch.
---

## Characteristics.
- Simulator 3D Cube Rubik.
- Automatic Generation of Scrambles.
- Resolution by:
    - Regression. (invert movs)
    - Searching IDDFS.
    - Model Machine Learning trainer.
- Animation step by step scramble and solution.
- Modular and easy to extends code.

## Algorithms were used:

### 1. Regreression.
Invert the original scramble to return the sube in its state solved.
Useful to validate the simulation and animation.

### 2. IDDFS.
Depht search with increase iterative of maximum depth.
Ensure find the solution optimal if the limit is enough.

### 3. Machine Learning Model
The Model was trainer with Pytorch that predict the movs sequence to solving the cube from assign state.

## Technologies.

- Pytorch 3.10
- Raylib/pyray
- NumPy
- Object Oriented Programming
- Algorithms searchings.

## Install.
1. Clona el repositorio:
```bash
git clone https://github.com/GORDIAN12/Solving-cube-rubik-with-Machine-Learning.git
cd rubik-ml-solver

2. Create virtual enviroment.
python -m venv venv
source venv/bin/activate   # Linux / Mac

3. Install Dependencies.
pip install -r requirements.txt

4. Run the program.
```bash
python main.py


5.Select the opction for resolution.
1. Regression
2. IDDFS
3. Model IA



