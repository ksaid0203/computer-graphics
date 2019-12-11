from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import pywavefront
from pywavefront import visualization

scene = pywavefront.Wavefront('teapot_n_glass.obj')

import random
import numpy as np
import math

import Particle
import CGEngine

n = 200

def myRand(start, end) :
    interval = end - start
    return start + interval * random.random()

class mySim(CGEngine.Loading) :

    def __init__(self, w, h, title):
        super(mySim,self).__init__(w,h,title)

        #self.particle = []
        #for i in range(n) :
        #    self.particle.append(Particle.Particle())


        #self.initObjects()


    def initObjects(self):
        root2 = math.sqrt(2.0)
        for i in range(n) :
            #l = np.array([myRand(-6, 6), 0.0, myRand(-6, 6)])
            ll = np.array([0.1, 0.1, 0.1])
            #self.particle[i].set(l,-l*0.1)
            vv = np.array([myRand(-2, 3), myRand(9,11), myRand(-2, 3)])
            self.particle[i].set(ll, vv)

            self.particle[i].setRadius(0.1)
            self.particle[i].setGravity(np.array([0., -9.8, 0.]))

        return



    def frame(self):
        dt = self.getDt()


        super(mySim,self).frame()

        for p in self.particle :
            p.simulate(dt)
            if p.loc[1] < 0.04 :
                ll = np.array([0.1, 0.1, 0.1])
                vv = np.array([myRand(-2, 3), myRand(9,11), myRand(-2, 3)])
                p.loc = ll
                p.vel = vv
            p.colHandle()

        #for i in range(10) :
        #    for j in range(i+1, 10) :
        #        self.particle[i].colHandlePair(self.particle[j])
        #        None

        for p in self.particle :
            p.cdraw([0.0,0.0,1.0,1.0])


        super(mySim,self).afterFrame()
    def frame2(self) :
        super(mySim,self).frame()
        visualization.draw(scene)
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
    ani.frame2()

ani.start(draw, key)
