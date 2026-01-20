from pyray import *
import config


init_window(config.window_w,config.window_h, "Solving cube rubik with ML")

set_target_fps(config.fps)
while not window_should_close():
    update_camera(config.camera,
                     CameraMode.CAMERA_ORBITAL)
    begin_drawing()
    clear_background(RAYWHITE)
    begin_mode_3d(config.camera)
    draw_grid(20,1.0)
    end_mode_3d()
    end_drawing()

close_window()

