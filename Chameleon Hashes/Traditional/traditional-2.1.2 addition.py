import random
from Crypto.Util.number import *
from gmpy2 import gcd, invert, isqrt

# 初始化全局变量
p, q, n = 0, 0, 0

def init():
    global p, q, n
    while True:
        # p 和 q 满足 p ≡ 3 (mod 8), q ≡ 7 (mod 8)
        p = getPrime(512)
        q = getPrime(512)
        if p % 8 == 3 and q % 8 == 7:
            break
    n = p * q
    print(f"Initialized p: {p}, q: {q}, n: {n}")

# 定义 f0 和 f1
def f0(x):
    return pow(x, 2, n)

def f1(x):
    return (4 * pow(x, 2, n)) % n

# 定义 f0 和 f1 的逆
def inv_f0(y):
    y = y % n
    y_div_1 = quadratic_residue_inverse(y)
    print(f"inv_f0: y_div_1 = {y_div_1}")
    return y_div_1

def inv_f1(y):
    y = y % n
    y_div_4 = (y * invert(4, n)) % n
    print(f"inv_f1: y_div_4 = {y_div_4}")
    return quadratic_residue_inverse(y_div_4)

# 计算模 n 的平方根（使用模 p 和模 q 分别计算平方根，再合并）
def quadratic_residue_inverse(y):
    # 验证 y 是否是模 n 的二次剩余
    if pow(y, (p - 1) // 2, p) != 1 or pow(y, (q - 1) // 2, q) != 1:
        raise ValueError(f"y = {y} is not a quadratic residue mod n")

    # 计算模 p 和模 q 的平方根
    root_p = pow(y, (p + 1) // 4, p)
    root_q = pow(y, (q + 1) // 4, q)
    print(f"quadratic_residue_inverse: root_p = {root_p}, root_q = {root_q}")

    # 使用中国剩余定理 (CRT) 合并
    q_inv = invert(q, p)
    result = (root_p + p * ((root_q - root_p) * q_inv % p)) % n
    return result

# 检查值是否为二次剩余
def is_quadratic_residue(y):
    return pow(y, (p - 1) // 2, p) == 1 and pow(y, (q - 1) // 2, q) == 1

if __name__ == '__main__':
    # 初始化参数
    init()

    # 消息 m1 和随机数 r1
    m1 = bytes_to_long(b'flag{Chameleon_Hash_is_good}')
    r1 = random.randint(1, n - 1)

    # 检查 r1 是否为二次剩余
    if not is_quadratic_residue(r1):
        raise ValueError(f"r1 = {r1} is not a quadratic residue mod n")

    print(f"Message m1: {m1}, Random r1: {r1}")

    # 计算 H(m1, r1)
    H = r1
    for bit in bin(m1)[2:]:
        if bit == '1':
            H = f1(H)
        else:
            H = f0(H)
        if not is_quadratic_residue(H):
            raise ValueError(f"H = {H} is not a quadratic residue mod n at bit {bit}")
    print(f"H(m1, r1): {H}")

    # 消息 m2 和随机数 r2
    m2 = bytes_to_long(b'flag{I_agree_with_msg1}')
    r2 = H

    print(f"Message m2: {m2}")

    # 构造 r2，使得 H(m1, r1) = H(m2, r2)
    for bit in reversed(bin(m2)[2:]):
        if bit == '1':
            r2 = inv_f1(r2)
        else:
            r2 = inv_f0(r2)
        if not is_quadratic_residue(r2):
            raise ValueError(f"r2 = {r2} is not a quadratic residue mod n at reversed bit {bit}")
        print(f"Reversed bit {bit}, r2 = {r2}")

    # 验证碰撞：计算 H(m2, r2)
    H2 = r2
    for bit in bin(m2)[2:]:
        if bit == '1':
            H2 = f1(H2)
        else:
            H2 = f0(H2)
    print(f"H(m2, r2): {H2}")

    # 验证碰撞结果
    if H == H2:
        print("Hash collision successful!")
    else:
        print("Hash collision failed!")
