from transform import Transformation


class Vehicle:

    def __init__(self, x, y, angle=0.0, scale=1.0):
        self.pos   = [x, y]
        self.angle = angle
        self.speed = [0.0, -200.0]
        self.scale = scale
        self.width = 100 * self.scale
        self.sensors = [Sensor(self,  25, -165), 
                        Sensor(self, -25, -165)]

    def step(self, dt=0.01):
        v2, v1 = self.speed
        if v2 == v1:
            dangle, dy, dx = 0.0, - dt * v1, 0.0
        else:
            dangle = dt / self.width * (v2 - v1)
            R = self.width / 2 * (v1 + v2) / (v2 - v1)
            dy = -cos(dangle / 2) * 2 * R * sin(dangle / 2)
            dx = sin(dangle / 2) * 2 * R * sin(dangle / 2)

        self.angle += dangle
        dx, dy = (cos(self.angle) * dx - sin(self.angle) * dy,
                  sin(self.angle) * dx + cos(self.angle) * dy)

        self.pos[0] += dx
        self.pos[1] += dy
        
        # TODO: sensors

    def draw(self):
        pushMatrix()
        translate(*self.pos)
        rotate(self.angle)
        scale(self.scale)

        stroke(0)
        strokeWeight(1)
        noFill()
        rect(0, -70, 80, 160)
        rect(-50, 0, 20, 40, 6, 6, 6, 6)
        rect(50, 0, 20, 40, 6, 6, 6, 6)

        noFill()
        bezier(-40, 0, -20, 0, -25, -40, -25, -150)
        bezier(-40, 0, -20, 0, 25, -100, 25, -150)
        bezier(40, 0, 20, 0, 25, -40, 25, -150)
        bezier(40, 0, 20, 0, -25, -100, -25, -150)

        line(-25, -150, -25, -160)
        line(25, -150, 25, -160)

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

        # transformation matrix of the vehicle
        M = Transformation().translate(*self.vehicle.pos).rotate(-self.vehicle.angle)
        # adding sensor transformation
        scale = self.vehicle.scale
        M.translate(scale * self.tpos[0], scale * self.tpos[1]).rotate(self.tangle)
        pos = M.apply(0, 0)
        return pos[0], pos[1], self.vehicle.angle + self.tangle 
                
    def activation(self, light_sources):
        """Compute how much light the sensor is receiving."""
        act = 0.0
        x, y, angle = world_pos() 
                
        for light in light_sources:
            # compute the angle with the light 
            theta = atan2(light.pos[0] - x, light.pos[1] - y)
            diff_angle = abs((theta - angle) % (2*PI)/PI)        
            # compute the light output (linear decrease)
            d = dist(light.pos[0], light.pos[1], x, y)
            act += max((1.0 - diff_angle) * (400 - d)/400, 0)
        
        return act
    
    def draw(self):
        """Draws the sensor 
        
        Assumes the current coordinate matrix is the one of the vehicle.
        """
        pushMatrix()
        translate(*self.tpos)
        rotate(self.tangle)
        arc(0, 0, 10, 10, 0, PI)
        popMatrix()