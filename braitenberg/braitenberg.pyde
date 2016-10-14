add_library('controlP5')

from world import World
from vehicle import Vehicle
from interface import Interface

w, h = 800, 800
world   = World(w, h)
vehicle = Vehicle(400, 400, w=80, h=120, sizescale=0.85)

def setup():
    global interface
    smooth(8)
    rectMode(CENTER)
    frameRate(30)
    size(w, h, P2D)

    myfont = createFont("DINNextRoundedLTPro-Regular", 16) 
    #loadFont("DINNextRoundedLTPro-Regular-16.vlw")
    interface = Interface(ControlP5(this), vehicle, font=myfont)
    world.add_light('mouse', 200, 200, 100.0)
    #vehicle.speed = interface.lw, interface.rw


def draw():

    background(255)
    
    
    world.lights['mouse'].x = mouseX + world.center[0] - width/2
    world.lights['mouse'].y = mouseY + world.center[1] - height/2

    for _ in range(10):
        vehicle.step(world, 0.01)
        #vehicle.speed = interface.lw, interface.rw

    world.recenter(vehicle)
    
    pushMatrix()
    translate(width/2 - world.center[0], height/2 - world.center[1])
    world.draw()
    vehicle.draw()
    popMatrix()
    
    interface.update_sliders()
    interface.draw()
    #noLoop()