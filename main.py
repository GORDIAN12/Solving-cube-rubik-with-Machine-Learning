from pyray import *
import config
from rubik import Rubik
from scramble import move_scram
from utils import *

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
    movs_str,
    move_scram.PERM
)

solution_queue = []
animating_scramble = True
solving_started = False
animation_complete = False
set_target_fps(config.fps)

opc=input("da una opcion a realizar 1. retroceso 2. IDDFS 3. MODELO IA")

if opc=="1":
    print("1. simular cubo rubik con retroceso")
    rotation_scramble = invert_scramble(movs)
    print("ROTATION SCRAMBLE", rotation_scramble)
    rotation_cube = rotation_queue_from_scramble(rotation_scramble)
elif opc=="2":
    print("2. simular cubo rubik IDDFS")
elif opc=="3":
    print("3. simular cubo rubik con modelo de entrenamiento")

animating_scramble = True
animation_complete = False

set_target_fps(config.fps)
while not window_should_close():
    if animating_scramble:
        if rotation_queue or rubik_cube.is_rotating:
            rotation_queue, _ = rubik_cube.handle_rotation(rotation_queue)
        else:
            rotation_cube, _ = rubik_cube.handle_rotation(rotation_cube)
            animating_scramble = False
    else:
        if rotation_cube or rubik_cube.is_rotating:
            rotation_cube, _ = rubik_cube.handle_rotation(rotation_cube)
        else:
            if not animation_complete:
                print(f"✓ ¡Cubo resuelto! ({len(rotation_cube)} en cola, rotating={rubik_cube.is_rotating})")
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




