import gc

add_library('controlP5')

from world import World
from vehicle import Vehicle
from interface import Interface


world   = World()
vehicle = Vehicle(400, 400, scale=0.75, )

def setup():
    global interface
    smooth(8)
    rectMode(CENTER)
    frameRate(30)
    size(800, 800, P2D)

    interface = Interface(ControlP5(this), lw=20.0)
    world.add_light('mouse', 200, 200, 5.0)    
    vehicle.speed = interface.lw, interface.rw
    
    
def draw():
    background(255)
    for _ in range(10):
        vehicle.step(world, 0.01)
    world.draw()
    vehicle.draw()
    
    stroke(0, 100)
    line(400, 0, 400, 800)
    line(0, 400, 800, 400)
    