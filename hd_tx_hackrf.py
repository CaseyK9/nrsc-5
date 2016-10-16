#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Hd Tx Hackrf
# Generated: Sun Oct 16 13:22:42 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time


class hd_tx_hackrf(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Hd Tx Hackrf")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2000000
        self.freq = freq = 95.7e6

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_2 = filter.rational_resampler_ccc(
                interpolation=256,
                decimation=243,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=125,
                decimation=49,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=samp_rate / 200000,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(0, 0)
        self.osmosdr_sink_0.set_if_gain(40, 0)
        self.osmosdr_sink_0.set_bb_gain(0, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(1.5e6, 0)
          
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 80000, 20000, firdes.WIN_HAMMING, 6.76))
        self.fft_vxx_0 = fft.fft_vcc(2048, False, (), True, 1)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(2048, 2048+112, 0, '')
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((-1-1j, -1+1j, 1-1j, 1+1j, 0), 1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 2048)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((0.1, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.001, ))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, 'symbols.raw', False)
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=50000,
        	quad_rate=200000,
        	tau=75e-6,
        	max_dev=75e3,
        	fh=-1.0,
        )
        self.analog_sig_source_x_0 = analog.sig_source_f(50000, analog.GR_COS_WAVE, 1000, 0.1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.analog_wfm_tx_0, 0))    
        self.connect((self.analog_wfm_tx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.osmosdr_sink_0, 0))    
        self.connect((self.blocks_conjugate_cc_0, 0), (self.rational_resampler_xxx_1, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_conjugate_cc_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.rational_resampler_xxx_2, 0))    
        self.connect((self.rational_resampler_xxx_2, 0), (self.blocks_multiply_const_vxx_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 80000, 20000, firdes.WIN_HAMMING, 6.76))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)


def main(top_block_cls=hd_tx_hackrf, options=None):

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
