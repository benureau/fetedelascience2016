from tileview import TileArray, TileObject
from networkview import NetworkView

ta = TileArray(4, 3, ['triangle', 'square'], ['blue', 'red'],
               screenpos=(240, 150), tilesize=80)
ta.add_object(TileObject('triangle', 'red'), (0, 1))
ta.add_object(TileObject('square', 'blue'), (2, 0))

nv = NetworkView(ta, (220, 450), 40)


def setup():
    size(800, 800)
    textAlign(CENTER);
    smooth()
    background(255)

        
def draw():
    fill(50)
    textSize(40)
    text("Memory Game", width/2, 100)
    ta.draw()
    nv.draw()
    
