"""
File: key_exp.py
Author: coperlm
Date Created: 2024-11-26
Resource: Chameleon Hashing Without Key Exposure
Remark: 密钥泄露例程代码
"""
import random
from sympy import mod_inverse

# 生成大质数 p 和生成元 g
p = 1019  # 这里使用小质数为了演示，实际应用中应该使用更大的质数
g = 2  # 生成元

# 模拟消息的哈希函数，假设H(m) = m（简化处理）
def H(m):
    return m % (p-1)

# 生成签名者的私钥和公钥
def generate_keys():
    x = random.randint(1, p-2)  # 私钥 x（随机选择）
    y = pow(g, x, p)  # 公钥 y = g^x % p
    return x, y

# 生成签名
def sign_message(x, m):
    r = random.randint(1, p-2)  # 随机数 r
    s = (r - x * H(m)) % (p-1)  # 计算签名
    return r, s

# 验证签名
def verify_signature(y, m, r, s):
    left = pow(g, s, p) * pow(y, H(m) + r, p) % p
    right = pow(g, r, p)
    return left == right

# 恢复私钥（如果泄露了签名的 r, s 和 m，攻击者可以恢复私钥）
def recover_private_key(r, s, m):
    # 计算 H(m) = m % (p-1)
    Hm = H(m)
    # 使用模逆恢复私钥
    x = mod_inverse(Hm, p-1) * (r - s) % (p-1)
    return x

# 示例演示

# 生成签名者的私钥和公钥
x, y = generate_keys()
print(f"签名者的私钥: {x}")
print(f"签名者的公钥: {y}")

# 签署一个消息
message = 123  # 假设消息是 123
r, s = sign_message(x, message)
print(f"签名: r = {r}, s = {s}")

# 验证签名
is_valid = verify_signature(y, message, r, s)
print(f"签名验证结果: {is_valid}")

# 攻击者伪造签名并恢复私钥
recovered_private_key = recover_private_key(r, s, message)
print(f"恢复的私钥: {recovered_private_key}")

# 验证恢复的私钥是否正确
assert recovered_private_key == x, "恢复的私钥错误"
print("私钥恢复成功，攻击者可以伪造签名！")
