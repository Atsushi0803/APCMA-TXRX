import numpy as np
from gnuradio import gr


class PulseDetection(gr.decim_block):
    def __init__(self, Sub_slot_rate=8):
        gr.decim_block.__init__(
            self,
            name='Pulse Detection',
            in_sig=[np.float32],
            out_sig=[np.float32],
            decim = Sub_slot_rate)
        self.decim = Sub_slot_rate
        self.set_relative_rate(1.0/Sub_slot_rate)

    def work(self, input_items, output_items):
        output_items[0][:] = [sum(input_items[0][j+self.decim*i] > 0.5 for j in range(self.decim)) > self.decim * 0.5 for i in range(len(output_items[0][:]))]
        return len(output_items[0][:])
