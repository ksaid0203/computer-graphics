from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import random
import math
import numpy as np
#import Animator
import Particle
'''
@Author : 김영빈
@description : 손에 대해 정의
'''

class Hand(Particle.Particle):
    def __init__(self, rootJoint ):
        self.rootJoint = rootJoint # type Joint
        #self.animator = Animator.Animator(self) #type Animator
        self.cubeOrder = ((0,1,2,3),(1,2,6,5),(2,3,7,6),(0,1,5,4),(0,3,2,4),(4,7,6,5))
        rootJoint.calcInverseBindTransform(np.identity(4))
    def doAnimation(self,keyboardState):
        currentPose = self.calculateCurrentAnimationPose(keyboardState)
        self.applyPoseToJoints(currentPose,self.rootJoint,np.identity(4))
        self.drawNonAnimation(self.rootJoint)
    def drawNonAnimation(self,rootJoint):

         result = np.array([np.dot(rootJoint.getAnimatedTransform() ,item) for item in rootJoint.originLocation])
         self.drawJoint(result)
         for child in rootJoint.children:
             self.drawNonAnimation(child)

    def calculateCurrentAnimationPose(self,keyboardState):
        currentPose= {"space" : np.identity(4),"b":np.identity(4) , "g":np.identity(4),"y":np.identity(4),
                      "h":np.identity(4),"n":np.identity(4)}
        currentTheta= {"space" : 0,"b":0 , "g":0,"y":0,
                      "h":0,"n":0}
        if keyboardState['reset'] == True:
            currentTheta['space'] = 0;currentTheta['b'] = 0; currentTheta['g'] = 0;currentTheta['y'] = 0;currentTheta['h'] = 0;currentTheta['n'] = 0
            self.rootJoint.initialLocalChangeTransform(self.rootJoint)
        for key in keyboardState:
            if key == 'reset' : continue
            if keyboardState[key] == True:
                currentTheta[key] -= 0.01
                currentPose[key] = self.rotationfMatrix(currentTheta[key])
                keyboardState[key] = False
        return currentPose
    def rotationfMatrix(self,theta):
        return np.array([ [math.cos(theta), -math.sin(theta),0,0],
                          [math.sin(theta),math.cos(theta),0,0]
                           ,[0,0,1,0]
                           ,[0,0,0,1]  ])
    def applyPoseToJoints(self,currentPose , joint , parentAnimationTransform):
        if currentPose.get(joint.name) is None :
            return
        changeLocalTransform  = currentPose.get(joint.name) #바꾸고싶은 회전연산을 갖고와서
        joint.localChangeTransform = np.dot(changeLocalTransform , joint.localChangeTransform ) # 현재 joint에다가 발라주고
        movetoparentTransform  =  np.dot(joint.localBindTransform , joint.localChangeTransform) #  M(i,p) * M(i,l)
        animationTransform = np.dot(parentAnimationTransform , movetoparentTransform)
        for childJoint in joint.children:
            self.applyPoseToJoints(currentPose , childJoint , animationTransform)
        resultNaimationTransform = np.dot(animationTransform, joint.getInverseLocalBindTransform())
        joint.setAnimatedTransform(resultNaimationTransform)
    def addJointsToArray (self,headJoint,  jointMatrices) :
        jointMatrices[headJoint.index] = headJoint.getAnimatedTransform()
        for childJoint in headJoint.children:
             self.addJointsToArray(childJoint, jointMatrices)
    #def update(self):
    #     self.animator.update()
    def getJointTransforms(self):
        return self.rootJoint
    def drawJoint(self,resutLocation):
        self.solidCube(resutLocation)
    def solidCube(self,cubeVertices):
         glBegin(GL_QUADS)
         for cubeQuad in self.cubeOrder :
             for idx , cubeVertex in enumerate(cubeQuad):
                 if idx > 2 : pass
                 glVertex3fv(cubeVertices[cubeVertex] [:3])
         glEnd()
    def isTouched(self , teaPot):
        isTouched = self.rootJoint.calcTouched(teaPot)
        return isTouched


