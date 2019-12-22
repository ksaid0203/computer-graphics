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

        self.theta = 0.0
        self.teapot = teapot.Teapot()
        self.initObjects()

    def initObjects(self):
        root2 = math.sqrt(2.0)
        for i in range(n) :
            vv = np.array([myRand(-2, 3), myRand(2,11), myRand(-2, 3)])
            self.steam[i].set(self.teapot.lid, vv)

            self.steam[i].setRadius(0.04)
            self.steam[i].setGravity(np.array([0., 2.0, 0.]))

        return

    def frame(self):
        dt = self.getDt()

        super(mySim,self).frame()

        for p in self.steam :
            p.simulate(dt)
            if p.loc[1] >= 6 :
                ll = self.teapot.lid
                vv = np.array([myRand(-2, 2), myRand(2,11), myRand(-2, 2)])
                p.loc = ll
                p.vel = vv
            #p.colHandle()

        self.teapot.draw(self.theta)
        self.theta += 0.1
        #self.teapot.rotateR(theta)
        for p in self.particle :
            p.cdraw([0.0,0.0,1.0,1.0])
        for p in self.steam :
            p.cdraw([1.0,1.0,1.0,1.0])

        super(mySim,self).afterFrame()

ani = mySim(500,500, b"Lab07-3:Collision")
ani.grid(True)


def key(k, x, y) :
    if k == b' ':
        if ani.timer.timerRunning:
            ani.timerStop()
        else:
            ani.timerStart()
    if k == b'r':
        ani.initObjects()


def draw():
    ani.frame()

ani.start(draw, key)
