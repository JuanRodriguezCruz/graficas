import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy 
import sys

__author__ = "Ivan Sipiran"
__license__ = "MIT"

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4

def crear_dama(x,y,r,g,b,radius):
    
    circle = []
    for angle in range(0,360,10):
        circle.extend([x, y, 0.0, r, g, b])
        circle.extend([x+numpy.cos(numpy.radians(angle))*radius, 
                       y+numpy.sin(numpy.radians(angle))*radius, 
                       0.0, r, g, b])
        circle.extend([x+numpy.cos(numpy.radians(angle+10))*radius, 
                       y+numpy.sin(numpy.radians(angle+10))*radius, 
                       0.0, r, g, b])
    
    return numpy.array(circle, dtype = numpy.float32)

def createQuad( tablero, x, y , color):
    
    tablero.extend([x/4.0, y/4.0, 0.0 ,color, color, color])
    tablero.extend([x/4.0, (y-1)/4.0, 0.0, color, color,color])
    tablero.extend([(x+1)/4.0, y/4.0, 0.0, color,color,color])

    tablero.extend([(x+1)/4.0, y/4.0, 0.0, color,color,color])
    tablero.extend([(x+1)/4.0, (y-1)/4.0, 0.0, color, color, color])
    tablero.extend([x/4.0, (y-1)/4.0, 0.0 ,color, color, color])


def crear_tablero():
    
    tablero = []
    for x in range(-4,4,1):
        for y in range(4,-4,-1):
            if ((x+y)%2==0):
                createQuad(tablero,x,y,0.0)
            else:
                createQuad(tablero,x,y,1.0)
    return numpy.array(tablero, dtype = numpy.float32)

def crear_enemigo():
    damas = []
    for y in [0.875,0.625]:
        for x in range(0,8):
            damas.extend(crear_dama(-0.875+(x*0.25),y,0.0,1.0,0.0,0.1))
        
    return numpy.array(damas, dtype= numpy.float32)


def crear_player():
    damas = []
    for y in [-0.875,-0.625]:
        for x in range(0,8):
            damas.extend(crear_dama(-0.875+(x*0.25),y,1.0,0.0,0.0,0.1))
        
    return numpy.array(damas, dtype= numpy.float32)

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Tarea 1", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    dama = crear_enemigo()
    dama = numpy.append(dama, crear_player())
    tablero = crear_tablero()
    print(tablero)

    # Defining shaders for our pipeline
    vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;

    out vec3 newColor;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """

    fragment_shader = """
    #version 330
    in vec3 newColor;

    out vec4 outColor;
    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """

    # Binding artificial vertex array object for validation
    tableroVAO = glGenVertexArrays(1)
    glBindVertexArray(tableroVAO)

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # Each shape must be attached to a Vertex Buffer Object (VBO)
    vboTablero = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vboTablero)
    glBufferData(GL_ARRAY_BUFFER, len(tablero) * SIZE_IN_BYTES, tablero, GL_STATIC_DRAW)

    

    

    glClear(GL_COLOR_BUFFER_BIT)

    glBindBuffer(GL_ARRAY_BUFFER, vboTablero)
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    glBindVertexArray(0)
    
    # It renders a scene using the active shader program (pipeline) and the active VAO (shapes)
    

    #--------------------------------------------------------------
    damaVAO = glGenVertexArrays(1)
    glBindVertexArray(damaVAO)
    vboDama = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vboDama)
    glBufferData(GL_ARRAY_BUFFER, len(dama) * SIZE_IN_BYTES, dama, GL_STATIC_DRAW)

   

  
    glBindBuffer(GL_ARRAY_BUFFER, vboDama)
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)
    # Setting up the clear screen color
    glClearColor(0.5,0.5, 0.5, 1.0)
    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)
    
    # It renders a scene using the active shader program (pipeline) and the active VAO (shapes)
    glBindVertexArray(tableroVAO)
    glDrawArrays(GL_TRIANGLES, 0, int(len(tablero)/6))
    glBindVertexArray(damaVAO)
    glDrawArrays(GL_TRIANGLES, 0, int(len(dama)/6))

    # Moving our draw to the active color buffer
    glfw.swap_buffers(window)

    # Waiting to close the window
    while not glfw.window_should_close(window):

        # Getting events from GLFW
        glfw.poll_events()
        
    glfw.terminate()