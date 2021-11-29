#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: OOK-APCMA Transmitter
# Author: Atsushi.N
# GNU Radio version: 3.8.3.1

from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import epy_block_0


class OOK_APCMA_TX(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "OOK-APCMA Transmitter")

        ##################################################
        # Variables
        ##################################################
        self.slot_width = slot_width = 64
        self.samp_rate = samp_rate = 125000
        self.interval_slot = interval_slot = 50
        self.bits_per_symbol = bits_per_symbol = 4

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_center_freq(924000000, 0)
        self.uhd_usrp_sink_0.set_gain(100, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(100000, 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.epy_block_0 = epy_block_0.ApcmaTransmitter(bits_per_symbol=bits_per_symbol, slot_width=slot_width, interval_slot=interval_slot)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.epy_block_0, 0), (self.uhd_usrp_sink_0, 0))


    def get_slot_width(self):
        return self.slot_width

    def set_slot_width(self, slot_width):
        self.slot_width = slot_width
        self.epy_block_0.slot_width = self.slot_width

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_interval_slot(self):
        return self.interval_slot

    def set_interval_slot(self, interval_slot):
        self.interval_slot = interval_slot
        self.epy_block_0.interval_slot = self.interval_slot

    def get_bits_per_symbol(self):
        return self.bits_per_symbol

    def set_bits_per_symbol(self, bits_per_symbol):
        self.bits_per_symbol = bits_per_symbol
        self.epy_block_0.bits_per_symbol = self.bits_per_symbol





def main(top_block_cls=OOK_APCMA_TX, options=None):
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
