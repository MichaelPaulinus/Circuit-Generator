import os
import random
import schemdraw
import schemdraw.elements as elm
from schemdraw.elements.lines import Line, LineDot
from schemdraw.elements.transistors import Bjt

while True:
    d = schemdraw.Drawing()

    # component 1

    c1 = random.randint(1,4) # random component 1 selection

    if c1==1:
        comp1 = elm.Diode()
    elif c1==2:
        comp1 = elm.Zener()
    elif c1 == 3:
        comp1 = elm.Opamp()
    else:
        comp1 = elm.Bjt(label='$Q_1$')

    d.add(comp1) # add component 1

    # component 2

    c2 = random.randint(1,4) # random component 2 selection

    if c1 == 4: # check for bjt
        comp2 = elm.Resistor(d='left',at=comp1.base, label='%dk$\Omega$' % random.randrange(1,100), lftlabel='$V_{in}$')
    elif c1==3: # check for op-amp
        non_inv = random.random()
        if non_inv>0.5: # non-inverting
            comp2 = elm.LineDot(d='left',at=comp1.in1, l=1) # input 1
            comp2a = elm.Resistor(label='%dk$\Omega$' % random.randrange(1,100))
        else: # inverting
            comp2 = elm.LineDot(d='left',at=comp1.in1, l=1) # input 1
            comp2a = elm.Resistor(label='%dk$\Omega$' % random.randrange(1,100), lftlabel='$V_{in}$')
    else:
        if c2==1:
            comp2 = elm.Capacitor(d='down', label='%d$\mu$F' % random.randrange(1,100))
        elif c2==2:
            comp2 = elm.Inductor(d='down', label='%dmH' % random.randrange(1,20))
        elif c2==3:
            comp2 = elm.Resistor(d='down')
        else:
            comp2 = elm.LED(d='down')

    d.add(comp2) # add component 2
    if c1==3:
        d.add(comp2a)

    if c1==3: # special case for op-amp
        if non_inv>0.5: # non-inverting
            d.add(elm.Ground(d='right'))
            d.labelI(comp2a, arrowlen=1)
        else: # inverting
            d.labelI(comp2a, arrowlen=1, reverse=True)

    # component 3

    if c1 == 4: # check for bjt
        temp = random.randrange(1,2)
        if temp==1:
            d.add(elm.Resistor(d='down', at=comp1.emitter, label='%dk$\Omega$' % random.randrange(1,100)))
            d.add(elm.Ground)
        else:
            d.add(elm.Ground(at=comp1.emitter))
    elif c1==3: # check for op-amp
        if non_inv>0.5: # non-inverting
            comp3 = elm.LineDot(d='left',at=comp1.in2, lftlabel='$V{in}$')
        else: # inverting
            comp3 = elm.Line(d='left', at=comp1.in2, l=1)

        d.add(comp3)
        if non_inv<0.5: # special case for inverting op-amp
            d.add(elm.Ground(d='right'))

    else:
        d.add(elm.Resistor(d='left', label='%dk$\Omega$' % random.randrange(1,100)))
        d.add(elm.Ground)

    # component 4

    if c1==4: # check for bjt
        comp4 = elm.Resistor(d='up',at=comp1.collector, label='%dk$\Omega$' % random.randrange(1,100), rgtlabel='$V_{cc}$')
    elif c1==3: # check for op-amp
        comp4 = elm.LineDot(d='right', at=comp1.out, rgtlabel='$V_{out}$')
    else:
        c4 = random.random() # selection AC/DC Source
        if c4>0.5:
            comp4 = elm.SourceV(d='up', label='12V')
        else:
            comp4 = elm.SourceSin(d='up', label='12V')

    d.add(comp4) # add component 4
    if c1==3: # special case for op-amp
        d.add(elm.Line(d='up'))
        R2 = elm.Resistor(d='left', label='%dk$\Omega$' % random.randrange(1,100), tox=comp2.end)
        d.add(R2)
        d.add(elm.Line(d='down', toy=comp2.end))

    # labels for current direction
    #    if non_inv>0.5: # non-inverting
            # d.labelI(R2, arrowlen = 1)
        # else: # inverting
            # d.labelI(R2, arrowlen = 1, reverse=True)

    #d.draw() # if you wanna display circuit on screen

    # file name convention
    i = 0
    while os.path.exists("schematic%s.png" % i):
        i += 1

    d.save("schematic%s.png" % i, False, 300)