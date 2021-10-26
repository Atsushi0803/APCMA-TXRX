import numpy as np
from gnuradio import gr


class pulse_detection(gr.decim_block):
    def __init__(self, Sub_slot_rate=5):
        gr.decim_block.__init__(self,
            name='Pulse Detection',
            in_sig=[np.float32],
            out_sig=[np.float32],
            decim = Sub_slot_rate)
        self.decim = Sub_slot_rate
        self.set_relative_rate(1.0/Sub_slot_rate)

    def work(self, input_items, output_items):
        output_items[0][:] = [(sum(input_items[0][self.decim * i : self.decim * (i + 1)]) > 0.5 * self.decim) for i in range(len(output_items[0][:]))]
        return len(output_items[0][:])
