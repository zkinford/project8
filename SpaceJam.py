from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import *
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from CollideObjectBase import PlacedObject
from CollideObjectBase import *
from CollideObjectBase import SphereCollideObj
from direct.interval.IntervalGlobal import Sequence

import DefensePaths as defensePaths
import SpaceJamClasses as spaceJamClasses
import math
import CollideObjectBase as collideObjectBase

class SpaceJam(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # It's very important to get rid of code bloat as much as possible. We got rid of many lines in this script just by using classes.
        self.Universe = spaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render, 'Universe', "Assets/Universe/Universe.jpg", (0, 0, 0), 10000)
        self.Planet1 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet1', "./Assets/Planets/Planet1.jpg", (-6000, -3000, -800), 250)
        self.Planet2 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet2', "./Assets/Planets/Planet2.jpg", (0, 6000, 0), 300)
        self.Planet3 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet3', "./Assets/Planets/Planet3.jpg", (500, -5000, 200), 500)
        self.Planet4 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet4', "./Assets/Planets/Planet4.jpg", (300, 6000, 500), 150)
        self.Planet5 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet5', "./Assets/Planets/Planet5.jpg", (700, -2000, 100), 500)
        self.Planet6 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet6', "./Assets/Planets/Planet6.jpg", (0, -900, -1400), 700)
        self.SpaceStation1 = spaceJamClasses.SpaceStation(self.loader, "./Assets/Space Station/spaceStation.egg", self.render, 'Space Station', "./Assets/Space Station/SpaceStation1_Dif2.png", (1500, 1000, -100), 40)
        self.Hero = spaceJamClasses.Spaceship(self.loader, "./Assets/Dumbledore/Dumbledore.egg", self.render,'Hero', "./Assets/Dumbledore/spacejet_C.png", (0, 0, 0), 50, self.taskMgr, self.render, self.accept)

        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.Hero.collisionNode, self.Hero.modelNode)
        self.cTrav.addCollider(self.Hero.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.render)

        self.SetCamera()

        fullCycle = 60

        for j in range(fullCycle):
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.SpaceStation1, nickName, j, fullCycle, 2)
            
        self.DrawCircleXYDefense()
        self.DrawCircleXZDefense()
        self.DrawCircleYZDefense()

    def DrawCircleXYDefense(self):
        self.parent = self.loader.loadModel('./Assets/DroneDefender/DroneDefender.obj')
        self.parent.setScale(0.25)
        a = 0.0
        aInc = 0.2
        R = 50.0

        for i in range(30):
            posVec = (R * math.cos(a), R * math.sin(a), 0)
            self.placeholder = self.render.attachNewNode("Placeholder")
            self.placeholder.setPos(posVec)
            self.placeholder.setColor(255, 0, 0, 1)
            self.parent.instanceTo(self.placeholder)
            a += aInc

    def DrawCircleXZDefense(self):
        self.parent = self.loader.loadModel('./Assets/DroneDefender/DroneDefender.obj')
        self.parent.setScale(0.25)
        a = 0.0
        aInc = 0.2
        R = 50.0

        for i in range(30):
            posVec = (R * math.cos(a), 0, R * math.sin(a))
            self.placeholder = self.render.attachNewNode("Placeholder")
            self.placeholder.setPos(posVec)
            self.placeholder.setColor(0, 255, 0, 1)
            self.parent.instanceTo(self.placeholder)
            a += aInc

    def DrawCircleYZDefense(self):
        self.parent = self.loader.loadModel('./Assets/DroneDefender/DroneDefender.obj')
        self.parent.setScale(0.25)
        a = 0.0
        aInc = 0.2
        R = 50.0

        for i in range(30):
            posVec = (0, R * math.cos(a), R * math.sin(a))
            self.placeholder = self.render.attachNewNode("Placeholder")
            self.placeholder.setPos(posVec)
            self.placeholder.setColor(0, 0, 255, 1)
            self.parent.instanceTo(self.placeholder)
            a += aInc 
             
    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
            unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
            unitVec.normalize()
            position = unitVec * radius * 250 + centralObject.modelNode.getPos()
            spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 10)

    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Hero.modelNode)
        self.camera.setFluidPos(0, 1, 0)

class Orbiter():
    self.Sentinal1 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, self.rootAssetFolder + "/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, self.rootAssetFolder + "/DroneDefender/octotoad1_auv.png", self.Planet5, 900, "MLB", self.Hero)
    self.Sentinal2 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, self.rootAssetFolder + "/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, self.rootAssetFolder + "/DroneDefender/octotoad1_auv.png", self.Planet2, 500, "Cloud", self.Hero)

class Wanderer(SphereCollideObject):
    numWanderers = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, modelName: str, scaleVec: Vec3, texPath: str, staringAt: Vec3):
        super(Wanderer, self).__init__(loader, modelPath, parentNode, modelName, Vec3(0, 0, 0), 3.2)

        self.modelNode.setScale(scaleVec)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.staringAt = staringAt
        Wanderer.numWanderers += 1

        posInterval0 = self.modelNode.posInterval(20, Vec3(300, 6000, 500), startPos = Vec3(0, 0, 0))
        posInterval1 = self.modelNode.posInterval(20, Vec3(700, -2000, 100), startPos = Vec3(300, 6000, 500))
        posInterval2 = self.modelNode.posInterval(20, Vec3(0, -900, -1400), startPos = Vec3(700, -2000, 100))

        self.travelRoute = Sequence(posInterval0, posInterval1, posInterval2, name = "Traveler")

        self.travelRoute.loop()

        self.Wanderer1 = spaceJamClasses.Wanderer(self.loader, self.rootAssetFolder + "/DroneDefender.obj", self.render, "Drone", 6.0, self.rootAssetFolder + "/DroneDefender/octotoad1_auv.png", self.Hero)
app = SpaceJam()
app.run()