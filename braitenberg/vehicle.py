from links import Link, Plug


class Vehicle:

    def __init__(self, x, y, angle=0.0, w=100, h=160, sizescale=1.0):
        self.x     = x
        self.y     = y
        self.angle = angle
        self.w, self.h, self.sizescale = w, h, sizescale
        self.sensors = [Sensor(self, 1.03125 * self.h,  self.w/4, angle=+radians(20)),
                        Sensor(self, 1.03125 * self.h, -self.w/4, angle=-radians(20))]
        wheel_size = (self.sizescale * 40, self.sizescale * 20)
        self.left_wheel  = Wheel(self, 0, -self.w/2, side='left',  size=wheel_size)
        self.right_wheel = Wheel(self, 0,  self.w/2, side='right', size=wheel_size)
        self.links   = [Link(self.sensors[0].plug, self.left_wheel.plug),
                        #Link(self.sensors[0].plug, self.right_wheel.plug),
                        #Link(self.sensors[1].plug, self.left_wheel.plug),
                        Link(self.sensors[1].plug, self.right_wheel.plug),
                       ]

    @property
    def wheel_speeds(self):
        return self.left_wheel.speed, self.right_wheel.speed

    @wheel_speeds.setter
    def wheel_speeds(self):
        lw, rw = speeds
        self.left_wheel.speed, self.right_wheel.speed = lw, rw

    def world_pos(self):
        """Return the world position of the vehicle"""
        return self.x, self.y, self.angle

    def step(self, world, dt=0.01):
        """Update the state of the vehicle"""
        self.update_wheel_speed(world.lights)
        self.update_position(dt)

    def update_wheel_speed(self, lights):
        """Update the wheel speeds as a function of the sensors activity"""
        for sensor in self.sensors:
            sensor.activation(lights.values())

        for link in self.links:
            link.step()

        self.left_wheel.step()
        self.right_wheel.step()


    def update_position(self, dt):
        v1, v2 = self.wheel_speeds
        if v2 == v1:
            dangle, dy, dx = 0.0, 0.0, dt * v1
        else:
            dangle = dt / self.w * (v1 - v2)
            R = self.w / 2 * (v1 + v2) / (v2 - v1)
            dx = -cos(dangle / 2) * 2 * R * sin(dangle / 2)
            dy =  sin(dangle / 2) * 2 * R * sin(dangle / 2)

        self.angle += dangle
        dx, dy = (cos(self.angle) * dx - sin(self.angle) * dy,
                  sin(self.angle) * dx + cos(self.angle) * dy)

        self.x += dx
        self.y += dy


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
        rect(0.4375 * self.h, 0, self.h, 0.8*self.w)

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
        self.acts = []

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

    def receive(self, act):
        self.acts.append(act)

    def step(self):
        """Compute speed"""
        if len(self.acts) > 0:
            s = 0
            for act in self.acts:

                s += act
            self.speed = 0.5*exp(5.0*s)/len(self.acts)
            self.acts = []


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
        self.act       = 0.0
        self.w         = 100.0

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

        self.act *= 1.0

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