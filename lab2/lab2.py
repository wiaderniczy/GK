#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def triangle():
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(-50.0, -20.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 55.0)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(50.0, -20.0)
    glEnd()

    glFlush()

def rectangle_lines(x, y, a, b):
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x - a/2, y - b/2)
    glVertex2f(x - a/2, y + b/2)

    glVertex2f(x - a/2, y + b/2)
    glVertex2f(x + a/2, y + b/2)

    glVertex2f(x + a/2, y + b/2)
    glVertex2f(x + a/2, y - b/2)

    glVertex2f(x + a/2, y - b/2)
    glVertex2f(x - a/2, y - b/2)

    glEnd()

    glFlush()

#punkt(x,y) to środek prostokąta
def rectangle(x, y, a, b):
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x - a/2, y - b/2)
    glVertex2f(x - a/2, y + b/2)
    glVertex2f(x + a/2, y + b/2)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x - a/2, y - b/2)
    glVertex2f(x + a/2, y - b/2)
    glVertex2f(x + a/2, y + b/2)
    glEnd()


def render(time):
    #triangle()
    rectangle(0,0,100,50)
    #rectangle_lines(0,0,100,100)

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
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
