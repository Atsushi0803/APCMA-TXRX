# -*- coding: utf-8 -*-

import numpy as np
from gnuradio import gr
import csv
import random


############################### APCMA Transmitter ############################
class ApcmaTransmitter(gr.sync_block):
    def __init__(self, bits_per_symbol=4, slot_width=128, interval_slot=50, slot_per_buffer=1):
        gr.sync_block.__init__(
            self,
            name='APCMA Modulation',
            in_sig=None,
            out_sig=[np.complex64]
        )

        self.bits_per_symbol = bits_per_symbol  # [bit/symbol]
        self.slot_width = slot_width  # [sample]
        self.interval_slot = interval_slot  # シンボル間隔のスロット数 [slot]
        self.slot_per_buffer = slot_per_buffer
        self.slot_per_symbol = 2 ** (1 + self.bits_per_symbol) + 5 + self.interval_slot

        self.nth_slot = 0  # タイムスロットの番号、1:2**self.fs +5
        self.nth_var = 0
        self.slot_ook = [0] * self.slot_per_symbol

        self.init_symbol()

    def decide_var(self, pattern, start_var, end_var):
        if pattern == "random":
            var = random.randint(start_var, end_var)
        elif pattern == "loop":
            var_list = list(range(start_var, end_var + 1))
            var = var_list[self.l]
            self.nth_var += 1
            if self.nth_var == len(var_list):
                self.nth_var = 0
        elif pattern == "static":
            var = start_var

        # 送信した値varを保存
        # with open('send_data.csv', 'a') as f:
        #     print(var, file=f)
        print(var)
        return var

    def init_symbol(self):
        var = self.decide_var("static", 1, 4)
        self.slot_ook = [0] * self.slot_per_symbol
        on = [0, var + 1, 2 ** (1 + self.bits_per_symbol) + 3 - var, 2 ** (1 + self.bits_per_symbol) + 4]
        for i in on:
            self.slot_ook[i] = 1

    def work(self, input_items, output_items):
        if len(output_items[0]) >= self.slot_width * self.slot_per_buffer:
            if self.nth_slot == 0:
                self.init_symbol()
                send_slot = self.slot_ook[:self.slot_per_buffer]
            elif self.nth_slot + self.slot_per_buffer > self.slot_per_symbol:
                temp = self.slot_ook[self.nth_slot:]
                self.init_symbol()
                send_slot = temp + self.slot_ook[:(self.nth_slot + self.slot_per_buffer) % self.slot_per_symbol]
            elif self.nth_slot + self.slot_per_buffer <= self.slot_per_symbol:
                send_slot = self.slot_ook[self.nth_slot: self.nth_slot + self.slot_per_buffer]
            output_items[0][:self.slot_width * self.slot_per_buffer] = np.repeat(send_slot, self.slot_width)
            print(send_slot)

            # flagを進める
            self.nth_slot = (self.nth_slot + self.slot_per_buffer) % self.slot_per_symbol

            return self.slot_width * self.slot_per_buffer
        else:
            return 0
