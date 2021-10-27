#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: OOK-APCMA Trasmitter
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import epy_block_0
import sys
import time
from gnuradio import qtgui


class OOK_APCMA_TX(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "OOK-APCMA Trasmitter")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("OOK-APCMA Trasmitter")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "OOK_APCMA_TX")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.slot_width = slot_width = 128
        self.slot_per_buffer = slot_per_buffer = 10
        self.samp_rate = samp_rate = 250000
        self.interval_slot = interval_slot = 50
        self.bits_per_symbol = bits_per_symbol = 2

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(924000000, 0)
        self.uhd_usrp_sink_0.set_gain(100, 0)
        self.uhd_usrp_sink_0.set_bandwidth(200000, 0)
        self.epy_block_0 = epy_block_0.blk(B=bits_per_symbol, slot_width=slot_width, interval_slot=interval_slot, slot_per_buffer=slot_per_buffer)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.epy_block_0, 0), (self.uhd_usrp_sink_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "OOK_APCMA_TX")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_slot_width(self):
        return self.slot_width

    def set_slot_width(self, slot_width):
        self.slot_width = slot_width
        self.epy_block_0.slot_width = self.slot_width

    def get_slot_per_buffer(self):
        return self.slot_per_buffer

    def set_slot_per_buffer(self, slot_per_buffer):
        self.slot_per_buffer = slot_per_buffer
        self.epy_block_0.slot_per_buffer = self.slot_per_buffer

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
        self.epy_block_0.B = self.bits_per_symbol


def main(top_block_cls=OOK_APCMA_TX, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
