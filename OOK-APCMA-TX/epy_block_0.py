import numpy as np
from gnuradio import gr
import csv
import random


############################### APCMA Transmitter ############################
class blk(gr.sync_block):
    def __init__(self, B=2, slot_width=400, interval_slot=50, slot_per_buffer=1):
        gr.sync_block.__init__(
            self,
            name='APCMA Modulation',
            in_sig=None,
            out_sig=[np.complex64]
        )
        
        self.B = B  # [bit/symbol]
        self.slot_width = slot_width  # [sample]
        self.interval_slot = interval_slot  # シンボル間隔のスロット数 [slot]
        self.slot_per_buffer = slot_per_buffer
        self.slot_per_symbol = 2 ** (1 + self.B) + 5 + self.interval_slot
        
        self.nslot = self.slot_per_symbol  # タイムスロットの番号、1:2**self.fs +5
        self.l = 0
        
        

    def decide_var(self, pattern, start_var, end_var):
        if pattern == "random":
            var = random.randint(start_var, end_var)
        elif pattern == "loop":
            var_list = list(range(start_var, end_var + 1))
            var = var_list[self.l]
            self.l += 1
            if self.l == len(var_list):
                self.l = 0
        elif pattern == "static":
            var = start_var

        # 送信した値varを保存
        # with open('send_data.csv', 'a') as f:
        #     print(var, file=f)
        return var
        
        
    def init_symbol(self):
	    var = self.decide_var("loop", 1, 8)
	    self.slot_ook = [0] * self.slot_per_symbol
	    on = [0, var+1, 2 ** (1 + self.B) + 3 - var, 2 ** (1 + self.B) + 4]
	    for i in on:
		    self.slot_ook[i] = 1
	    self.nslot = 0
	    print(self.slot_ook)


    def work(self, input_items, output_items):
        print(self.nslot)
        # 1シンボルを送信したあとの処理
        if self.nslot == self.slot_per_symbol:
            self.init_symbol()
        
        if self.slot_per_buffer > self.slot_per_symbol - self.nslot:
            slot_per_buffer = self.slot_per_symbol - self.nslot
        else:
            slot_per_buffer = self.slot_per_buffer
            
        if len(output_items[0]) >= self.slot_width * slot_per_buffer:
            output_items[0][:self.slot_width * slot_per_buffer] = np.repeat(self.slot_ook[self.nslot:self.nslot+slot_per_buffer], self.slot_width)
            

            # flagを進める
            self.nslot = self.nslot + slot_per_buffer

            return self.slot_width * slot_per_buffer
        else:
            return 0
