from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import random
import numpy as np
import math
import time
import Particle
import Hand
import CGEngine
import Joint
#import Animator
import teapot

upCnt =0
downCnt = 0
leftCnt = 0
rightCnt = 0

n = 400
nn = 40
theta = 0.5

def solidCube(cubeVertices,cubeQuads):
    glBegin(GL_QUADS)
    cubeVertices = np.array(cubeVertices)
    cubeQuads = np.array(cubeQuads)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()


def makeCubeInfo( arg):
    baseInfo = arg[0]
    plusInfo = arg[1]
    vertices0 = (baseInfo[0], baseInfo[1], baseInfo[2],1)
    vertices1 = (baseInfo[0], baseInfo[1], baseInfo[2] + plusInfo[2],1)
    vertices2 = (baseInfo[0] + plusInfo[0], baseInfo[1], baseInfo[2] + plusInfo[2],1)
    vertices3 = (baseInfo[0] + plusInfo[0], baseInfo[1], baseInfo[2],1)
    vertices4 = (baseInfo[0], baseInfo[1] - plusInfo[1], baseInfo[2],1)
    vertices5 = (baseInfo[0], baseInfo[1] - plusInfo[1], baseInfo[2] + plusInfo[2],1)
    vertices6 = (baseInfo[0] + plusInfo[0], baseInfo[1] - plusInfo[1], baseInfo[2] + plusInfo[2],1)
    vertices7 = (baseInfo[0] + plusInfo[0], baseInfo[1] - plusInfo[1], baseInfo[2],1)
    return (vertices0, vertices1, vertices2, vertices3, vertices4, vertices5, vertices6, vertices7)


baseY = 7
jointLocation = {'space' : [[-3,baseY,0] ,[7,4,4] ],
                 'b' : [[5,baseY,0],[4,3,2]],
                 'g' : [[10,baseY,0],[4,1,0.5]],
                 'y' : [[10,baseY,1],[4,1,0.5]],
                 'h' : [[10,baseY,2],[4,1,0.5]],
                 'n' : [[10,baseY,3],[4,1,0.5]],
                 }
jointSpaceRoot = Joint.Joint(1 , "space" ,np.identity(4) ,makeCubeInfo(jointLocation.get('space')))
jointBLoc =[5,0,0]
jointB = Joint.Joint(2,   "b",   np.array([[1,0,0,7],[0,1,0,0],[0,0,1,0],[0,0,0,1]])   ,makeCubeInfo(jointLocation.get('b'))   )

jointG = Joint.Joint(4,"g" , np.array([[1,0,0,5],[0,1,0,0],[0,0,1,0],[0,0,0,1]])  ,makeCubeInfo(jointLocation.get('g'))   )
jointY = Joint.Joint(4,"y" , np.array([[1,0,0,5],[0,1,0,0],[0,0,1,0],[0,0,0,1]])  ,makeCubeInfo(jointLocation.get('y'))   )
jointH = Joint.Joint(4,"h" , np.array([[1,0,0,5],[0,1,0,0],[0,0,1,0],[0,0,0,1]])   ,makeCubeInfo(jointLocation.get('h'))   )
jointN = Joint.Joint(4,"n" , np.array([[1,0,0,5],[0,1,0,0],[0,0,1,0],[0,0,0,1]])   ,makeCubeInfo(jointLocation.get('n'))   )

jointB.addChild(jointG)
jointB.addChild(jointY)
jointB.addChild(jointH)
jointB.addChild(jointN)

jointSpaceRoot.addChild(jointB)

# joint 다 초기화하고 animatedModel 만들어야지

Hand  = Hand.Hand( jointSpaceRoot)
print(np.array([1,2,3]).shape)
print(jointSpaceRoot)

# print(2)
backCount = 0
handState = False

cubeOrder = ((0,1,2,3),(1,2,6,5),(2,3,7,6),(0,1,5,4),(0,3,2,4),(4,7,6,5))
def myRand(start, end) :
    interval = end - start
    return start + interval * random.random()

class mySim(CGEngine.Loading) :

    def __init__(self, w, h, title):
        super(mySim,self).__init__(w,h,title)

        self.curTime = time.time()
        self.particle = []
        self.steam = []

        #self.nParticle = 40
        self.particleVel = 3
        self.particleRadius = 0.05
        for i in range(nn) :
            self.particle.append(Particle.Particle())
        for i in range(n) :
            self.steam.append(Particle.Particle())
 
        self.collisionCnt = [0] * len(self.particle)

        self.teapot = teapot.Teapot()
        self.teapot.hand = False
        self.initObjects()
        self.setBackground(b"bg_cosmos.jpg")
        #self.background = [b"bg_cosmos.jpg"]

    def initObjects(self):
        global n , nn
        root2 = math.sqrt(2.0)
        for i in range(n) :
            vv = np.array([myRand(-2, 3), myRand(2,11), myRand(-2, 3)])
            self.steam[i].set(self.teapot.lid, vv)

            self.steam[i].setRadius(0.04)
            self.steam[i].setGravity(np.array([0., 2.0, 0.]))

        for i in range(nn) :
            vv = np.array([0.0, 0.0, 0.0])
            self.particle[i].set(self.teapot.lid, vv)
            self.particle[i].setRadius(0.2)
            self.particle[i].setGravity(np.array([0., -9.8, 0.]))
        #for i in range(self.nParticle) :
        #    l = np.array([myRand(-0.3,0.3),0.001, myRand(-0.3,0.3)])
        #    v = np.array([myRand(-self.particleVel,self.particleVel),myRand(6,7),myRand(-self.particleVel,self.particleVel)])
        #    self.particle[i].set(l,v)
        #    self.particle[i].setRadius(self.particleRadius)
        #    self.particle[i].setGravity(np.array([0., -9.8, 0.]))

        return



    def frame(self):
        global backCount, handState
        dt = self.getDt()
        #dt*=10

        super(mySim,self).frame()
        #self.teapot.colHandlePair(Hand)
        self.teapot.zeroBean(Hand)
        self.teapot.hand = handState
        self.teapot.draw(theta)
        if self.teapot.hand :
            self.teapot.rotateT(theta, self.teapot.axis)
            
        newCurTime = time.time()
        #print(newCurTime-self.curTime)
        # if newCurTime - self.curTime > random.random() / 1000.0:
        #     self.curTime = newCurTime
        #     self.particle.append(Particle.Particle())
        #     self.collisionCnt.append(0)
        #
        #     l = np.array([myRand(-0.1,0.1), 0.001, myRand(-0.1,0.1)])
        #     v = np.array([myRand(-self.particleVel, self.particleVel), myRand(8,9), myRand(-self.particleVel, self.particleVel)])
        #     self.particle[-1].set(l, v)
        #     self.particle[-1].setRadius(self.particleRadius)
        #     self.particle[-1].setGravity(np.array([0., -9.8, 0.]))


        #for idx , p in enumerate(self.particle):
        #    if idx <3 :break
        #    p.simulate(dt)
        #    if p.loc[1] < 0 :
        #        p.vel[1] = - p.vel[1] / 1.7
        #        self.collisionCnt[idx] = self.collisionCnt[idx] + 1
            #p.colHandle()
        #print(self.particle[0].vel)
        maxCollision = 4
        #self.particle = [ item for item,cnt in zip(self.particle,self.collisionCnt) if cnt < maxCollision ]
        #self.collisionCnt= [ cnt for cnt in self.collisionCnt if cnt < maxCollision]
        #(len(self.particle))
        #self.nParticle = len(self.particle)
        #for i in range(self.nParticle) :
        #    for j in range(i+1, self.nParticle) :
        #        self.particle[i].colHandlePair(self.particle[j])

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
                #vv = np.array([0.0 ,0.0, 0.0])
                vv = np.array([myRand(-2, 2), myRand(2,11), myRand(-2, 2)])
                p.loc = ll
                p.vel = vv

        for p in self.particle :
            p.cdraw([0.0,0.0,1.0,1.0])
        for p in self.steam :
            p.cdraw([1.0, 1.0, 1.0, 1.0])


        global upCnt,downCnt,leftCnt,rightCnt
        glPushMatrix()
        for i in range(upCnt):
            glTranslatef(0,1,0)
        for i in range(downCnt):
            glTranslatef(0,-1,0)
        for i in range(leftCnt):
            glTranslatef(0,0,-1)
        for i in range(rightCnt):
            glTranslatef(0,0,1)
        Hand.doAnimation(ani.KeyInputState)
        glPopMatrix()
        print(Hand.rootJoint.getCurAnimatedLocationCOG() , ' is COG of RottJoint')
        print(self.KeyInputState)
        # cubeOrder = ((0, 1, 2, 3), (1, 2, 6, 5), (2, 3, 7, 6), (0, 1, 5, 4), (0, 3, 2, 4), (4, 7, 6, 5))
        # vertices = makeCubeInfo(0,0,-2,5,2,2)
        # solidCube(vertices,cubeOrder)
        # glBegin(GL_QUADS)
        # for i in range(4):
        #     glVertex3f(vertices[i][0],vertices[i][1],vertices[i][2])
        # glEnd()
        super(mySim,self).afterFrame()

ani = mySim(500,500, b"Lab07-3:found")
ani.grid(False)
ani.timerStart()

def key(k, x, y) :
    global Hand,upCnt,downCnt,leftCnt, rightCnt, handState
    if k == b' ':
        ani.KeyInputState['space'] = True
    #    if ani.timer.timerRunning:
    #        ani.timerStop()
    #    else:
    #        ani.timerStart()
    else :
        ani.KeyInputState['space'] = False
    if k == b'r':
        ani.initObjects()
        ani.KeyInputState['reset'] = True
        upCnt = 0
        downCnt = 0
        rightCnt = 0
        leftCnt = 0
    else :
        ani.KeyInputState['reset'] = False
    if k == b'b':
        ani.KeyInputState['b'] = True
        print(Hand.rootJoint.children[0].localBindTransform, " is rootJoint.localBindTransform ")
        print(Hand.rootJoint.children[0].inverseBindTransform, " is rootJoint.inverseBindTransform ")
    else:
        ani.KeyInputState['b'] = False
    if k == b'v':
        ani.KeyInputState['v'] = True
    else:
        ani.KeyInputState['v'] = False
    if k == b'y':
        ani.KeyInputState['y'] = True
    else:
        ani.KeyInputState['y'] = False
    if k == b'g':
        ani.KeyInputState['g'] = True
    else:
        ani.KeyInputState['g'] = False
    if k == b'h':
        ani.KeyInputState['h'] = True
    else:
        ani.KeyInputState['h'] = False
    if k == b'n':
        ani.KeyInputState['n'] = True
    else:
        ani.KeyInputState['n'] = False
    if k == b'w':
        upCnt += 1
    if k==b'a':
        leftCnt += 1
    if k == b'd':
        rightCnt += 1
    if k == b's':
        downCnt += 1
    if k == b'z':
        handState = True
def draw():
    ani.frame()
ani.initObjects()
ani.start(draw,key)
# ani.initObjects()
# ani.timerStart()






