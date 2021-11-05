import numpy as np
from gnuradio import gr


class ApcmaDecode(gr.sync_block):
    def __init__(self, B=2):
        gr.sync_block.__init__(
            self,
            name='Decoding APCMA',
            in_sig=[np.float32],
            out_sig=None
        )

        # 復号するために参照するパルス列の作成
        self.B = B  # [bits/symbol]
        self.number_of_slot = 2 ** (self.B + 1) + 5
        self.ApcmaCode = [[0] * self.number_of_slot for i in range(2 ** self.B)]
        for i in range(2 ** self.B):
            self.ApcmaCode[i][0] = 1
            self.ApcmaCode[i][i + 2] = 1
            self.ApcmaCode[i][- i - 3] = 1
            self.ApcmaCode[i][-1] = 1

        self.PulseList = np.zeros(self.number_of_slot)  # 入力されたパルス列のリスト

    def work(self, input_items, output_items):
        for i in range(len(input_items[0][:])):
            self.PulseList = np.append(self.PulseList[1:], input_items[0][i])
            print(self.PulseList)
            for j in range(len(self.ApcmaCode)):
                if np.all(np.logical_and(self.PulseList, self.ApcmaCode[j]) == self.ApcmaCode[j]):
                    print(f'Word:{j+1}')
                    # with open('C:\\Users\\Atsushi.N\\Desktop\\Output.txt', 'a') as f:
                    #     f.write(j+1)
        return 0
