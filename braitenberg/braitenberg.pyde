
from vehicle import Vehicle

vehicle = Vehicle(400, 400, scale=0.75)

def setup():
    smooth(8)
    rectMode(CENTER)
    frameRate(30)
    size(800, 800)
    
    
def draw():
    background(255)
    for _ in range(1000):
        vehicle.step(0.00001)
    vehicle.draw()
    
    stroke(0, 100)
    line(400, 0, 400, 800)
    line(0, 400, 800, 400)
