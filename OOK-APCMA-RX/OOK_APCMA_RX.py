#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: APCMA_Demodulation
# Author: Atsushi.N
# GNU Radio version: 3.8.3.1

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import epy_block_0
import epy_block_1
import epy_block_2

from gnuradio import qtgui

class OOK_APCMA_RX(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "APCMA_Demodulation")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("APCMA_Demodulation")
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

        self.settings = Qt.QSettings("GNU Radio", "OOK_APCMA_RX")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.Threshhold = Threshhold = 400
        self.Sub_Slot_Rate = Sub_Slot_Rate = 5
        self.Slot_Length = Slot_Length = 400
        self.Bits_Per_Symbol = Bits_Per_Symbol = 2

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.epy_block_2 = epy_block_2.APCMA_Decode(B=Bits_Per_Symbol)
        self.epy_block_1 = epy_block_1.pulse_detection(Sub_slot_rate=Sub_Slot_Rate)
        self.epy_block_0 = epy_block_0.signal_detection(slot_length=Slot_Length, sub_slot_rate=Sub_Slot_Rate, threshhold=Threshhold)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\data.wav', False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.epy_block_1, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_wavfile_source_0, 1), (self.epy_block_0, 1))
        self.connect((self.epy_block_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.epy_block_1, 0), (self.epy_block_2, 0))
        self.connect((self.epy_block_2, 0), (self.qtgui_time_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "OOK_APCMA_RX")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

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





def main(top_block_cls=OOK_APCMA_RX, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
