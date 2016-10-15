from vehicle import Vehicle


class Interface:

    def __init__(self, cp5, vehicle, font=None, sidebar=300):
        self.lw, self.rw = 0.0, 0.0

        self.cp5 = cp5
        self.cp5.setAutoDraw(False)
        self.vehicle = vehicle
        self.sidebar = sidebar

        self.sidebar_vehicle = Vehicle(width-sidebar/2, height/2 + vehicle.h/2, 
                                       w=vehicle.w, h=vehicle.h, sizescale=vehicle.sizescale,
                                       angle=radians(-90))

        self.lines = []

        def slider_style(slider, pos, active=True):
            slider.setPosition(*pos)
            
            slider.setSize(16, 150)
            slider.setRange(-100, 100)
            slider.setColorBackground(color(250,105, 0))
            slider.setColorForeground(color(255,185, 0))
            if not active:
                slider.setColorActive(color(255,185, 0))
            else:
                slider.setColorActive(color(255,225, 0))
            slider.setColorValue(color(0))
            slider.setColorLabel(color(0))
            
            if font is not None:
                slider.getValueLabel().setFont(font)
                slider.getCaptionLabel().toUpperCase(False)
                slider.getCaptionLabel().setFont(font)
                slider.setCaptionLabel("")
        
            #slider.setLock(not active)
        
            self.lines.append((pos[0], pos[1]+150/2, pos[0] + 15, pos[1] + 150/2))                

        self.lw_slider = self.cp5.addSlider("Roue Gauche")
        self.lw_slider.setValue(self.vehicle.left_wheel.speed)
        slider_style(self.lw_slider, (902, 550), active=False)
    
        self.rw_slider = self.cp5.addSlider("Roue Droite")
        self.rw_slider.setValue(self.vehicle.right_wheel.speed)
        slider_style(self.rw_slider, (982, 550), active=False)

        self.linkmap = {'Capteur Gauche -> Roue Gauche': 2,
                        'Capteur Droit -> Roue Droite' : 1,
                        'Capteur Gauche -> Roue Droite': 3,
                        'Capteur Droite -> Roue Gauche': 0}

        for name, pos in zip(self.linkmap.keys(), [(850-8, 460-50), (1050-8, 460-50), (850-8, 320-100), (1050-8, 320-100)]):
            w_slider = self.cp5.addSlider(name)
            w_slider.setValue(self.vehicle.links[self.linkmap[name]].w)
            slider_style(w_slider, pos, active=True)
            w_slider.setRange(-1.0, 1.0)
            w_slider.addListener(self.callback)
            

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
        # sidebar    
        stroke(0)
        fill(255)
        rect(width-self.sidebar/2, height/2, self.sidebar, height+2) 
        
        self.sidebar_vehicle.sensors[0].act = self.vehicle.sensors[0].act
        self.sidebar_vehicle.sensors[1].act = self.vehicle.sensors[1].act
        self.sidebar_vehicle.draw()
        
        stroke(color(250,105, 0, 100))
        fill(color(250,105, 0, 100))
        strokeWeight(2)

        line (910, 600, 910, 460)
        ellipse(910, 460, 4, 4)
        line (990, 600, 990, 460)
        ellipse(990, 460, 4, 4)

        ellipse(930, 420, 4, 4)
        line (930, 420, 900, 420)
        line (900, 420, 850, 460)

        ellipse(970, 420, 4, 4)
        line (970, 420, 1000, 420)
        line (1000, 420, 1050, 460)

        ellipse(956, 380, 4, 4)
        line (956, 380, 1000, 380)
        line (1000, 380, 1050, 320)

        ellipse(944, 380, 4, 4)
        line (944, 380, 900, 380)
        line (900, 380, 850, 320)

                
        self.cp5.draw()
        
        stroke(255, 0, 0, 150)
        strokeWeight(1)
        for ln in self.lines:
            line(*ln)
        
        