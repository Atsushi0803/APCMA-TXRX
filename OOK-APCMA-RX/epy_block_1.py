import numpy as np
from gnuradio import gr


class pulse_detection(gr.decim_block):
    def __init__(self, Sub_slot_rate=5):
        gr.decim_block.__init__(self,
            name='Pulse Detection',
            in_sig=[np.float32],
            out_sig=[np.float32],
            decim = 5)
        self.decim = Sub_slot_rate
        self.set_relative_rate(1.0/self.decim)

    def work(self, input_items, output_items):
        output_items[0][:] = [sum(input_items[0][j+self.decim*i] > 0.5 for j in range(self.decim)) >= 3 for i in range(len(output_items[0][:]))]
        return len(output_items[0][:])