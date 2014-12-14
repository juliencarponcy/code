import PyControl as pc
import hardware as hw
from two_step import *

pc.verbose = True

box = hw.Box(pc)

t = Two_step(pc,box)

# Initialise hardware.

# boxIO = hw.BoxIO(pc)

# poke_1 = hw.Poke(boxIO, 1)
# button_1 = Button(pc, poke_1)

# poke_2 = hw.Poke(boxIO, 2)
# poke_3 = hw.Poke(boxIO, 3)
# poke_4 = hw.Poke(boxIO, 4)

# # Instantiate state machines.

# button_1 = Button(pc, poke_1)
# button_2 = Button(pc, poke_2)
# button_3 = Button(pc, poke_3)
# button_4 = Button(pc, poke_4)

# Run PyControl.

def run(dur = 20):
	pc.run_machines(dur * second)  







