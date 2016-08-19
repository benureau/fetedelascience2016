
from vehicule import Vehicule

vehicule = Vehicule(400, 400, scale=0.5)

def setup():
    smooth(8)
    rectMode(CENTER)
    frameRate(30)
    size(800, 800)
    
    
def draw():
    background(255)
    for _ in range(1000):
        vehicule.step(0.00001)
    vehicule.draw()
    stroke(0, 100)
    line(400, 0, 400, 800)
    line(0, 400, 800, 400)
