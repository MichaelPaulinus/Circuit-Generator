import os
import random
import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()

# component 1
c1 = random.randint(1,3)
if c1==1:
    d.add(elm.Diode())
elif c1==2:
    d.add(elm.Photodiode())    
else:
    d.add(elm.Potentiometer())

# component 2
c2 = random.randint(1,3)
if c2==1:
    d.add(elm.Capacitor(d='down'))
elif c2==2:
    d.add(elm.Inductor(d='down'))
else:
    d.add(elm.LED(d='down'))

# component 3
d.add(elm.Resistor(d='left'))
d.add(elm.Ground)

# component 4
c4 = random.randint(1,2)
if c4==1:
    d.add(elm.SourceV(d='up'))
else:
    d.add(elm.SourceSin(d='up'))

d.draw()


i = 0
while os.path.exists("schematic%s.png" % i):
    i += 1
d.save("schematic%s.png" % i, "w")