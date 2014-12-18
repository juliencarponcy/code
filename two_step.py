from State_machine import *

class Two_step(State_machine):

    states = ['pre_session',
              'post_session',
              'center_active',
              'left_active',
              'right_active',
              'left_reward',
              'right_reward',
              'wait_for_poke_out',
              'inter_trial']

    events = ['left_poke', 
              'left_poke_out',
              'right_poke',
              'right_poke_out',
              'high_poke',
              'low_poke',
              'session_timer',
              'state_timer',
              'session_startstop']

    initial_state = 'pre_session'

    norm_prob = 0.8
    reward_probs = [0.2,0.8]

    def __init__(self, PyControl, box):

        self.box = box

        State_machine.__init__(self, PyControl, box)

    def stop(self):
        self.box.off()

    # State event handler functions.

    def all_states(self, event):
        if event == 'session_startstop' and not self.state == 'pre_session':
            self.goto('post_session')

    def pre_session(self, event):
        if event == 'session_startstop':
            self.box.houselight.on()
            self.goto('center_active')

    def post_session(self, event):
            self.box.houselight.off()     

    def center_active(self, event):
        if event == 'entry':
            self.box.center_poke.LED.on()
        elif event == 'exit':
            self.box.center_poke.LED.off()
        elif event == 'high_poke':
            if withprob(self.norm_prob):
                self.goto('left_active')
            else:
                self.goto('right_active')
        elif event == 'low_poke':
            if withprob(self.norm_prob):
                self.goto('right_active')
            else:
                self.goto('left_active')

    def left_active(self, event):
        if event == 'entry':
            self.box.left_poke.LED.on()
        elif event == 'exit':
            self.box.left_poke.LED.off()
        elif event == 'left_poke':
            if withprob(self.reward_probs[0]):
                self.goto('left_reward')
            else:
                self.goto('wait_for_poke_out')

    def right_active(self, event):
        if event == 'entry':
            self.box.right_poke.LED.on()
        elif event == 'exit':
            self.box.right_poke.LED.off()
        elif event == 'right_poke':
            if withprob(self.reward_probs[1]):
                self.goto('right_reward')
            else:
                self.goto('wait_for_poke_out')

    def left_reward(self, event):
        if event == 'entry':
            self.box.left_poke.SOL.on()
            self.set_timer('state_timer', 100 * ms)
        elif event == 'exit':
            self.box.left_poke.SOL.off()
        elif event == 'state_timer':
            self.goto('wait_for_poke_out')

    def right_reward(self, event):
        if event == 'entry':
            self.box.right_poke.SOL.on()
            self.set_timer('state_timer', 100 * ms)
        if event == 'exit':
            self.box.right_poke.SOL.off()
        if event == 'state_timer':
            self.goto('wait_for_poke_out')     
        
    def wait_for_poke_out(self, event):
        if event == 'entry':
            if not (self.box.left_poke.get_state() or \
                    self.box.right_poke.get_state()):
                self.goto('inter_trial') # Subject already left poke.
        elif event in ['left_poke_out', 'right_poke_out']:
            self.goto('inter_trial')

    def inter_trial(self, event):
        if event == 'entry':
            self.set_timer('state_timer', 1 * second)
        if event == 'state_timer':
            self.goto('center_active')









