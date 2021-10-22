# -*- coding: utf-8 -*-
import numpy as np
from gnuradio import gr


class APCMA_Decode(gr.sync_block):
    def __init__(self, B=2):
        gr.sync_block.__init__(
            self,
            name='Decoding APCMA',
            in_sig=[np.float32],
            out_sig=None
        )

        self.B = B # [bits/symbol]
        self.Nslot = 2 ** (self.B + 1) + 5
        self.ApcmaCode = [[0] * self.Nslot for i in range(2 ** self.B)]
        for i in range(2 ** self.B):
            self.ApcmaCode[i][0] = 1
            self.ApcmaCode[i][i + 2] = 1
            self.ApcmaCode[i][- i - 3] = 1
            self.ApcmaCode[i][-1] = 1

        self.PulseList = np.zeros(self.Nslot)

    def work(self, input_items, output_items):
        for i in range(len(input_items[0][:])):
            self.PulseList = np.append(self.PulseList[1:], input_items[0][i])
            for j in range(len(self.ApcmaCode)):
                if np.all(np.logical_and(self.ApcmaCode[j][:],self.PulseList)==self.ApcmaCode[j][:]):
                    print("Word:{}".format(j+1))
                    print(self.PulseList)
        # output_items[0][:] = input_items[0][:]
        # return len(output_items[0][:])
        return 0
