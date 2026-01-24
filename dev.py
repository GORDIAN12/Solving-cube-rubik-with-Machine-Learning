from pyray import *
from rubik import Rubik
from utils import *
import config
from scramble import move_scram
from ML import searching

init_window(config.window_w, config.window_h, "Solving cube rubik with ML")
rubik_cube = Rubik()

# 1) Generar scramble
movs = move_scram.generate_movs(5)
print("SCRAMBLE:", movs)

# 2) Generar cola de rotación visual para el scramble
rotation_queue = rotation_queue_from_scramble(movs)

# 3) Aplicar scramble al estado lógico
state_scrambled = move_scram.apply_scramble(
    move_scram.SOLVED_STATE.copy(),
    movs,
    move_scram.PERM
)

rotation_scramble=invert_scramble(movs)
print("ROTATION SCRAMBLE",rotation_scramble)
rotation_cube=rotation_queue_from_scramble(rotation_scramble)
"""
# 4) Encontrar solución con IDDFS
sol = searching.iddfs_solve(state_scrambled, move_scram.PERM, move_scram.SOLVED_STATE, max_depth=10)
print("Solución encontrada:", sol)

# 5) Convertir solución a cola
solution_queue = rotation_queue_from_scramble(sol) if sol is not None else []
print("SOLUTION", solution_queue)
print(f"Total movimientos en solución: {len(solution_queue)}")
"""
# Flags de control
animating_scramble = True
animation_complete = False

set_target_fps(config.fps)
while not window_should_close():
    # CRÍTICO: Siempre llamar handle_rotation para completar animaciones en progreso
    if animating_scramble:
        if rotation_queue or rubik_cube.is_rotating:  # ← CAMBIO CLAVE
            rotation_queue, _ = rubik_cube.handle_rotation(rotation_queue)
        else:
            rotation_cube, _ = rubik_cube.handle_rotation(rotation_cube)
            # Solo cambiar cuando la cola esté vacía Y no haya rotación en progreso
            #print(f"✓ Scramble completado ({len(rotation_queue)} en cola, rotating={rubik_cube.is_rotating})")
            #animating_scramble = False
    else:
        if solution_queue or rubik_cube.is_rotating:  # ← CAMBIO CLAVE
            solution_queue, _ = rubik_cube.handle_rotation(solution_queue)
        else:
            if not animation_complete:
                print(f"✓ ¡Cubo resuelto! ({len(solution_queue)} en cola, rotating={rubik_cube.is_rotating})")
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