import numpy as np
from gnuradio import gr
import csv
import random


############################### APCMA Transmitter ############################
class blk(gr.sync_block):
    def __init__(self, B=2, pulse_width=400, slot_width=400, interval_slot=50):
        gr.sync_block.__init__(
            self,
            name='APCMA Modulation',
            in_sig=None,
            out_sig=[np.complex64]
        )

        # pulse_width[sample]   : パルス幅[us]
        # 100                   : 512
        # 200                   : 1024
        # 400                   : 2048
        # 1600                  : 8192
        # 各パラメータの決定
        self.pulse_width = pulse_width  # [sample]
        self.B = B  # [bit/symbol]
        self.slot_width = slot_width  # [sample]
        self.interval_slot = interval_slot  # シンボル間隔のスロット数 [slot]

        self.nslot = 0  # タイムスロットの番号、1:2**self.fs +5
        self.l = 0
        self.init_symbol()  # 最初のシンボルを決定


    def init_symbol(self):
        # 送信する値varを決定(1,ランダム; 2,サイクル; 3,固定)
        # 1,ランダム
        # var = random.randint(1, 2 ** self.B)  # ランダム

        # 2,サイクル
        var_list = list(range(1, 2 ** self.B + 1))
        var = var_list[self.l]
        self.l += 1
        if self.l == 2 ** self.B:
            self.l = 0

        # 3,固定
        # var = 3

        # 送信した値varを保存
        # with open('send_data.csv', 'a') as f:
        #     print(var, file=f)
        self.slot_ook = [0] * (2 ** (1 + self.B) + 5 + self.interval_slot)
        on = [0, var+1, 2 ** (1 + self.B) + 3 - var, 2 ** (1 + self.B) + 4]
        for i in on:
            self.slot_ook[i] = 1
        self.nslot = 0

    def work(self, input_items, output_items):
        if len(output_items[0]) > self.slot_width:
            output_items[0][:] = np.zeros(len(output_items[0]))
            if self.slot_ook[self.nslot] == 1:
                output_items[0][0:self.pulse_width] = 1

            # flagを進める
            self.nslot = self.nslot + 1

            # 1シンボルを送信したあとの処理
            if self.nslot == (2 * (2 ** self.B + 1) + self.interval_slot):
                self.init_symbol()

            return self.slot_width
        else:
            return 0

