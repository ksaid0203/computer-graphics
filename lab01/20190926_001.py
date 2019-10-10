from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
# pyopengl package를 활용하여 opengl api를 구현한 python sample code이다
# 검정 배경에 흰 네모가 나온다
def MyDisplay() :
	glClear(GL_COLOR_BUFFER_BIT)
	glBegin(GL_POLYGON)
	glVertex3f(-0.5,-0.5,0.0)
	glVertex3f(0.5,-0.5,0.0)
	glVertex3f(0.5,0.5,0.0)
	glVertex3f(-0.5,0.5,0.0)
	glEnd()
	glFlush()
	
def main() :
	glutInit()
	glutCreateWindow(b"OpenGL Drawing Example")
	
	glutDisplayFunc(MyDisplay)
	glutMainLoop()
	
if __name__ == '__main__' :
	main()
	
#predict.py -- tf -- keras loadh5 t7

#inpaint.py 