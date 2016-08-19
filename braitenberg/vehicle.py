

class Vehicle:
    
    
    def __init__(self, x, y, angle=0.0, scale=1.0):
        self.pos = [x, y]
        self.angle = angle
        self.speed = [0.0, -200.0]
        self.scale  = scale
        self.width = 100 * self.scale
        
        
    def step(self, dt=0.01):
        v2, v1 = self.speed
        if v2 == v1:
            dangle, dy, dx = 0.0, - dt * v1, 0.0
        else:
            dangle = dt / self.width * (v2 - v1)
            R = self.width/2 * (v1 + v2)/(v2 - v1)
            dy = -cos(dangle/2) * 2 * R * sin(dangle/2)
            dx =  sin(dangle/2) * 2 * R * sin(dangle/2)
        
        self.angle  += dangle
        dx, dy = (cos(self.angle) * dx - sin(self.angle) * dy,
                  sin(self.angle) * dx + cos(self.angle) * dy)

        self.pos[0] += dx
        self.pos[1] += dy
                    
                    
    def draw(self):
        pushMatrix()
        translate(self.pos[0], self.pos[1])
        #rect(0, 0, 5, 5)
        rotate(self.angle)
        scale(self.scale)
        
        stroke(0)
        strokeWeight(1)
        noFill()
        rect( 0, -70, 80, 160) 
        rect(-50,  0, 20, 40, 6, 6, 6, 6) 
        rect( 50,  0, 20, 40, 6, 6, 6, 6)
        
        noFill()
        bezier(-40,  0, -20,  0, -25,  -40, -25, -150)
        bezier(-40,  0, -20,  0,  25, -100,  25, -150)
        bezier( 40,  0,  20,  0,  25,  -40,  25, -150)
        bezier( 40,  0,  20,  0, -25, -100, -25, -150)

        line(-25, -150, -25, -160)
        line( 25, -150,  25, -160)

        arc( 25, -165, 10, 10, 0, PI);
        arc(-25, -165, 10, 10, 0, PI);

        popMatrix()