class Interface:

    def __init__(self, cp5, vehicle):
        self.lw, self.rw = 0.0, 0.0

        self.cp5 = cp5
        self.cp5.setAutoDraw(False)
        self.vehicle = vehicle

        self.lines = []

        def slider_style(slider):
            slider.setSize(200, 20)
            slider.setRange(-100, 100)
            slider.setColorBackground(color(220))
            slider.setColorForeground(color(150))
            slider.setColorActive(color(150))
            slider.setColorValue(color(0))
            slider.setColorLabel(color(0))
        

        self.lw_slider = self.cp5.addSlider("Roue Droite")
        self.lw_slider.setPosition(50, 700)
        self.lw_slider.setValue(self.vehicle.left_wheel.speed)
        slider_style(self.lw_slider)
        self.lines.append((150, 700, 150, 719))                
    
        self.rw_slider = self.cp5.addSlider("Roue Gauche")
        self.rw_slider.setPosition(50, 730)
        self.rw_slider.setValue(self.vehicle.right_wheel.speed)
        slider_style(self.rw_slider)
        self.lines.append((150, 730, 150, 749))                
        
        self.cp5.getController("Roue Droite").addListener(self.callback)
        self.cp5.getController("Roue Gauche").addListener(self.callback)

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
        
    def draw(self):
        self.cp5.draw()
        
        stroke(50, 50, 50)
        strokeWeight(1)
        for ln in self.lines:
            line(*ln)