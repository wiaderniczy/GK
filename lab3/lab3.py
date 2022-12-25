#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

n = 25

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def egg_points():
    points = [[[0.0] * 3 for k in range(n)] for k in range(n)]

    for i in range(n):
        u = 1 / (n - 1) * i
        for j in range(n):
            v = 1 / (n - 1) * j

            points[i][j][0] = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) \
                              * math.cos(math.pi * v)
            points[i][j][1] = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
            points[i][j][2] = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) \
                              * math.sin(math.pi * v)

    return points


def egg_points_render():
    points = egg_points()

    for i in range (n):
        for j in range (n):
            glColor3f(1.0, 0.0, 0.0)
            glBegin(GL_POINTS)

            glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])

            glEnd()


def egg_lines_render():
    points = egg_points()

    for i in range(n):
        for j in range(n):
            if i == n - 1:
                nextI = 0
            else:
                nextI = i + 1

            if j == n - 1:
                nextJ = 0
            else:
                nextJ = j + 1

            glColor3f(1.0, 0.420, 0.69)
            glBegin(GL_LINES)

            glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
            glVertex3f(points[nextI][j][0], points[nextI][j][1], points[nextI][j][2])

            glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
            glVertex3f(points[i][nextJ][0], points[i][nextJ][1], points[i][nextJ][2])

            glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 90/ 3.1415)

    egg_lines_render()
    #egg_points_render()
    #axes()

    glFlush()


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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
