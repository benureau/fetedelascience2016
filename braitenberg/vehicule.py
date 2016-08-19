

class Vehicule:
    
    def __init__(self, x, y, angle=0.0):
        self.pos = x, y
        self.angle = angle
        
    def draw(self):
        pushMatrix()
        translate(self.pos[0], self.pos[1])
        rotate(self.angle)
        
        stroke(0)
        strokeWeight(1)
        #strokeJoin(ROUND)
        fill(255)
        rect(0, 0, 80, 160) 
        rect(-50, 70, 20, 40, 6, 6, 6, 6) 
        rect( 50, 70, 20, 40, 6, 6, 6, 6)
        
        noFill()
        bezier(-40, 70, -20, 70, -25, -40, -25, -80)
        bezier(-40, 70, -20, 70,  25,  20,  25, -80)
        bezier( 40, 70,  20, 70,  25, -40,  25, -80)
        bezier( 40, 70,  20, 70, -25,  20, -25, -80)

        line(-25, -80, -25, -90)
        line( 25, -80,  25, -90)

        arc( 25, -95, 10, 10, 0, PI);
        arc(-25, -95, 10, 10, 0, PI);

        popMatrix()