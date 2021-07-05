import os
import random
import schemdraw
import schemdraw.elements as elm
from schemdraw.elements.lines import Line, LineDot
from schemdraw.elements.transistors import Bjt

# components used
# resistor
# capacitor
# inductor
# bjt
# dc voltage source
# ac voltage source
# controlled voltage source
# diode
# op-amp
# ground

while True:
    d = schemdraw.Drawing()

    # component 1 selection (backbone of circuit)
    # component 1 is selected randomly by assigning each component to a random int ranging from 1->4
    c1 = random.randint(1,4) # random component 1 selection

    if c1==1: # diode selected
        comp1 = elm.Diode()
    elif c1==2: # multiple branches circuit selected
        if random.random()>0.5:
            comp1 = elm.Resistor(label='%dk$\Omega$' % random.randrange(1,100)) # resistor with label
        else:
            comp1 = elm.Resistor() # resistor without label
    elif c1 == 3: # op-amp selected
        comp1 = elm.Opamp()
    else: # bjt selected
        if random.random()>0.5:
            comp1 = elm.Bjt(label='$Q_1$') # bjt with label
        else:
            comp1 = elm.Bjt() # bjt without label

    d.add(comp1) # add component 1

    # component 2 selection
    # component 2 is also selected randomly, however it takes into account component 1's selection
    # eg. if component 1 is a bjt, the next component to follow must be connected at either the base, collector or emitter of bjt
    # eg. if component 1 is an op-amp, the next component to follow must be connected  at V1 or V2 of the op-amp
    c2 = random.randint(1,4) # random component 2 selection

    if c1 == 4: # check if component 1 is a bjt so arrangement of following components allign with bjt
        if random.random()>0.5:
            comp2 = elm.Resistor(d='left',at=comp1.base, label='%dk$\Omega$' % random.randrange(1,100), lftlabel='$V_{in}$')
        else:
            comp2 = elm.Resistor(d='left',at=comp1.base, lftlabel='$V_{in}$')
    elif c1==3: # check for op-amp selection
        non_inv = random.random()
        if non_inv>0.5: # creates a non-inverting op-amp
            comp2 = elm.LineDot(d='left',at=comp1.in1, l=1) # input 1
            if random.random()>0.5:
                comp2a = elm.Resistor(label='%dk$\Omega$' % random.randrange(1,100))
            else:
                comp2a = elm.Resistor()
        else: # creates an inverting op-amp
            comp2 = elm.LineDot(d='left',at=comp1.in1, l=1) # input 1
            if random.random()>0.5:
                comp2a = elm.Resistor(label='%dk$\Omega$' % random.randrange(1,100), lftlabel='$V_{in}$')
            else:
                comp2a = elm.Resistor(lftlabel='$V_{in}$')
	# if component 1 is not a component with special requirements such as an op-amp/bjt, the following else statement is executed                
    else: # basic circuit
        if c2==1:
            if random.random()>0.5:
                comp2 = elm.Capacitor(d='down', label='%d$\mu$F' % random.randrange(1,100))
            else:
                comp2 = elm.Capacitor(d='down')
        elif c2==2:
            if random.random()>0.5:
                comp2 = elm.Inductor(d='down', label='%dmH' % random.randrange(1,20))
            else:
                comp2 = elm.Inductor(d='down')
        elif c2==3:
            if random.random()>0.5:
                comp2 = elm.Resistor(d='down', label='%dk$\Omega$' % random.randrange(1,100))
            else:
                comp2 = elm.Resistor(d='down')
        else:
            comp2 = elm.SourceControlledV(d='down', reverse=True)

    d.add(comp2) # add component 2
    if c1==3:
        d.add(comp2a)

    if c1==3: # special case for op-amp
        if non_inv>0.5: # non-inverting
            d.add(elm.Ground(d='right'))

    # component 3 selection
    # similar rules from component 2 selection applies to component 3 selection
    if c1 == 4: # check for bjt
        temp1 = random.randrange(1,2)
        if temp1==1:
            if random.random()>0.5:
                d.add(elm.Resistor(d='down', at=comp1.emitter, label='%dk$\Omega$' % random.randrange(1,100)))
            else:
                d.add(elm.Resistor(d='down', at=comp1.emitter))                
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
        if random.random()>0.5:
            d.add(elm.Resistor(d='left', label='%dk$\Omega$' % random.randrange(1,100)))
        else:
            d.add(elm.Resistor(d='left'))
        d.add(elm.Ground)

    # component 4 selection
    if c1==4: # check for bjt
        if random.random()>0.5:
            comp4 = elm.Resistor(d='up',at=comp1.collector, label='%dk$\Omega$' % random.randrange(1,100), rgtlabel='$V_{cc}$')
        else:
            comp4 = elm.Resistor(d='up',at=comp1.collector, rgtlabel='$V_{cc}$')
    elif c1==3: # check for op-amp
        comp4 = elm.LineDot(d='right', at=comp1.out, rgtlabel='$V_{out}$')
    else:
        if random.random()>0.5: # selection AC/DC Source
            if random.random()>0.5:
                comp4 = elm.SourceV(d='up', label='12V')
            else:
                comp4 = elm.SourceV(d='up')
        else:
            if random.random()>0.5:
                comp4 = elm.SourceSin(d='up', label='12V')
            else:
                comp4 = elm.SourceSin(d='up')

    d.add(comp4) # add component 4
    if c1==3: # special case for op-amp
        d.add(elm.Line(d='up'))
        if random.random()>0.5:
            R2 = elm.Resistor(d='left', label='%dk$\Omega$' % random.randrange(1,100), tox=comp2.end)
        else:
            R2 = elm.Resistor(d='left', tox=comp2.end)
        d.add(R2)
        d.add(elm.Line(d='down', toy=comp2.end))

    # component 5 selection
    if random.random()>0.5: # for multiple branches
        if c1==1 or c1==2:
            if random.random()>0.5: # add resistor
                if random.random()>0.5:
                    comp5 = elm.Resistor(d='right', at=comp1.end, label='%dk$\Omega$' % random.randrange(1,100))
                else:
                    comp5 = elm.Resistor(d='right', at=comp1.end)
            else:
                if random.random()>0.5: # add capacitor
                    comp5 = elm.Capacitor(d='right', at=comp1.end,label='%d$\mu$F' % random.randrange(1,100))
                else:
                    comp5 = elm.Capacitor(d='right', at=comp1.end)
            d.add(comp5)

            if random.random()>0.5: # add DC source
                if random.random()>0.5:
                    comp6 = elm.SourceV(d='down', label='12V', at=comp5.end, tox=comp2.end, reverse=True)
                else:
                    comp6 = elm.SourceV(d='down', at=comp5.end, tox=comp2.end, reverse=True)                    
            else: # add AC source
                if random.random()>0.5:
                    comp6 = elm.SourceSin(d='down', label='12V', at=comp5.end, tox=comp2.end)
                else:
                    comp6 = elm.SourceSin(d='down', at=comp5.end, tox=comp2.end)
            d.add(comp6)
            d.add(elm.Line(d='left', at=comp6.end, tox=comp2.end)) 

    # saved image file name convention
    i = 0
    while os.path.exists("schematic%s.jpg" % i):
        i += 1

    d.save("schematic%s.jpg" % i, False, 300)