from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import random
import numpy as np
import math

import Particle
import CGEngine
import teapot

n = 400
nn = 40
theta = 0.5

def myRand(start, end) :
    interval = end - start
    return start + interval * random.random()

class mySim(CGEngine.Loading) :

    def __init__(self, w, h, title):
        super(mySim,self).__init__(w,h,title)
        self.steam = []
        self.particle = []
        for i in range(n) :
            #self.particle.append(Particle.Particle())
            self.steam.append(Particle.Particle())

        for i in range(nn) :
            self.particle.append(Particle.Particle())
        self.teapot = teapot.Teapot()
        self.initObjects()

    def initObjects(self):
        root2 = math.sqrt(2.0)
        for i in range(n) :
            vv = np.array([myRand(-2, 3), myRand(2,11), myRand(-2, 3)])
            self.steam[i].set(self.teapot.lid, vv)

            self.steam[i].setRadius(0.04)
            self.steam[i].setGravity(np.array([0., 2.0, 0.]))

        for i in range(nn ) :
            vv = np.array([0.0, 0.0, 0.0])
            self.particle[i].set(self.teapot.lid, vv)
            self.particle[i].setRadius(0.2)
            self.particle[i].setGravity(np.array([0., -9.8, 0.]))
        return

    def frame(self):
        global theta
        dt = self.getDt()

        super(mySim,self).frame()

        for p in self.steam :
            p.simulate(dt)
            if p.loc[1] >= 6 :
                ll = self.teapot.lid
                vv = np.array([myRand(-2, 2), myRand(2,11), myRand(-2, 2)])
                p.loc = ll
                p.vel = vv

        for p in self.particle :
            p.simulate(dt)
            if self.teapot.hand == False:
                p.loc = self.teapot.lid
            if p.loc[1] < 0.04 :
                ll = self.teapot.lid
                vv = np.array([0.0 ,0.0, 0.0])
                p.loc = ll
                p.vel = vv
        #self.particle = [ particle for particle in self.particle if particle.loc[1] > 0 ]
        #if self.teapot.hand :
        #    for p in self.particle :
        #        p.simulate(dt)

        self.teapot.draw(theta)
        if self.teapot.hand :
            self.teapot.rotateT(theta, self.teapot.axis)
        for p in self.particle :
            p.cdraw([0.0,0.0,1.0,1.0])
        for p in self.steam :
            p.cdraw([1.0,1.0,1.0,1.0])

        super(mySim,self).afterFrame()

ani = mySim(500,500, b"Lab07-3:Collision")
ani.grid(True)
ani.timerStart()

def key(k, x, y) :
    global theta
    #if k == b' ':
    #    if ani.timer.timerRunning:
    #        ani.timerStop()
    #    else:
    #        ani.timerStart()
    if k == b'r':
        ani.initObjects()


def draw():
    ani.frame()

ani.start(draw, key)
