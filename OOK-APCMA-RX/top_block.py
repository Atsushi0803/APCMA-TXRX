#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.7.13.5
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import epy_block_0
import epy_block_1
import epy_block_2
import time


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200000
        self.Threshhold = Threshhold = 0.1
        self.Sub_Slot_Rate = Sub_Slot_Rate = 5
        self.Slot_Length = Slot_Length = 100
        self.Bits_Per_Symbol = Bits_Per_Symbol = 4

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(924000000, 0)
        self.uhd_usrp_source_0.set_gain(10, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0.set_bandwidth(200000, 0)
        self.uhd_usrp_source_0.set_auto_dc_offset(True, 0)
        self.uhd_usrp_source_0.set_auto_iq_balance(True, 0)
        self.epy_block_2 = epy_block_2.APCMA_Decode(B=Bits_Per_Symbol)
        self.epy_block_1 = epy_block_1.pulse_detection(Sub_slot_rate=Sub_Slot_Rate)
        self.epy_block_0 = epy_block_0.signal_detection(slot_length=Slot_Length, sub_slot_rate=Sub_Slot_Rate, threshhold=Threshhold)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 1), (self.epy_block_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.epy_block_0, 0))
        self.connect((self.epy_block_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_1, 0), (self.epy_block_2, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_complex_to_float_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_Threshhold(self):
        return self.Threshhold

    def set_Threshhold(self, Threshhold):
        self.Threshhold = Threshhold
        self.epy_block_0.threshhold = self.Threshhold

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
        self.epy_block_2.B = self.Bits_Per_Symbol


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
