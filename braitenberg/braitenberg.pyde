add_library('controlP5')

from vehicle import Vehicle
from interface import Interface

vehicle = Vehicle(400, 400, scale=0.75, )


def setup():
    global interface
    smooth(8)
    rectMode(CENTER)
    frameRate(30)
    size(800, 800)
    interface = Interface(ControlP5(this), lw=20.0)
    
    
def draw():
    background(255)
    vehicle.speed = interface.lw, interface.rw
    for _ in range(100):
        vehicle.step(0.001)
    vehicle.draw()
    
    stroke(0, 100)
    line(400, 0, 400, 800)
    line(0, 400, 800, 400)