add_library('controlP5')

from world import World
from vehicle import Vehicle
from interface import Interface

SIDEBAR_WIDTH = 300

def setup():
    global interface, world, vehicle
    smooth(8)
    rectMode(CENTER)
    frameRate(30)
    
#    size(1100, 800, P2D)
    fullScreen(P2D)

    world   = World(width - SIDEBAR_WIDTH, height)
    vehicle = Vehicle(400, 400, w=80, h=120, sizescale=0.85)


    myfont = createFont("DINNextRoundedLTPro-Regular", 16) 
    #loadFont("DINNextRoundedLTPro-Regular-16.vlw")
    interface = Interface(ControlP5(this), vehicle, font=myfont, sidebar=SIDEBAR_WIDTH)
    world.add_light('mouse', 200, 200, 100.0)
    #vehicle.speed = interface.lw, interface.rw


def draw():

    background(255)
    
    
    world.lights['mouse'].x = min(mouseX, width - SIDEBAR_WIDTH) + world.center[0] + SIDEBAR_WIDTH/2 - width/2
    world.lights['mouse'].y = mouseY + world.center[1] - height/2

    for _ in range(10):
        vehicle.step(world, 0.01)
        #vehicle.speed = interface.lw, interface.rw

    world.recenter(vehicle)
    
    pushMatrix()
    translate(width/2 - world.center[0] - SIDEBAR_WIDTH/2, height/2 - world.center[1])
    world.draw()
    vehicle.draw()
    popMatrix()
    
    interface.update_sliders()
    interface.draw()
    #noLoop()