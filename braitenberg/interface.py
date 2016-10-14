class Interface:

    def __init__(self, cp5, vehicle):
        self.lw, self.rw = 0.0, 0.0

        self.cp5 = cp5
        self.vehicle = vehicle

        lw_slider = self.cp5.addSlider("Left Wheel")
        lw_slider.setPosition(50, 700)
        lw_slider.setSize(200, 20)
        lw_slider.setRange(-100, 100)
        lw_slider.setValue(self.vehicle.left_wheel.speed)
        lw_slider.setColorLabel(color(0))
        self.lw_slider = lw_slider

        rw_slider = self.cp5.addSlider("Right Wheel")
        rw_slider.setPosition(50, 730)
        rw_slider.setSize(200, 20)
        rw_slider.setRange(-100, 100)
        rw_slider.setValue(self.vehicle.right_wheel.speed)
        rw_slider.setColorLabel(color(0))
        self.rw_slider = rw_slider

        self.cp5.getController("Left Wheel").addListener(self.callback)
        self.cp5.getController("Right Wheel").addListener(self.callback)

    def callback(self, slider):
        pass
    # def callback(self, slider):
    #     if slider.getName() == 'Left Wheel':
    #         self.lw = slider.getValue()
    #     elif slider.getName() == 'Right Wheel':
    #         self.rw = slider.getValue()
    #     else:
    #         raise ValueError("Unrecognized slider")
    
    def update_sliders(self):
        self.lw_slider.setValue(self.vehicle.left_wheel.speed)
        self.rw_slider.setValue(self.vehicle.right_wheel.speed)
