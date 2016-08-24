class Vehicle:

    def __init__(self, x, y, angle=0.0, scale=1.0):
        self.pos   = [x, y]
        self.angle = angle
        self.speed = [0.0, 0.0]
        self.scale = scale
        self.width = 100 * self.scale
        self.sensors = [Sensor(self, 165,  25), 
                        Sensor(self, 165, -25)]

    def world_pos():
        return self.pos, self.angle

    def step(self, world, dt=0.01):
        v1, v2 = self.speed
        if v2 == v1:
            dangle, dy, dx = 0.0, 0.0, dt * v1
        else:
            dangle = dt / self.width * (v1 - v2)
            R = self.width / 2 * (v1 + v2) / (v2 - v1)
            dx = -cos(dangle / 2) * 2 * R * sin(dangle / 2)
            dy =  sin(dangle / 2) * 2 * R * sin(dangle / 2)

        self.angle += dangle
        dx, dy = (cos(self.angle) * dx - sin(self.angle) * dy,
                  sin(self.angle) * dx + cos(self.angle) * dy)

        self.pos[0] += dx
        self.pos[1] += dy
        
        for sensor in self.sensors:
            sensor.activation(world.lights.values())

#         # DEBUG: display where sensors think they are.
#         for sensor in self.sensors:
#             x, y, a = sensor.world_pos()
#             stroke(0)
#             rect(x, y, 5, 5)             

    def draw(self):
        pushMatrix()
        translate(*self.pos)
        rotate(self.angle)
        scale(self.scale)

        stroke(0)
        strokeWeight(1)
        noFill()
        rect(70, 0, 160, 80)
        rect(0, -50, 40, 20, 6, 6, 6, 6)
        rect(0,  50, 40, 20, 6, 6, 6, 6)

        noFill()
        bezier(0, -40, 0, -20,  40, -25, 150, -25)
        bezier(0, -40, 0, -20, 100,  25, 150,  25)
        bezier(0,  40, 0,  20,  40,  25, 150,  25)
        bezier(0,  40, 0,  20, 100, -25, 150, -25)

        line(150, -25, 160, -25)
        line(150,  25, 160,  25)

        for sensor in self.sensors:
            sensor.draw()

        popMatrix()


class Sensor:
    
    def __init__(self, vehicle, tx, ty, tangle=0.0):
        """Sensor instanciation
        
        :param  tx, ty:  position from the center of the vehicle
        :param  angle:   angle from the anteroposterior axis of the vehicle
                         (anterior direction is zero, posterior is PI or -PI)
        """
        self.vehicle = vehicle
        self.tpos    = tx, ty
        self.tangle  = tangle

    def world_pos(self):
        """Compute the absolute world position of the sensors"""
        pushMatrix()
        # transformation matrix of the vehicle
        translate(*self.vehicle.pos)
        rotate(self.vehicle.angle)
        # adding sensor transformation
        translate(0.75 * self.tpos[0], 0.75 * self.tpos[1])
        rotate(self.tangle)
        x, y = modelX(0, 0, 0), modelY(0, 0, 0)
        popMatrix()
                     
        fill(255, 0, 0)
        noStroke()
        return (x, y), self.vehicle.angle + self.tangle 
                
    def activation(self, light_sources):
        """Compute how much light the sensor is receiving."""
        self.act = 0.0
        pos, angle = self.world_pos() 
        x, y = pos
        arc(30, 30, 40, 40, 0, angle, PIE)
                
        for light in light_sources:
            # compute the angle with the light 
            theta = atan2(light.pos[1] - y, light.pos[0] - x)
            arc(30, 90, 40, 40, 0, theta % (2*PI), PIE)

            diff_angle = abs(((theta % TWO_PI) - (angle % TWO_PI)))  
            diff_angle = min(diff_angle, TWO_PI - diff_angle)
            arc(30, 150, 40, 40, 0, diff_angle, PIE)
            # compute the light output (linear decrease)
            d = dist(light.pos[0], light.pos[1], x, y)
            self.act += max((1.0 - diff_angle/PI) * (400 - d/light.intensity)/400, 0)
        
        return self.act
    
    def draw(self):
        """Draws the sensor 
        
        Assumes the current coordinate matrix is the one of the vehicle.
        """
        pushMatrix()
        translate(*self.tpos)
        rotate(self.tangle)
        fill(255, 0, 0, 255*self.act)
        stroke(0)
        arc(0, 0, 10, 10, HALF_PI, 3*HALF_PI)
        popMatrix()
        
        
class Link:
    
    def __init__(self, pre, post, w0):
        self.pre  = pre
        self.post = post
        self.w    = w0
        
    def step(self):
        """Transmit activation from pre to post"""
        self.post.receive(self.w * self.pre.act)
        
    def draw(self):
        x1, y1 = self.pre.pos
        x2, y2 = self.post.pos 
        bezier(x1, y1, 0, -20,  40, -25, x2, y2)
        
class Plug:
    """A small positional object to connect stuff aesthetically"""
    
    def __init__(self):
        pass