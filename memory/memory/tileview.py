COLORMAP   = {'blue': (0, 0, 255), 'red': (255, 0, 0)}

class TileObject:
    
    def __init__(self, shapename, colorname):
        """
        :param shapename:  type of shape (triangle, square)
        :param colorname:  type of color (blue, red)
        """
        self.shapename = shapename
        self.colorname = colorname
        
    def draw(self, tilesize=50):
        fill(*COLORMAP[self.colorname])
        noStroke()
        a, b = tilesize, 0.5*tilesize
        if self.shapename == 'triangle':
            triangle(a/2, (a - b)/2, (a - b)/2, (a + b)/2, (a + b)/2, (a + b)/2)
        elif self.shapename == 'square':
            rect((a - b)/2, (a - b)/2, b, b)

class TileArray:
    
    def __init__(self, w, h, shapenames, colornames, 
                       screenpos=(0, 0), tilesize=30):
        self.w, self.h = w, h
        self.shapenames = shapenames
        for colorname in colornames:
            assert colorname in COLORMAP
        self.colornames = colornames
        self.tiles = {} # [[None for j in range(h)] for i in range(w)]
        self.screenpos = screenpos
        self.tilesize = tilesize
        
    def add_object(self, tile, pos):
        """Add an object to the tile array"""
        assert 0 <= pos[0] < self.w and 0 <= pos[1] < self.h
        assert tile.shapename in self.shapenames
        assert tile.colorname in self.colornames
        pos = tuple(pos)
        assert pos not in self.tiles
        self.tiles[pos] = tile
        
    def draw(self):
        x_0, y_0 = self.screenpos
        pushMatrix()
        translate(x_0, y_0)
        for i in range(self.w):
            for j in range(self.h):
                pushMatrix()
                translate(i * self.tilesize, j * self.tilesize)
                noFill()
                stroke(200)
                strokeWeight(2)
                rect(3, 3, self.tilesize - 6, self.tilesize - 6)
                if (i, j) in self.tiles:
                    self.tiles[(i, j)].draw(self.tilesize)
                popMatrix()
        popMatrix()