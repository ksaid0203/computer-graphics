from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from math import *


"""
메뉴 추가
카메라 위치
"""
    

##############################################################################
# vertices
##############################################################################

vertices=[#정점의 좌표
        -0.25,-0.25,0.25,
        -0.25,0.25,0.25,
        0.25,0.25,0.25,
        0.25,-0.25,0.25,
        -0.25,-0.25,-0.25,
        -0.25,0.25,-0.25,
        0.25,0.25,-0.25,
        0.25,-0.25,-0.25,
        ]
colors=[#각 정점의 색깔을 정의함 
        0.2,0.2,0.2,
        1.0,0.0,0.0,
        1.0, 1.0, 0.0,
        0.0,1.0,0.0,
        0.0,0.0,1.0,
        1.0,0.0,1.0,
        1.0,1.0,1.0,
        0.0,1.0,1.0,
        ]
indices=[ #정점 리스트 : 6면을 4개의 정점으로 한 면을 정의함
        0,3,2,1,
        2,3,7,6,
        0,4,7,3,
        1,2,6,5,
        4,5,6,7,
        0,1,5,4,
        ]

Angle=0.0

##############################################################################
def init():
    glClearColor (1.0, 1.0, 1.0, 1.0)

def drawAxis():
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    glVertex3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, 1, 0.0)
    glEnd()
    glBegin(GL_LINES)
    glColor3f(0,1,0)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f(1, 0.0, 0.0)
    glEnd()
    glBegin(GL_LINES)
    glColor3f(0,0,1)
    glVertex3f(0.0, 0.0, -1)
    glVertex3f(0.0, 0.0, 1)
    glEnd()
    
    
def MyTimer(Value):
    global Angle
    
    Angle += 0.01
    glutPostRedisplay()
    glutTimerFunc(40,MyTimer,1)

def reshape_func(w, h):
    glViewport(0,0,w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60,1.0,0.01,20.0)

def disp_func():
    # clear
    glClear(GL_COLOR_BUFFER_BIT)
    glFrontFace(GL_CCW);							
    glEnable(GL_CULL_FACE);	
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices) #정점변수 설정
    glColorPointer(3, GL_FLOAT, 0, colors)#정점색 저장변수 지정

    # view
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(3.0*cos(Angle),1,3*sin(Angle), #카메라위치->perspective때는허용됨
              0.0, 0.0, 0.0,#초점
              0.0,1.0, 0.0) #카메라방향

    drawAxis()
    glPushMatrix()
    glRotatef(30.0, 1.0, 1.0, 1.0)
    
    #for i in range(6):
    #    glDrawElements(GL_POLYGON,4,GL_UNSIGNED_BYTE, indices[4*i])
    glDrawElements(GL_QUADS, 24, GL_UNSIGNED_BYTE,indices) # 4각매쉬로, 24개 정점

    glPopMatrix()
    
    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)
    glFlush()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGBA) # double buffering?
	# frame buffer에 있다가 display하는
	# 1개만 하면 껌뻑거림 현상
	# 다음 버퍼를 그림
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"Vertex Handling")
    init()    

    glutDisplayFunc(disp_func)
    glutTimerFunc(40,MyTimer,1)
    glutReshapeFunc(reshape_func)


    glutMainLoop()

if __name__=="__main__":
    main()

