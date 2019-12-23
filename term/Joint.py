import numpy as np
'''
@Author : 김영빈
@description : 관절에 대해 정의
'''

class Joint:
    def __init__(self,index , name, localBindTransform,originLocation ):
        self.index = index
        self.name =name
        self.localBindTransform = np.array(localBindTransform)
        #self.localBindTransform = localBindTransform
        self.children =[]
        self.animatedTransform  =  localBindTransform # 얘는 형식이뭐지
        self.inverseBindTransform = localBindTransform
        self.originLocation =originLocation
        self.localChangeTransform = np.identity(4)
    def addChild(self,child):
        self.children.append(child)
    def getAnimatedTransform(self):
        return self.animatedTransform
    def setAnimatedTransform(self,animationTransform):
        self.animatedTransform = animationTransform
    def setLocalBindTransform(self,localBindTransform):
        self.localBindTransform = localBindTransform
    def getInverseLocalBindTransform(self):
        return self.inverseBindTransform
    def calcInverseBindTransform(self,parentBindTransform):
        bindTransform = np.matmul(parentBindTransform,self.localBindTransform)
        self.inverseBindTransform = self.getInverseMatrix(bindTransform)
        for child in self.children:
            child.calcInverseBindTransform(bindTransform)
    def getInverseMatrix(self,source):
        try:
            inverse = np.linalg.inv(source)
        except np.linalg.LinAlgError:
            return None
        else:
            return inverse
    def initialLocalChangeTransform(self,joint):
        print("이거 사불러진다")
        joint.localChangeTransform = np.identity(4)
        for child in joint.children:
            self.initialLocalChangeTransform(child)
    def isTouched(self,joint , teapot):
        #calc dist
        Touched = joint.calcTouched(teapot)
        if len(joint.children) == 0 :
            return Touched
        for child in joint.children:
            Touched += joint.isTouched(child , teapot)
        return Touched
    def calcTouched(self,teapot): # return 1 when touched
        curJointLoc = self.getCurAnimatedLocationCOG()
        return 1 if np.sum( (teapot.loc-curJointLoc) **2) < 101.10 else 0
    def getCurAnimatedLocation  (self): # COG : Center of Gravity 무게중심
        resultLocation = np.array([np.dot(self.getAnimatedTransform(), item) for item in self.originLocation])
        return resultLocation

    def getCurAnimatedLocationCOG(self):  # COG : Center of Gravity 무게중심
        loc = self.getCurAnimatedLocation()[:,:3] # 좌표정보만 갖고와서
        return np.mean(loc ,axis = 0 )
