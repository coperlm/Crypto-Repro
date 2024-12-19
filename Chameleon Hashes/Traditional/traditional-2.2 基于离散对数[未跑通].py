"""
File: traditional-2.2 基于离散对数.py
Author: coperlm
Date Created: 2024-11-24
Resource: Chameleon Hashing and Signatures - 2.2
Remark: 
"""
import random
from sympy import isprime, mod_inverse

# 1. 初始化参数
def setup():
    while True:
        q = random.randint(2**8, 2**10)  # 选择一个较大的素数 q
        if isprime(q):
            break
    while True:
        k = random.randint(2, 100)  # 选择一个随机整数 k
        p = k * q + 1
        if isprime(p):  # 确保 p 是素数
            break
    g = 2  # 通常选择 g 为较小值，确保 g 是模 p 的生成元
    while pow(g, q, p) == 1:  # 确保 g 是模 p 的 q 阶元
        g += 1
    x = random.randint(1, q - 1)  # 私钥 x
    y = pow(g, x, p)  # 公钥 y
    return p, q, g, x, y

# 2. 变色龙哈希函数
def chameleon_hash(p, q, g, y, m, r):
    return (pow(g, m, p) * pow(y, r, p)) % p

# 3. 生成碰撞
def generate_collision(p, q, x, m, r, m_prime):
    # 求解新的随机值 r'
    diff = (m - m_prime) % q
    r_prime = (r - (diff * mod_inverse(x, q)) % q) % q  # 修正公式
    return r_prime

# 示例运行
if __name__ == "__main__":
    # 设置参数
    p, q, g, x, y = setup()
    print(f"Public Parameters: p={p}, q={q}, g={g}, y={y}")
    print(f"Private Key: x={x}")
    
    # 随机生成消息和随机数
    m = random.randint(1, q - 1)
    r = random.randint(1, q - 1)
    print(f"Original Message: m={m}, r={r}")
    
    # 计算哈希值
    h = chameleon_hash(p, q, g, y, m, r)
    print(f"Chameleon Hash: h={h}")
    
    # 生成碰撞
    m_prime = random.randint(1, q - 1)  # 新消息
    r_prime = generate_collision(p, q, x, m, r, m_prime)
    print(f"Collision: New Message m'={m_prime}, r'={r_prime}")
    
    # 验证碰撞
    h_prime = chameleon_hash(p, q, g, y, m_prime, r_prime)
    print(f"Hash for New Message: h'={h_prime}")
    print(f"Collision Successful: {h == h_prime}")
