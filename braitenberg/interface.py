class Interface:
    
    def __init__(self, cp5, lw=0.0, rw=0.0):
        self.lw, self.rw = lw, rw
                       
        self.cp5 = cp5
         
        lw_slider = self.cp5.addSlider("Left Wheel")
        lw_slider.setPosition(50, 700)
        lw_slider.setSize(200, 20)
        lw_slider.setRange(-200, 200)
        lw_slider.setValue(self.lw)
        lw_slider.setColorLabel(color(0))
        
        rw_slider = self.cp5.addSlider("Right Wheel")
        rw_slider.setPosition(50, 730)
        rw_slider.setSize(200, 20)
        rw_slider.setRange(-200, 200)
        rw_slider.setValue(self.rw)
        rw_slider.setColorLabel(color(0))
        
        self.cp5.getController("Left Wheel").addListener(self.callback)
        self.cp5.getController("Right Wheel").addListener(self.callback)
    
    def callback(self, slider):
        if slider.getName() == 'Left Wheel':
            self.lw = slider.getValue()
        elif slider.getName() == 'Right Wheel':
            self.rw = slider.getValue()
        else:
            raise ValueError("Unrecognized slider")  
            
        