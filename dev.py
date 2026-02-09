from pyray import *
from ML import searching
from rubik import Rubik
from utils import *
import config
from scramble import move_scram
from ML.tester import solve_state
"""
init_window(config.window_w, config.window_h, "Solving cube rubik with ML")
rubik_cube = Rubik()

movs = move_scram.generate_movs(5)
if isinstance(movs, list):
    movs_list = movs
    movs_str = " ".join(movs)
else:
    movs_str = movs
    movs_list = movs.split()

print("SCRAMBLE:", movs_str)

rotation_queue = rotation_queue_from_scramble(movs_list)

state_scrambled = move_scram.apply_scramble(
    move_scram.SOLVED_STATE.copy(),
    movs_str,  # ✅ string
    move_scram.PERM
)

solution_queue = []
animating_scramble = True
solving_started = False
animation_complete = False

set_target_fps(config.fps)
while not window_should_close():
    if animating_scramble:
        if rotation_queue or rubik_cube.is_rotating:
            rotation_queue, _ = rubik_cube.handle_rotation(rotation_queue)
        else:
            animating_scramble = False  # ✅ terminó scramble
    else:
        # calcular solución una sola vez
        if not solving_started:
            sol = solve_state(state_scrambled)
            print("SOL:", sol)
            solution_queue = rotation_queue_from_scramble(sol) if sol is not None else []
            solving_started = True

        # animar solución
        if solution_queue or rubik_cube.is_rotating:
            solution_queue, _ = rubik_cube.handle_rotation(solution_queue)
        else:
            if not animation_complete:
                print("✓ ¡Cubo resuelto (animación terminada)!")
                animation_complete = True

    update_camera(config.camera, CameraMode.CAMERA_THIRD_PERSON)
    begin_drawing()
    clear_background(RAYWHITE)
    begin_mode_3d(config.camera)
    draw_grid(20, 1.0)

    for cube in rubik_cube.cubes:
        for cube_part in cube:
            position = Vector3(cube[0].center[0], cube[0].center[1], cube[0].center[2])
            draw_model(cube_part.model, position, 2, cube_part.face_color)

    end_mode_3d()
    end_drawing()

close_window()
"""


from pyray import *
from rubik import Rubik
from utils import *
import config
from scramble import move_scram

init_window(config.window_w, config.window_h, "Solving cube rubik with ML")
rubik_cube = Rubik()


movs = move_scram.generate_movs(5)
print("SCRAMBLE:", movs)

rotation_queue = rotation_queue_from_scramble(movs)

state_scrambled = move_scram.apply_scramble(
    move_scram.SOLVED_STATE.copy(),
    movs,
    move_scram.PERM
)

# 4) Encontrar solución con IDDFS
sol = searching.iddfs_solve(state_scrambled, move_scram.PERM, move_scram.SOLVED_STATE, max_depth=10)
print("Solución encontrada:", sol)

# 5) Convertir solución a cola
solution_queue = rotation_queue_from_scramble(sol) if sol is not None else []

print("SOLUTION", solution_queue)
print(f"Total movimientos en solución: {len(solution_queue)}")


animating_scramble = True
animation_complete = False

set_target_fps(config.fps)
while not window_should_close():

    # 1) Animar scramble
    if animating_scramble:
        if rotation_queue or rubik_cube.is_rotating:
            rotation_queue, _ = rubik_cube.handle_rotation(rotation_queue)
        else:
            animating_scramble = False

    # 2) Animar solución
    else:
        if solution_queue or rubik_cube.is_rotating:
            solution_queue, _ = rubik_cube.handle_rotation(solution_queue)
        else:
            if not animation_complete:
                print("✓ Cubo resuelto")
                animation_complete = True

    update_camera(config.camera, CameraMode.CAMERA_THIRD_PERSON)
    begin_drawing()
    clear_background(RAYWHITE)
    begin_mode_3d(config.camera)
    draw_grid(20, 1.0)

    for cube in rubik_cube.cubes:
        for cube_part in cube:
            position = Vector3(
                cube[0].center[0],
                cube[0].center[1],
                cube[0].center[2]
            )
            draw_model(cube_part.model, position, 2, cube_part.face_color)

    end_mode_3d()
    end_drawing()
