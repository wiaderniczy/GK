#!/usr/bin/env python3
import sys
import  math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

#------------------------------------------------------
#   GUIDE DO TEKSTUR (KTÓRY KLAWISZ DO KTÓREJ TEKSTURY)
#   megamind = M
#   baller = B
#   tosia = T
#   tekstura.tga = D
#------------------------------------------------------
viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

phi_light = 0.0
theta_light = 0.0

r = 10.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0
hide_wall = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.3, 0.3, 0.3, 1.0]
light_diffuse = [0.5, 0.5, 0.5, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 10.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

def light_1():
    light_position[0] = math.cos(theta_light * math.pi / 180) * math.cos(phi_light * math.pi / 180) * r
    light_position[1] = math.sin(phi_light * math.pi / 180) * r
    light_position[2] = math.sin(theta_light * math.pi / 180) * math.cos(phi_light * math.pi / 180) * r

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

def shutdown():
    pass

def getTexture(string):
    megamind = Image.open("megamind.tga")
    default = Image.open("tekstura.tga")
    baller = Image.open("baller.tga")
    tosia = Image.open("tosia.tga")

    if (string == "M"):
        image = megamind
    if (string == "D"):
        image = default
    if (string == "B"):
        image = baller
    if (string == "T"):
        image = tosia

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )

def render(time):
    global theta
    global phi
    global theta_light
    global phi_light

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    light_1()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
    
    if right_mouse_button_pressed: 
        theta_light += delta_x * pix2angle
        phi_light += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    glBegin(GL_POLYGON)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-3.0, 0.0, -3.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(3.0, 0.0, -3.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(3.0, 0.0, 3.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-3.0, 0.0, 3.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-3.0, 0.0, -3.0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 5.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(3.0, 0.0, -3.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(3.0, 0.0, -3.0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 5.0, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(3.0, 0.0, 3.0)
    glEnd()

    if hide_wall == 0:
        glBegin(GL_TRIANGLES)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(3.0, 0.0, 3.0)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 5.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-3.0, 0.0, 3.0)
        glEnd()

    
    glBegin(GL_TRIANGLES)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-3.0, 0.0, 3.0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 5.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-3.0, 0.0, -3.0)
    glEnd()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global hide_wall
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_M and action == GLFW_PRESS:
        getTexture("M")
    if key == GLFW_KEY_D and action == GLFW_PRESS:
        getTexture("D")
    if key == GLFW_KEY_B and action == GLFW_PRESS:
        getTexture("B")
    if key == GLFW_KEY_T and action == GLFW_PRESS:
        getTexture("T")
    
    if key == GLFW_KEY_KP_SUBTRACT and action == GLFW_PRESS:
        hide_wall = 1
    if key == GLFW_KEY_KP_ADD and action == GLFW_PRESS:
        hide_wall = 0


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
