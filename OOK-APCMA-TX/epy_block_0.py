import numpy as np
from gnuradio import gr
import random


############################### APCMA Transmitter ############################
class ApcmaTransmitter(gr.sync_block):
    def __init__(self, bits_per_symbol=2, slot_width=400, interval_slot=50):
        gr.sync_block.__init__(
            self,
            name='APCMA Modulation',
            in_sig=None,
            out_sig=[np.complex64]
        )

        # 各パラメータの決定
        self.bits_per_symbol = bits_per_symbol  # [bits/symbol]
        self.slot_width = slot_width  # [sample]
        self.interval_slot = interval_slot  # シンボル間隔のスロット数 [slot]
        self.slot_per_symbol = 2 ** (1 + self.bits_per_symbol) + 5 + self.interval_slot

        self.nth_slot = 0  # タイムスロットの番号
        self.nth_var = 0  # varをループにするときのindex

        self.slot_ook = [0] * self.slot_per_symbol  # slotのon-offを表すリスト
        self.init_symbol()  # 最初のシンボルを決定

    def decide_var(self, pattern, start_var, end_var):
        if pattern == "random":
            var = random.randint(start_var, end_var)
        elif pattern == "loop":
            var_list = list(range(start_var, end_var + 1))
            var = var_list[self.nth_var]
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
        self.nth_slot = 0
        var = self.decide_var("loop", 1, 4)
        self.slot_ook = [0] * self.slot_per_symbol
        on = [0, var + 1, self.slot_per_symbol - 2 - var, self.slot_per_symbol - 1]
        for i in on:
            self.slot_ook[i] = 1

    def work(self, input_items, output_items):
        if len(output_items[0]) > self.slot_width:
            output_items[0][:self.slot_width] = np.repeat(self.slot_ook[self.nth_slot], self.slot_width)

            # flagを進める
            self.nth_slot = self.nth_slot + 1

            # 1シンボルを送信したあとの処理
            if self.nth_slot == self.slot_per_symbol:
                self.init_symbol()

            return self.slot_width
        else:
            return 0
