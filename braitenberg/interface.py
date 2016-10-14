

class Interface:

    def __init__(self, cp5, vehicle, font=None):
        self.lw, self.rw = 0.0, 0.0

        self.cp5 = cp5
        self.cp5.setAutoDraw(False)
        self.vehicle = vehicle

        self.lines = []

        def slider_style(slider, pos, active=True):
            slider.setPosition(*pos)
            
            slider.setSize(200, 20)
            slider.setRange(-100, 100)
            slider.setColorBackground(color(220))
            slider.setColorForeground(color(150))
            slider.setColorActive(color(150))
            slider.setColorValue(color(0))
            slider.setColorLabel(color(0))
            
            if font is not None:
                slider.getValueLabel().setFont(font)
                slider.getCaptionLabel().toUpperCase(False)
                slider.getCaptionLabel().setFont(font)
        
            #slider.setLock(not active)
        
            self.lines.append((pos[0] + 100, pos[1], pos[0] + 100, pos[1] + 19))                

        self.lw_slider = self.cp5.addSlider("Roue Gauche")
        self.lw_slider.setValue(self.vehicle.left_wheel.speed)
        slider_style(self.lw_slider, (50, 700), active=False)
    
        self.rw_slider = self.cp5.addSlider("Roue Droite")
        self.rw_slider.setValue(self.vehicle.right_wheel.speed)
        slider_style(self.rw_slider, (50, 730), active=False)

        self.linkmap = {'Capteur Gauche -> Roue Gauche': 2,
                        'Capteur Droit -> Roue Droite' : 1,
                        'Capteur Gauche -> Roue Droite': 3,
                        'Capteur Droite -> Roue Gauche': 0}

        for name, pos_y in zip(self.linkmap.keys(), [550, 580, 610, 640]):
            w_slider = self.cp5.addSlider(name)
            w_slider.setValue(self.vehicle.links[self.linkmap[name]].w)
            slider_style(w_slider, (50, pos_y), active=True)
            w_slider.setRange(-1.0, 1.0)
            w_slider.addListener(self.callback)
                                        
        #self.cp5.getController("Roue Droite").addListener(self.callback)
        #self.cp5.getController("Roue Gauche").addListener(self.callback)

    def callback(self, slider):
        slider_name = slider.getName()
        if slider_name in self.linkmap:
            self.vehicle.links[self.linkmap[slider_name]]. w = slider.getValue()
        else:
            raise ValueError("Unrecognized slider")
    
    def update_sliders(self):
        self.lw_slider.setValue(self.vehicle.left_wheel.speed)
        self.rw_slider.setValue(self.vehicle.right_wheel.speed)

    def draw(self):
        self.cp5.draw()
        
        stroke(50, 50, 50)
        strokeWeight(1)
        for ln in self.lines:
            line(*ln)