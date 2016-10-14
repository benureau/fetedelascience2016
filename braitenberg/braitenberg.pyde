add_library('controlP5')

from world import World
from vehicle import Vehicle
from interface import Interface


world   = World()
vehicle = Vehicle(400, 400, w=50, h=80, sizescale=0.65)

def setup():
    global interface
    smooth(8)
    rectMode(CENTER)
    frameRate(30)
    size(800, 800, P2D)

    interface = Interface(ControlP5(this), lw=10.0)
    world.add_light('mouse', 200, 200, 100.0)
    #vehicle.speed = interface.lw, interface.rw


def draw():
    scale(1.0)
    background(255)
    world.lights['mouse'].x = mouseX
    world.lights['mouse'].y = mouseY

    for _ in range(10):
        vehicle.step(world, 0.01)
        #vehicle.speed = interface.lw, interface.rw
    world.draw()
    vehicle.draw()

    stroke(0, 100)
    line(400, 0, 400, 800)
    line(0, 400, 800, 400)