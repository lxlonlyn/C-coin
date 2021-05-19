# -*- coding: utf-8 -*-
import sha1
import random
import struct


# ECDSA签名机制。私匙 160 比特，公匙为点坐标。
class ECDSA:
    # 生成元及模数
    g = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, \
        0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    # 随机数种子
    seed = 8 * 3 ** 179
    MOD = 0xFFFFFFFFFFFFFFFFFFFFFFFF0123456789ABCEA7
    # 定义无穷点，GF 的阶
    INF = (-1, -1)
    order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    def __init__(self):
        ECDSA.seed = (ECDSA.seed * ECDSA.seed) % ECDSA.MOD
        self.private_key, self.public_key = self.gen_pair_keys()

    # ---------------------------------------------------------------------------
    # 数学处理模块
    # ---------------------------------------------------------------------------

    # inv(x) 返回 x 在模 p 意义下的逆元
    def inv(self, input_num, md=p):
        k = md - 2
        res = 1
        tmp = input_num % md
        while k > 0:
            if k % 2 == 1:
                res = res * tmp % md
            tmp = tmp * tmp % md
            k = k // 2
        return res % md

    # 椭圆曲线 y^2 = x^3 + 7 上加法
    def curve_add(self, p1, p2):
        # 如果是 0, 0 直接返回另一个
        if p1 == self.INF:
            return p2
        if p2 == self.INF:
            return p1

        # 相加为 INF 处理
        if p1[0] == p2[0]:
            if (p1[1] + p2[1]) % self.p == 0:
                return self.INF

        # 计算斜率
        if (p1[0] == p2[0]) and (p1[1] == p2[1]):
            k = (3 * p1[0] * p1[0]) % self.p * self.inv(2 * p1[1]) % self.p
        else:
            k = (p2[1] - p1[1] + self.p) % self.p * self.inv((p2[0] - p1[0] + self.p) % self.p) % self.p

        # 计算坐标
        x3 = (k * k + 2 * self.p - p1[0] - p2[0]) % self.p
        y3 = (k * (p1[0] - x3 + self.p) + self.p - p1[1]) % self.p
        return x3, y3

    # 椭圆曲线 y^2 = x^3 + 7 上乘法，基于快速加法实现
    def curve_mul(self, x_in, k):
        r = k
        res = self.INF
        tmp = x_in
        while r > 0:
            if r % 2 == 1:
                res = self.curve_add(res, tmp)
            tmp = self.curve_add(tmp, tmp)
            r = r // 2
        return res

    # ---------------------------------------------------------------------------
    # 私匙公匙处理模块
    # 如果没有特殊声明，输入和返回值都是字符串
    # ---------------------------------------------------------------------------

    # 随机生成私匙，公匙（不推荐，随机产生未压缩私匙，计算得出未压缩公匙）
    def gen_pair_keys(self):
        pri_key = ECDSA.seed ** 2 % self.p
        pub_key = self.curve_mul(self.g, pri_key)
        return pri_key, pub_key

    # 由未压缩私匙生成压缩私匙（wit）
    def get_wit_from_private_key(self, input_str):
        import base58
        from sha256 import my_sha256
        input_str = '80' + input_str + '01'
        h = my_sha256(my_sha256(input_str, True, True), True, True)
        input_str += h[0:8]
        bits = b''
        for i in range(0, len(input_str), 2):
            num = (int(input_str[i], 16) << 4) + (int(input_str[i + 1], 16))
            bits += struct.pack('<B', num)
        return base58.b58encode(bits).decode()

    # 由压缩私匙（wit）生成私匙
    def get_private_key_from_wit(self, input_str):
        import base58
        bits = base58.b58decode(input_str.encode())
        bits = bits[1:-5]
        out_str = ""
        for i in range(32):
            out_str += hex(bits[i] // 16)[2:] + hex(bits[i] % 16)[2:]
        return out_str

    # 由私匙导出公匙，返回未压缩公匙二元组 (x, y)
    def get_public_key_from_private_key(self, private_key, is_compressed=False):
        if private_key[0:2] == "0x":
            private_key = private_key[2:]
        if is_compressed:
            key = int(self.get_private_key_from_wit(private_key), 16)
        else:
            key = int(private_key, 16)
        return self.curve_mul(self.g, key)

    # 由未压缩公匙获得压缩公匙。输入为未压缩公匙二元组 (x, y)
    def get_compressed_public_key_from_public_key(self, public_key):
        x, y = public_key
        compressed_key = ""
        if y % 2 == 0:
            compressed_key += "02"
        else:
            compressed_key += "03"
        num_str = hex(x)[2:]
        return compressed_key + num_str

    # 由压缩公匙生成地址
    def get_addr_from_compressed_public_key(self, ckey):
        import hashlib
        from sha256 import my_sha256
        import base58
        # part 1: 对 33 位压缩公匙 -> sha256 -> ripemd160
        sha = my_sha256(ckey, True, True)
        hash160 = hashlib.new("ripemd160", sha.encode())
        hash160 = hash160.hexdigest()
        hash160 = "00" + hash160
        # part 2: 校验码由 part 1 两次 hash 得到
        verify_code = my_sha256(my_sha256(hash160, True, True), True, True)[:8]
        sum_str = hash160 + verify_code
        bits = b''
        for i in range(0, len(sum_str), 2):
            num = (int(sum_str[i], 16) << 4) + (int(sum_str[i + 1], 16))
            bits += struct.pack('<B', num)
        return base58.b58encode(bits).decode()

    # ---------------------------------------------------------------------------
    # 签名处理模块
    # ---------------------------------------------------------------------------
    '''
        签名是 320 比特，由 (R,S) 表示
        1. 产生 160 比特的随机数 k
        2. 计算 P = k * g
        3. P 的横坐标 x 即为 R
        4. 利用 sha1 计算原信息哈希，得到 160 位整数 z
        5. S = k^(-1) * (z + private_key * R) % p
    '''

    def gen_signature(self, input_str, key):
        k = random.randrange(2 ** 150, 2 ** 160, 1)
        P = self.curve_mul(self.g, k)
        R = P[0]
        z = int(sha1.my_sha1(input_str), 16)
        S = self.inv(k, self.order) * ((z + key * R) % self.order) % self.order
        return R, S

    # 验证:
    '''
        计算 P = S^(-1) * z * g + S^(-1) * R * public_key
        如果 P 的横坐标 x 与 R 相同，则签名有效
    '''

    def verify_signature(self, input_str, key, sign):
        R, S = sign
        z = int(sha1.my_sha1(input_str), 16)
        P = self.curve_add(self.curve_mul(self.g, self.inv(S, self.order) * z),
                           self.curve_mul(key, self.inv(S, self.order) * R))
        if P[0] == R:
            return True
        else:
            return False


if __name__ == "__main__":
    a = ECDSA()
    print(a.private_key)
    wit = "KwdMAjGmerYanjeui5SHS7JkmpZvVipYvB2LJGU1ZxJwYvP98617"
    #print(wit)
    #print(a.public_key)
    #print(a.get_public_key_from_private_key(hex(a.private_key)[2:]))
    #print("{:x}".format(a.get_public_key_from_private_key(wit, True)[0]))
    ckey = a.get_compressed_public_key_from_public_key(a.get_public_key_from_private_key(wit, True))
    print(a.get_compressed_public_key_from_public_key(a.get_public_key_from_private_key(wit, True)))
    print(a.get_addr_from_compressed_public_key(ckey))
    print(a.get_addr_from_compressed_public_key("02d0de0aaeaefad02b8bdc8a01a1b8b11c696bd3d66a2c5f10780d95b7df412345"))