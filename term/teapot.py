from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import random
import math
import numpy as np
from Particle import *

class Teapot(Particle) :

    def __init__(self):
        self.loc = np.array([2.5,0.,2.5])
        self.vel = np.array([0.,0.,0.])
        self.radius = 1.0
        self.mass = 1.0
        self.force = np.array([0., 0., 0.])
        self.gravity = np.array([0., -9.8, 0.])
        self.colPlane = np.array([0., 1., 0., 0.])
        self.Flag = False
        return

    def isSkewed(self) :
        return
    def draw(self) :
        glPushMatrix()
        glTranslatef(self.loc[0], self.loc[1], self.loc[2])
        glutSolidTeapot(0.5)
        glPopMatrix()
    def drawC(self) :
        glPushMatrix()
        glTranslatef(self.loc[0], self.loc[1], self.loc[2])
        glRotated(90.0, 1.0, 0.0, 0.0)
        quad = gluNewQuadric()
        gluCylinder(quad, 1.0, 2.0, 2.0, 3, 3)
        #glutSolidTorus(1.0, 0.5, 3, 3)
        glPopMatrix()

    #def draw(self):
    #    glPushMatrix()
    #    glTranslatef(self.loc[0], self.loc[1], self.loc[2])
    #    glutSolidSphere(self.radius, 20, 20)
    #    glPopMatrix()

    def cdraw(self, color):
        glPushMatrix()
        glColor(color)
        glTranslatef(self.loc[0], self.loc[1], self.loc[2])
        glutSolidSphere(self.radius, 20, 20)
        glPopMatrix()

    def set(self, loc, vel=np.array([0., 0., 0.])):
        self.loc = loc
        self.vel = vel

    def setColPlane(self, N=np.array([0.,1.,0.]), d=0.0) :
        if self.colPlane is None :
            self.colPlane = np.array([0., 1., 0., 0.])
        else :
            self.colPlane[0] = N[0]
            self.colPlane[1] = N[1]
            self.colPlane[2] = N[2]
            self.colPlane[3] = d
    def setColPlaneNone(self) :
        self.colPlane = None
    def setRadius(self, r):
        self.radius = r

    def setMass(self, m):
        self.mass = m
        self.radius = m**(1.0/3.0)

    def setGravity(self, g):
        self.gravity = g

    def addForce(self, f):
        self.force += f

    def resetForce(self):
        self.force = np.array([0., 0., 0.])

    def simulate(self, dt):
        acc = self.gravity + self.force / self.mass
        self.vel = self.vel + acc*dt
            
        self.loc = self.loc + self.vel*dt
    def computeForce(self, other):
        l0 = self.loc
        l1 = other.loc
        m0 = self.mass
        m1 = other.mass
        dir = l1-l0
        r   = np.linalg.norm(dir)
        dir = dir/r
        G = 40.5
        force = (G * m1*m0 / (r**2.0)) *dir
        return force

    def colHandlePair(self, other):
        l0 = self.loc
        l1 = other.loc
        m0 = self.mass
        m1 = other.mass
        v0 = self.vel
        v1 = other.vel
        r0 = self.radius
        r1 = other.radius
        R = r0+r1

        N = l0 - l1
        dist = np.linalg.norm(N)
        N = N/dist

        e = 0.1;

        if dist < R : # collision
            penetration = R - dist
            l0 += (0.5+0.5*e)*penetration * N
            l1 -= (0.5+0.5*e)*penetration * N
            # do velocities snuggle each other ?
            Vrel = v0 - v1
            if np.dot(Vrel, N) < 0:
                # processing collision(update velocity)
                M = m0 + m1
                vp0 = np.dot(N, v0)
                vp1 = np.dot(N, v1)

                J = (1 + e) * (vp1 - vp0) * m0 * m1 / (m0 + m1)

                v0new =  J / m0 + vp0;
                v1new = -J / m1 + vp1;

                self.vel = self.vel - vp0 * N + v0new * N
                other.vel = other.vel - vp1 * N + v1new * N

    def colHandle(self):

        if self.colPlane is None :
            return

        N = np.array([self.colPlane[0], self.colPlane[1], self.colPlane[2]])
        d = self.colPlane[3]
        p0 = d*N

        u = self.loc - p0

        penetration = -np.dot(u,N)
        e = 1.0

        if penetration > -self.radius : # the center through into plane.
            penetration += self.radius
            self.loc += (1+e)*penetration*N
            penVel = -np.dot(self.vel, N)
            if penVel > 0 :
                self.vel = self.vel + (1.+e)*penVel*N
