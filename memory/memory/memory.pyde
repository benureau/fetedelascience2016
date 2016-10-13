from tileview import TileArray, TileObject
from networkview import NetworkView

ta = TileArray(4, 3, ['triangle', 'square'], ['blue', 'red'],
               screenpos=(100, 100), tilesize=50)
ta.add_object(TileObject('triangle', 'red'), (0, 1))
ta.add_object(TileObject('square', 'blue'), (2, 0))

nv = NetworkView(ta, (100, 300), 40)


def setup():
    size(800, 800)
    background(255)

        
def draw():
    ta.draw()
    nv.draw()
    
