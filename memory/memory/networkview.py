from tileview import COLORMAP

class NetworkView:
    
    def __init__(self, tileview, screenpos, tilesize=30):
        self.tv = tileview
        self.tilesize = tilesize
        self.pos = screenpos
        
    def draw(self):
        textSize(14)

        w = self.tv.w * len(self.tv.colornames) 
        h = self.tv.h * len(self.tv.shapenames) 
        a = self.tilesize
        
        pushMatrix()
        translate(*self.pos)
        
        w_tile = len(self.tv.colornames)
        h_tile = len(self.tv.shapenames)

        noStroke()
        fill(230)
        for j_t in range(self.tv.w):
            for i_t in range(self.tv.h):
                rect((j_t * w_tile + 0.7) * a, (i_t * h_tile + 0.7) * a, 
                     a * (w_tile - 0.4), a * (h_tile - 0.4))
                     
                                                                                                                                    
        strokeWeight(1)
        for i in range(w):
            stroke(100)
            line((i + 1) * a,         0.0,
                 (i + 1) * a, (h + 1) * a)
            noStroke()
            fill(255)
            ellipse((i + 1) * a, (h + 1.1) * a, 35, 35)
            fill(100)
            text("0", (i + 1) * a, (h + 1.1) * a)

        
        for j in range(h):
            stroke(100)
            line(        0.0, (j + 1) * a,
                 (w + 1) * a, (j + 1) * a)
            noStroke()
            fill(255)
            ellipse((w + 1.1) * a, (j + 1.15) * a, 35, 35)
            fill(100)
            text("0", (w + 1.1) * a, (j + 1.15) * a)
    


        stroke(200)
        strokeWeight(2)
        fill(255)
        for j in range(h):
            shapename = self.tv.shapenames[j % len(self.tv.shapenames)]
            if shapename == 'triangle':
                triangle(0.0, (j + 0.75) * a,
                         -0.25 * a, (j + 1.25) * a,
                         +0.25 * a, (j + 1.25) * a)
            elif shapename == 'square':
                rect(-0.25 * a, (j + 0.75) * a, 0.5 * a, 0.5 * a) 

        noStroke()
        for i in range(w):
            colorname = self.tv.colornames[i % len(self.tv.colornames)]
            fill(*COLORMAP[colorname])
            ellipse((i + 1) * a, 0.0, 0.6 * a, 0.6 * a)
            
        noStroke()
        fill(100)
        textSize(14)
    
        for tilecoo, tile in self.tv.tiles.items():
            i = h_tile * tilecoo[1] + self.tv.shapenames.index(tile.shapename) 
            j = w_tile * tilecoo[0] + self.tv.colornames.index(tile.colorname) 
            ellipse((j+1) * a, (i+1) * a, 7, 7)

            fill(255)
            ellipse((j+1) * a, (h + 1.1) * a, 35, 35)
            fill(100)
            text("1", (j+1) * a, (h + 1.1) * a)

            fill(255)
            ellipse((w+1.1) * a, (i + 1.15) * a, 35, 35)
            fill(100)
            text("1", (w+1.1) * a, (i + 1.15) * a)
                        
        popMatrix()