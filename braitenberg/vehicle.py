from links import Link, Plug


class Vehicle:

    def __init__(self, x, y, angle=0.0):
        self.x     = x
        self.y     = y
        self.angle = angle
        self.width = 100
        self.sensors = [Sensor(self, 165,  25), 
                        Sensor(self, 165, -25)]
        self.left_wheel  = Wheel(self, 0, -50, side='left')
        self.right_wheel = Wheel(self, 0,  50, side='right')
        self.links   = [Link(self.sensors[0].plug, self.left_wheel.plug),
                        Link(self.sensors[0].plug, self.right_wheel.plug),
                        Link(self.sensors[1].plug, self.left_wheel.plug),
                        Link(self.sensors[1].plug, self.right_wheel.plug),]

    @property
    def wheel_speeds(self):
        return self.left_wheel.speed, self.right_wheel.speed

    @wheel_speeds.setter
    def wheel_speeds(self):
        lw, rw = speeds
        self.left_wheel.speed, self.right_wheel.speed = lw, rw

    def world_pos(self):
        return self.x, self.y, self.angle

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

        self.x += dx
        self.y += dy
        
        for sensor in self.sensors:
            sensor.activation(world.lights.values())

#         # DEBUG: display where sensors think they are.
#         for sensor in self.sensors:
#             x, y, a = sensor.world_pos()
#             stroke(0)
#             rect(x, y, 5, 5)             

    def draw(self):
        pushMatrix()
        translate(self.x, self.y)
        rotate(self.angle)
        
        stroke(0)
        strokeWeight(1)
        noFill()
        rect(70, 0, 160, 80)
        
        self.left_wheel.draw()
        self.right_wheel.draw()
        
        noFill()
        #bezier(0, -40, 0, -20,  40, -25, 150, -25)
        #bezier(0, -40, 0, -20, 100,  25, 150,  25)
        #bezier(0,  40, 0,  20,  40,  25, 150,  25)
        #bezier(0,  40, 0,  20, 100, -25, 150, -25)

        for sensor in self.sensors:
            sensor.draw()

        popMatrix()

        for link in self.links:
            link.draw()



class Wheel:

    def __init__(self, parent, x, y, side, size=(40, 20), speed=0.0):
        self.parent = parent
        self.x, self.y = x, y  # relative to the vehicule
        assert side in ('left', 'right')
        self.side = side
        self.size = size
        self.speed = speed

        plug_y = self.size[1]/2 if side == 'left' else -self.size[1]/2
        plug_a = HALF_PI        if side == 'left' else -HALF_PI
        self.plug = Plug(self, 0, plug_y, angle=plug_a, bend=20)

    def world_pos(self):
        px, py, pangle = self.parent.world_pos()
        dx, dy = ( self.x * cos(-pangle) + self.y * sin(-pangle), 
                  -self.x * sin(-pangle) + self.y * cos(-pangle))
        return px + dx, py + dy, pangle

    def draw(self):
        """Draw a wheel. Assumes vehicule coordinates"""
        stroke(0)
        noFill()
        rect(self.x, self.y, self.size[0], self.size[1], 6, 6, 6, 6)



class Sensor:
    
    def __init__(self, vehicle, x, y, angle=0.0):
        """Sensor instanciation
        
        :param  tx, ty:  position from the center of the vehicle
        :param  angle:   angle from the anteroposterior axis of the vehicle
                         (anterior direction is zero, posterior is PI or -PI)
        """
        self.vehicle   = vehicle
        self.x, self.y = x, y
        self.angle     = angle
        self.plug      = Plug(self, -5, 0, angle=PI, bend=40)

    def world_pos(self):
        """Compute the absolute world position of the sensors"""
        pushMatrix()
        resetMatrix()
        # transformation matrix of the vehicle
        translate(self.vehicle.x, self.vehicle.y)
        rotate(self.vehicle.angle)
        # adding sensor transformation
        translate(self.x, self.y)
        rotate(self.angle)
        x, y = modelX(0, 0, 0), modelY(0, 0, 0)
        popMatrix()
                     
        return x, y, self.vehicle.angle + self.angle 
                
    def activation(self, light_sources):
        """Compute how much light the sensor is receiving."""
        self.act = 0.0
        x, y, angle = self.world_pos()
        # arc(30, 30, 40, 40, 0, angle, PIE)
                
        for light in light_sources:
            # compute the angle with the light 
            theta = atan2(light.y - y, light.x - x)
            # arc(30, 90, 40, 40, 0, theta % (2*PI), PIE)

            diff_angle = abs(((theta % TWO_PI) - (angle % TWO_PI)))  
            diff_angle = min(diff_angle, TWO_PI - diff_angle)
            # arc(30, 150, 40, 40, 0, diff_angle, PIE)
            # compute the light output (linear decrease)
            d = dist(light.x, light.y, x, y)
            self.act += max((1.0 - diff_angle/PI) * (400 - d/light.intensity)/400, 0)
        
        return self.act
    
    def draw(self):
        """Draws the sensor. Assumes vehicule coordinates."""
        pushMatrix()
        translate(self.x, self.y)
        rotate(self.angle)
        fill(255, 0, 0, 255*self.act)
        stroke(0)
        arc(0, 0, 10, 10, HALF_PI, 3*HALF_PI)
        popMatrix()
        
        
