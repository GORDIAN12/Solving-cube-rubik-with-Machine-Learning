from pyray import *
import numpy as np

class Cube:
    def __init__(self,size,center,face_color):
        self.size=size
        self.center=center
        self.face_color=face_color
        self.orientation=np.eye(3) #Identy matrix representation initial orientation

        #inicializamos la lista vacia para modelos y actualizacion de los colores de las caras
        self.model=None
        self.gen_meshe(size)
        self.create_model()
    def gen_meshe(self,scale:tuple):
        #creamos la malla central del cubo
        self.mesh=gen_mesh_cube(*scale)

    def create_model(self):
        self.model=load_model_from_mesh(self.mesh)
        self.model.transform=matrix_translate(self.center[0],self.center[1],self.center[2])

class Rubik:
    def __init__(self)->None:
        self.cubes=[]
        self.generate_rubik(2)

    def generate_rubik(self,size):
        colors=[WHITE,GREEN,BLUE,RED,YELLOW,ORANGE]
        offset=size-0.7
        size_z=size*0.9,size*0.9,size*0.1
        size_x=size*0.9,size*0.1,size*0.9
        size_y=size*0.1,size*0.9,size*0.9

        for x in range(3):
            for y in range(3):
                for z in range(3):
                    face_colors=[
                        BLACK if z!=2 else colors[0],#FRONT
                        BLACK if z!=0 else colors[1],#BACK
                        BLACK if x!=2 else colors[2],#RIGHT
                        BLACK if x!=0 else colors[3],#LEFT
                        BLACK if y!=2 else colors[4],#TOP
                        BLACK if y!=0 else colors[5],#BOTTOM
                    ]
                    #CENTER
                    center_position=np.array([(x-1)*offset,(y-1)*offset,(z-1)*offset])
                    center=Cube((size, size, size),center_position, BLACK)
                    #FRONT
                    front_position=np.array([center_position[0],center_position[1],center_position[2]+size/2 ])
                    front=Cube(size_z, front_position, face_colors[0])

                    #BACK
                    back_position=np.array([center_position[0],center_position[1],center_position[2]-size/2])
                    back=Cube(size_z, back_position, face_colors[1])

                    #RIGHT
                    right_position=np.array([center_position[0]+size/2,center_position[1],center_position[2]])
                    right=Cube(size_y, right_position, face_colors[2])

                    #LEFT
                    left_position=np.array([center_position[0]-size/2,center_position[1],center_position[2]])
                    left=Cube(size_y, left_position, face_colors[3])

                    #TOP
                    top_position=np.array([center_position[0],center_position[1]+size/2,center_position[2]])
                    top=Cube(size_x, top_position, face_colors[4])

                    #BOTTOM
                    bottom_position=np.array([center_position[0],center_position[1]-size/2,center_position[2]])
                    bottom=Cube(size_x, bottom_position, face_colors[5])

                    self.cubes.append([center,front,back,right,left,top,bottom])

        return self.cubes
                    

