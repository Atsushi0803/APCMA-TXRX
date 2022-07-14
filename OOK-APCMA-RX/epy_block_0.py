import numpy as np
from gnuradio import gr
import math


class SignalDetection(gr.decim_block):
    def __init__(self, slot_length=128, sub_slot_rate=8, threshold=0.2):
        gr.decim_block.__init__(
            self,
            name='Signal Detection',
            in_sig=[np.float32, np.float32],
            out_sig=[np.float32],
            decim=slot_length/sub_slot_rate)

        self.decim = int(slot_length/sub_slot_rate)
        self.set_relative_rate(sub_slot_rate/slot_length)
        self.threshold = threshold

    def work(self, input_items, output_items):
        tmp = [(abs(input_items[0][i]) > 0.1) or (abs(input_items[1][i]) > 0.1) for i in range(len(input_items[0]))]
        output_items[0][:] = [sum(tmp[i * self.decim:(i + 1) * self.decim]) > self.decim * 0.5 for i in range(len(output_items[0][:]))]
        return len(output_items[0][:])
