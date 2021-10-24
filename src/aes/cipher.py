from util.blocks import processMessage, convert_matrix, convert_list
from util.galois import mat_mul, rcon

class Cipher():
    def __init__(self, msg, key):
        self.msg = msg
        self.key = key

        self.s_box = [
            99, 124, 119, 123, 242, 107, 111, 197,  48,   1, 103,  43, 254, 215, 171, 118,
            202, 130, 201, 125, 250,  89,  71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
            183, 253, 147,  38,  54,  63, 247, 204,  52, 165, 229, 241, 113, 216,  49,  21,
            4, 199,  35, 195,  24, 150,   5, 154,   7,  18, 128, 226, 235,  39, 178, 117,
            9, 131,  44,  26,  27, 110,  90, 160,  82,  59, 214, 179,  41, 227,  47, 132,
            83, 209,   0, 237,  32, 252, 177,  91, 106, 203, 190,  57,  74,  76,  88, 207,
            208, 239, 170, 251,  67,  77,  51, 133,  69, 249,   2, 127,  80,  60, 159, 168,
            81, 163,  64, 143, 146, 157,  56, 245, 188, 182, 218,  33,  16, 255, 243, 210,
            205,  12,  19, 236,  95, 151,  68,  23, 196, 167, 126,  61, 100,  93,  25, 115,
            96, 129,  79, 220,  34,  42, 144, 136,  70, 238, 184,  20, 222,  94,  11, 219,
            224,  50,  58,  10,  73,   6,  36,  92, 194, 211, 172,  98, 145, 149, 228, 121,
            231, 200,  55, 109, 141, 213,  78, 169, 108,  86, 244, 234, 101, 122, 174,   8,
            186, 120,  37,  46,  28, 166, 180, 198, 232, 221, 116,  31,  75, 189, 139, 138,
            112,  62, 181, 102,  72,   3, 246,  14,  97,  53,  87, 185, 134, 193,  29, 158,
            225, 248, 152,  17, 105, 217, 142, 148, 155,  30, 135, 233, 206,  85,  40, 223,
            140, 161, 137,  13, 191, 230,  66, 104,  65, 153,  45,  15, 176,  84, 187,  22
        ]

        self.actual_blocks = processMessage(self.msg)
        self.blocks = self.counter(0)

        self.addRoundKey()
        for i in range(10):
            self.expandKey(i)
            self.subBytes()
            self.shiftRows()
            if i != 9:
                self.mixColumns()
            
            self.addRoundKey()

        for i in range(len(self.actual_blocks)):
            for j in range(16):
                self.blocks[i][j] ^= self.actual_blocks[i][j]

    def subBytes(self):
        for block in self.blocks:
            for i in range(len(block)):
                block[i] = self.s_box[block[i]]

    def shiftRows(self):
        for i in range(len(self.blocks)):
            block = convert_matrix(self.blocks[i])
            for x in range(1, len(block)):
                block[x] = block[x][x:] + block[x][:x]

            self.blocks[i] = convert_list(block)

    def mixColumns(self):
        matrix = [
            [2, 3, 1, 1],
            [1, 2, 3, 1],
            [1, 1, 2, 3],
            [3, 1, 1, 2]
        ]

        for block_raw in self.blocks:
            block = convert_matrix(block_raw)
            for column in range(4):
                val = [[block[i][column]] for i in range(4)]
                result = mat_mul(matrix, val)

                for i in range(4):
                    block_raw[i + (column*4)] = result[i][0]

    def addRoundKey(self):
        for block in self.blocks:
            for i in range(len(self.key)):
                block[i] ^= self.key[i]

    def expandKey(self, round):
        column_f = [self.s_box[self.key[i]] for i in range(12, 16)]
        column_f = column_f[1:] + [column_f[0]]
        column_f[0] ^= rcon(round)
        for i in range(4):
            for j in range(4):
                self.key[j + (4*i)] ^= column_f[j]
                column_f[j] = self.key[j + (4*i)]

    def counter(self, nonce):
        nonce <<= 64
        blocks = []
        for i in range(len(self.actual_blocks)):
            block = [0 for _ in range(16)]
            temp = nonce
            for j in range(16):
                block[15-j] = temp&0xff
                temp >>= 8
        
            blocks.append(block)
            nonce += 1
        
        return blocks
