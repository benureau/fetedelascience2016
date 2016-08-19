
from vehicule import Vehicule

vehicule = Vehicule(400, 400)

def setup():
    smooth(8)
    rectMode(CENTER)
    frameRate(30)
    size(800, 800)
    
    
def draw():
    background(255)
    vehicule.draw()