
class World:
    
    def __init__(self):
        self.lights = {}
        
    def add_light(self, name, x, y, intensity):
        self.lights[name] = Light(x, y, intensity=intensity)
    
    def del_light(self, name):
        del self.light[name]
        
        
    def draw(self):
        for light in self.lights.values():
            light.draw()
            
    
class Light:
    
    def __init__(self, x, y, intensity=1.0):
        """Light with position x,y and a given intensity."""
        self.pos = x, y
        self.intensity = intensity  # a negative weight is repulsive.
        
    def draw(self):
        noStroke()
        fill(255, 215, 0, min(255, 20*self.intensity))
        ellipse(self.pos[0], self.pos[1], 20.0, 20.0)