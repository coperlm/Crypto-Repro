"""
File: traditional-2.1.1 基于线性方程.py
Author: coperlm
Date Created: 2024-11-21
Resource: Chameleon Hashing and Signatures - 2.1.1
Remark: 
"""
import random
import gmpy2
from Crypto.Util.number import *

a = 0 ; b = 0 ; c = 0 ; d = 0 ; p = 0

def init():
    global a, b, c, d, p
    p = getPrime(512)
    while True:
        a = random.randint(1, 2**512)
        c = random.randint(1, 2**512)
        if gmpy2.gcd(a, p) == 1 and gmpy2.gcd(c, p) == 1:  # 确保 a 和 c 与 p 互质
            break
    b = random.randint(1, 2**512)
    d = random.randint(1, 2**512)

# 线性变换函数
def f1(x):
    return (a * x + b) % p

def f2(x):
    return (c * x + d) % p

# 线性变换逆函数
def inv_f1(y):
    return (y - b) * gmpy2.invert(a, p) % p

def inv_f2(y):
    return (y - d) * gmpy2.invert(c, p) % p

if __name__ == '__main__':
    init()
    m1 = bytes_to_long(b'flag{Chameleon_Hash_is_good}')
    r1 = random.randint( 1 , p - 1 )

    # 计算 H(m1, r1)
    H = r1
    for i in str(bin(m1)[2:]):
        if i == '1':
            H = f1(H)
        else:
            H = f2(H)
    print(f"H(m1, r1): {H}")

    m2 = bytes_to_long(b'flag{I_agree_with_msg1}')

    # 构造新的随机数 r2，使 H(m1, r1) = H(m2, r2)
    r2 = H
    for i in reversed(str(bin(m2)[2:])):  # 逆序推回原随机数
        if i == '1':
            r2 = inv_f1(r2)
        else:
            r2 = inv_f2(r2)
    print(f"Recovered r2: {r2}")

    # 验证碰撞：计算 H(m2, r2)
    H2 = r2
    for i in str(bin(m2)[2:]):
        if i == '1':
            H2 = f1(H2)
        else:
            H2 = f2(H2)
    print(f"H(m2, r2): {H2}")

    # 验证碰撞结果
    if H == H2:
        print("Hash collision successful!")
    else:
        print("Hash collision failed!")
