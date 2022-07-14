#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: APCMA_Demodulation
# Author: Atsushi.N
# GNU Radio version: 3.8.3.1

from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import epy_block_0
import epy_block_1
import epy_block_2


class OOK_APCMA_RX(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "APCMA_Demodulation")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 250000
        self.Threshold = Threshold = 0.2
        self.Sub_Slot_Rate = Sub_Slot_Rate = 8
        self.Slot_Length = Slot_Length = 128
        self.Bits_Per_Symbol = Bits_Per_Symbol = 4

        ##################################################
        # Blocks
        ##################################################
        self.epy_block_2 = epy_block_2.ApcmaDecode(bits_per_symbol=Bits_Per_Symbol)
        self.epy_block_1 = epy_block_1.PulseDetection(Sub_slot_rate=Sub_Slot_Rate)
        self.epy_block_0 = epy_block_0.SignalDetection(slot_length=Slot_Length, sub_slot_rate=Sub_Slot_Rate, threshold=Threshold)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, 'C:\\Users\\Atsushi.N\\Desktop\\wav_sink\\data1.wav', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.epy_block_0, 1))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.epy_block_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_1, 0), (self.epy_block_2, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_Threshold(self):
        return self.Threshold

    def set_Threshold(self, Threshold):
        self.Threshold = Threshold
        self.epy_block_0.threshold = self.Threshold

    def get_Sub_Slot_Rate(self):
        return self.Sub_Slot_Rate

    def set_Sub_Slot_Rate(self, Sub_Slot_Rate):
        self.Sub_Slot_Rate = Sub_Slot_Rate

    def get_Slot_Length(self):
        return self.Slot_Length

    def set_Slot_Length(self, Slot_Length):
        self.Slot_Length = Slot_Length

    def get_Bits_Per_Symbol(self):
        return self.Bits_Per_Symbol

    def set_Bits_Per_Symbol(self, Bits_Per_Symbol):
        self.Bits_Per_Symbol = Bits_Per_Symbol
        self.epy_block_2.bits_per_symbol = self.Bits_Per_Symbol





def main(top_block_cls=OOK_APCMA_RX, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
