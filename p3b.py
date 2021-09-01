# coding=utf-8
"""Dibujo de un paisaje simple utilizando los elementos creados"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import grafica.easy_shaders as es
import grafica.basic_shapes as bs
from grafica.gpu_shape import GPUShape, SIZE_IN_BYTES


# We will use 32 bits data, so floats and integers have 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    else:
        print('Unknown key')

# Funcion para crear el cielo con 
# y0 la altura superior
# yf la altura inferior
def createSky(y0, yf):
    # Defining locations and colors for each vertex of the shape
    #####################################
    color1 = [0.0, 0.6, 0.8]
    color0 = [0.7, 1.0, 1.0]

    vertexData = np.array([
    #   positions        colors
        -1.0, yf, 0.0,  color1[0], color1[1], color1[2],
         1.0, yf, 0.0,  color1[0], color1[1], color1[2],
         1.0,  y0, 0.0,  color0[0], color0[1], color0[2],
        -1.0,  y0, 0.0,  color0[0], color0[1], color0[2]
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    return bs.Shape(vertexData, indices)
    
# Funcion para crear un rectangulo con 
# y0 la altura superior
# yf la altura inferior
# color0 un arreglo con el color rgb superior
# color1 un arreglo con el color rgb inferior
def createRect(y0, yf, color0, color1):
    # Defining locations and colors for each vertex of the shape
    #####################################

    vertexData = np.array([
    #   positions        colors
        -1.0, yf, 0.0,  color1[0], color1[1], color1[2],
         1.0, yf, 0.0,  color1[0], color1[1], color1[2],
         1.0,  y0, 0.0,  color0[0], color0[1], color0[2],
        -1.0,  y0, 0.0,  color0[0], color0[1], color0[2]
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    size = len(indices)
    return bs.Shape(vertexData, indices)
    
# Funcion para crear una montaña con 
# color0 un arreglo con el color rgb superior
# color1 un arreglo con el color rgb inferior
def createMountain(color0, color1):

    # Defining locations and colors for each vertex of the shape
    #####################################
    
    vertexData = np.array([
    #   positions        colors
        -0.5, -0.5, 0.0,  color1[0], color1[1], color1[2],
         0.5, -0.5, 0.0,  color1[0], color1[1], color1[2],
         0.0,  0.5, 0.0,  color0[0], color0[1], color0[2],
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2], dtype= np.uint32)

    size = len(indices)
    return bs.Shape(vertexData, indices)

# Funcion para crear un triangulo con 
# pos0 coordenadas del vertice inferior izquierdo
# pos1 coordenadas del vertice inferior derecho
# pos2 coordenadas del vertice superior
# color0 un arreglo con el color rgb superior
# color1 un arreglo con el color rgb inferior
def createTriangle(pos0, pos1, pos2, color0, color1):

    # Defining locations and colors for each vertex of the shape
    #####################################
    
    vertexData = np.array([
    #   positions        colors
        pos0[0], pos0[1], 0.0,  color1[0], color1[1], color1[2],
        pos1[0], pos1[1], 0.0,  color1[0], color1[1], color1[2],
        pos2[0], pos2[1], 0.0,  color0[0], color0[1], color0[2],
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2], dtype= np.uint32)

    size = len(indices)
    return bs.Shape(vertexData, indices)

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Dibujo de paisaje simple", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleShaderProgram()


    # Creating shapes on GPU memory

    # 1- Creamos la Figura del cielo en la GPU
    skyShape = createSky(1.0, -0.5) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpuSky = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    pipeline.setupVAO(gpuSky) # Se le dice al pipeline como leer esta parte de la memoria 
    gpuSky.fillBuffers(skyShape.vertices, skyShape.indices, GL_STATIC_DRAW) # Llenamos esta memoria de la GPU con los vertices e indices

    # 2- Creamos la Figura del pasto en la GPU
    grassShape = createRect(-0.5, -1.0, [0.0, 1.0, 0.0], [0.0, 0.6, 0.0]) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpuGrass = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    pipeline.setupVAO(gpuGrass) # Se le dice al pipeline como leer esta parte de la memoria 
    gpuGrass.fillBuffers(grassShape.vertices, grassShape.indices, GL_STATIC_DRAW) # Llenamos esta memoria de la GPU con los vertices e indices

    # 3- Creamos la Figura de la montaña en la GPU
    mountainShape = createMountain([1.0, 1.0, 1.0],[0.0, 0.7, 0.0]) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpuMountain = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    pipeline.setupVAO(gpuMountain) # Se le dice al pipeline como leer esta parte de la memoria  
    gpuMountain.fillBuffers(mountainShape.vertices, mountainShape.indices, GL_STATIC_DRAW)  # Llenamos esta memoria de la GPU con los vertices e indices

    # 4- Creamos la Figura de la carpa en la GPU
    tentShape = createTriangle(pos0=[-0.8, -0.8], pos1=[-0.4, -0.8], pos2=[-0.6, -0.4], color0=[1.0, 1.0, 0.0], color1=[1.0, 0.0, 0.0]) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpuTent = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    pipeline.setupVAO(gpuTent) # Se le dice al pipeline como leer esta parte de la memoria 
    gpuTent.fillBuffers(tentShape.vertices, tentShape.indices, GL_STATIC_DRAW)  # Llenamos esta memoria de la GPU con los vertices e indices
    
    
    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Se le dice a OpenGL que use el shaderProgram simple
        glUseProgram(pipeline.shaderProgram)

        pipeline.drawCall(gpuSky) # Se dibuja el cielo
        pipeline.drawCall(gpuGrass) # Se dibuja el pasto
        pipeline.drawCall(gpuMountain)  # Se dibuja la montaña
        pipeline.drawCall(gpuTent) # Se dibuja la carpa

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuMountain.clear()
    gpuTent.clear()
    gpuSky.clear()
    gpuGrass.clear()

    glfw.terminate()
