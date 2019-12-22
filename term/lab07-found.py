from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import random
import numpy as np
import math

import Particle
import CGEngine
import teapot
import cup

n = 200

def myRand(start, end) :
    interval = end - start
    return start + interval * random.random()

def juhoDist(me, other) :
    result = me - other
    dist = np.linalg.norm(result)

    return dist

class mySim(CGEngine.Loading) :
    def __init__(self, w, h, title):
        super(mySim,self).__init__(w,h,title)

        self.particle = []
        for i in range(n) :
            self.particle.append(Particle.Particle())

        self.cup = cup.Cup()
        self.teapot = teapot.Teapot()
        self.initObjects()

    def initObjects(self):
        root2 = math.sqrt(2.0)

        for i in range(n) :
            ll = np.array([0.0, 7.0, 0.0])
            vv = np.array([0.0, 0.0, 0.0])
            self.particle[i].set(ll, vv)

            self.particle[i].setRadius(0.2)
            self.particle[i].setGravity(np.array([0., -9.8, 0.]))
        return

    def frame(self):
        dt = self.getDt()

        super(mySim,self).frame()

        for p in self.particle :
            p.simulate(dt)
            
            if juhoDist(self.cup.loc, p.loc) <= 0.1 :
                vv = np.array([0,0,0])
                p.vel = vv
                p.setRadius(0.06)
                p.setGravity(np.array([0.,0.,0.]))
            p.colHandle()

        self.cup.draw()
        self.teapot.draw()
        print(self.teapot.isSkewed())
        for p in self.particle :
            p.cdraw([0.0,0.0,1.0,1.0])

        self.teapot.colHandlePair(self.cup)

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
