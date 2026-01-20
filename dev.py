import numpy as np
from pyray import *
import config
from rubik import Rubik

init_window(config.window_w,config.window_h, "Solving cube rubik with ML")
rubik_cube = Rubik()
rotation_queue=[(1.5707963267948966, np.array([0,0,1]),2),
                (1.5707963267948966, np.array([1,0,0]),2),
                (1.5707963267948966, np.array([0,0,1]),0)]

set_target_fps(config.fps)
while not window_should_close():
    rotation_queue,_=rubik_cube.handle_rotation(rotation_queue)

    update_camera(config.camera,
                     CameraMode.CAMERA_THIRD_PERSON)
    begin_drawing()
    clear_background(RAYWHITE)
    begin_mode_3d(config.camera)
    draw_grid(20,1.0)
    for i, cube in enumerate(rubik_cube.cubes):
        for cube_part in cube:
            position=Vector3(cube[0].center[0], cube[0].center[1], cube[0].center[2])
            print(cube[0].center)
            draw_model(cube_part.model, position,2, cube_part.face_color)
    end_mode_3d()
    end_drawing()

close_window()

