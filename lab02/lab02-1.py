from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

TopLeftX = 0
TopLeftY = 0
BottomRightX = 0
BottomRightY = 0
"""
이벤트핸들링이 어떻게 하는지 보자
"""
def MyDisplay():
    glViewport(0, 0, 300, 300)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_POLYGON)
    glVertex3f(TopLeftX/300.0, (300-TopLeftY)/300.0, 0.0)
    glVertex3f(TopLeftX/300.0, (300-BottomRightY)/300.0, 0.0)
    glVertex3f(BottomRightX/300.0, (300-BottomRightY)/300.0, 0.0)
    glVertex3f(BottomRightX/300.0, (300-TopLeftY)/300.0, 0.0)
    glEnd()
    glFlush()

def MyMouseClick(Button, State, X, Y):
    global TopLeftX, TopLeftY
    if Button==GLUT_LEFT_BUTTON and State == GLUT_DOWN: # glut Document
        TopLeftX = X
        TopLeftY = Y   

def MyMouseMove(X, Y):
    global BottomRightX, BottomRightY
    BottomRightX = X
    BottomRightY = Y
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowSize(300, 300) # glut의 윈도우 크기
    glutInitWindowPosition(0, 0) # glut의 윈도우 위치
    glutCreateWindow(b"OpenGL Drawing Example")  # not only string, put 'b' in front of string.
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION) # gl projection
    glLoadIdentity()
    glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)
    glutDisplayFunc(MyDisplay)
    glutMouseFunc(MyMouseClick) # mouse event
    glutMotionFunc(MyMouseMove) # motion event
    glutMainLoop()

if __name__ == '__main__':
    main()
