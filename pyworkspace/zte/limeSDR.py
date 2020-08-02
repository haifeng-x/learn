#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Auto Acquire Test
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
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import limesdr
import sip
import sys
from gnuradio import qtgui
#import threading
import time


class limeSDR(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "limeSDR")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("limeSDR")
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

        self.settings = Qt.QSettings("GNU Radio", "limeSDR")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.sample_rate = sample_rate = 20e6
        self.rx_freq = rx_freq = 2.442e9
        self.gain_rx = gain_rx = 20

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	1024, #size
        	sample_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.limesdr_source_0 = limesdr.source('0009081C05C31C1A', 0, '')
        self.limesdr_source_0.set_sample_rate(sample_rate)
        self.limesdr_source_0.set_oversampling(1)
        self.limesdr_source_0.set_center_freq(rx_freq, 0)
        self.limesdr_source_0.set_bandwidth(sample_rate,0)
        self.limesdr_source_0.set_digital_filter(sample_rate,0)
        self.limesdr_source_0.set_gain(gain_rx,0)
        self.limesdr_source_0.set_antenna(1,0)
        self.limesdr_source_0.calibrate(sample_rate, 0)

        #self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'D:\\WORKSPACE\\limeSDR\\MineWorkFiles\\SavedFiles\\autotest', True)
        #self.blocks_file_sink_0.set_unbuffered(True)



        ##################################################
        # Connections
        ##################################################
        #self.connect((self.limesdr_source_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.limesdr_source_0, 0), (self.qtgui_time_sink_x_0, 0))

    def changefilename(self,astr):
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex * 1,
                                                   astr, True)
        #self.blocks_file_sink_0.close()
        self.blocks_file_sink_0.set_unbuffered(True)
        self.connect((self.limesdr_source_0, 0), (self.blocks_file_sink_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "limeSDR")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.sample_rate)
        self.limesdr_source_0.set_bandwidth(self.sample_rate,0)
        self.limesdr_source_0.set_digital_filter(self.sample_rate,0)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.limesdr_source_0.set_center_freq(self.rx_freq, 0)

    def get_gain_rx(self):
        return self.gain_rx

    def set_gain_rx(self, gain_rx):
        self.gain_rx = gain_rx
        self.limesdr_source_0.set_gain(self.gain_rx,0)


def main(top_block_cls=limeSDR, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    for i in range(0,10):
        a = ('D:\\ZTE\limeSDR\\Bluetooth\\VideoStream2442M%d') % (i)
        tb.changefilename(a)
        tb.start()
        time.sleep(4)
        tb.blocks_file_sink_0.close()
        tb.stop()
        tb.wait()

        #time.sleep(4)

if __name__ == '__main__':
    main()
