
class World:

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.center = w/2, h/2
        self.lights = {}

    def add_light(self, name, x, y, intensity):
        self.lights[name] = Light(x, y, intensity=intensity)

    def del_light(self, name):
        del self.light[name]


    def draw(self):
        stroke(0, 100)
        res = 400
        x_c, y_c = self.center
        x_0 = int(x_c) - (int(x_c) % res) 
        y_0 = int(y_c) - (int(y_c) % res) 
            
        for i in range(-2, 3):
            line(x_0 + i*res, y_c - height, x_0 + i*res, y_c + height)
        for j in range(-2, 3):
            line(x_c - width, y_0 + j*res, x_c + width, y_0 + j*res)
        
        for light in self.lights.values():
            light.draw()

    def recenter(self, vehicle):
        """If the vehicle is too close of an edge, change the world's 
        screen offset, to translate the view of world. 
        """
        buffer = 200
        x_c, y_c = self.center
        print(vehicle.x, vehicle.y)
        if vehicle.x - (x_c - self.w/2) < buffer:
            self.center = vehicle.x - buffer + self.w/2, y_c
        if (x_c + self.w/2) - vehicle.x  < buffer:
            self.center = vehicle.x + buffer - self.w/2, y_c
        if vehicle.y - (y_c - self.h/2)  < buffer:
            self.center = self.center[0], vehicle.y - buffer + self.h/2
        if (y_c + self.h/2) - vehicle.y  < buffer:
            self.center = self.center[0], vehicle.y + buffer - self.h/2

class Light:

    def __init__(self, x, y, intensity=1.0):
        """Light with position x,y and a given intensity."""
        self.x, self.y = x, y
        self.intensity = intensity  # a negative weight is repulsive.

    def draw(self):
        noStroke()
        fill(255, 215, 0, min(255, 20*self.intensity))
        ellipse(self.x, self.y, 20.0, 20.0)