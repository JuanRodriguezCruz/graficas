# coding=utf-8
"""Dibujo del cuadrado basico sin utilizar EBO (solamente vertices)"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np


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


def createShaderProgram():
    
    # Defining shaders for our pipeline
    vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    void main()
    {
        fragColor = color;
        gl_Position = vec4(position, 1.0f);
    }
    """

    fragment_shader = """
    #version 330

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor, 1.0f);
    }
    """

    # Binding artificial vertex array object for validation
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    return shaderProgram


def createQuad(shaderProgram):

    # Defining locations and colors for each vertex of the shape
    #####################################
    
    vertexData = np.array([
    #   positions        colors
        -0.5, -0.5, 0.0,  1.0, 0.0, 0.0, #0
         0.5, -0.5, 0.0,  0.0, 1.0, 0.0, #1
         0.5,  0.5, 0.0,  0.0, 0.0, 1.0, #2

         0.5,  0.5, 0.0,  0.0, 0.0, 1.0, #3
        -0.5,  0.5, 0.0,  1.0, 1.0, 1.0, #4
        -0.5, -0.5, 0.0,  1.0, 0.0, 0.0  #5
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # VAO, VBO and EBO and  for the shape
    #####################################
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    # Binding VBO and EBO to the VAO
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBindVertexArray(0)

    # Setting up stride in the Vertex Attribute Object (VAO)
    #####################################
    glBindVertexArray(vao)

    # Setting up the location of the attributes position and color from the VBO
    # A vertex attribute has 3 integers for the position (each is 4 bytes),
    # and 3 numbers to represent the color (each is 4 bytes),
    # Henceforth, we have 3*4 + 3*4 = 24 bytes
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 6 * SIZE_IN_BYTES, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    
    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 6 * SIZE_IN_BYTES, ctypes.c_void_p(3 * SIZE_IN_BYTES))
    glEnableVertexAttribArray(color)

    # unbinding current vao
    glBindVertexArray(0)

    # Sending vertices and indices to GPU memory
    #####################################
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * SIZE_IN_BYTES, vertexData, GL_STATIC_DRAW)
    return vao, vbo
    

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Drawing a quad without EBO", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
    # Creating our shader program and telling OpenGL to use it
    shaderProgram = createShaderProgram()
    glUseProgram(shaderProgram)

    # Creating shapes on GPU memory
    vao, vbo = createQuad(shaderProgram)
    
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

        # Drawing the Quad as specified in the VAO without indices
        glBindVertexArray(vao)
        #            draw_mode,   pointer=0, vertex_count 
        vertexCount = 6
        glDrawArrays(GL_TRIANGLES, 0, vertexCount)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    glDeleteBuffers(1, [vbo])
    glDeleteVertexArrays(1, [vao])

    glfw.terminate()
