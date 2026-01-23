import numpy as np
from pyray import *
import config
from rubik import Rubik
from utils import rotation_queue_from_scramble
init_window(config.window_w,config.window_h, "Solving cube rubik with ML")
rubik_cube = Rubik()

scramble = "U2 R2 D U2 B'"
rotation_queue = rotation_queue_from_scramble(scramble)

set_target_fps(config.fps)
while not window_should_close():
    rotation_queue,_=rubik_cube.handle_rotation(rotation_queue)

    update_camera(config.camera,
                     CameraMode.CAMERA_THIRD_PERSON)
    begin_drawing()
    clear_background(RAYWHITE)
    begin_mode_3d(config.camera)
    draw_grid(20,1.0)
    for cube in rubik_cube.cubes:
        for cube_part in cube:
            position=Vector3(cube[0].center[0], cube[0].center[1], cube[0].center[2])
            print(cube[0].center)
            draw_model(cube_part.model, position,2, cube_part.face_color)
    end_mode_3d()
    end_drawing()

close_window()

