import random
from hashlib import sha256

# 假设 p 和 q 是已知的安全素数，g 是 Q_p 的生成元
p = 23  # 示例素数
q = 11  # 示例素数
g = 5   # 示例生成元

# 密钥生成
def key_generation():
    x = random.randint(1, q-1)
    y = pow(g, x, p)
    return (x, y)

# 哈希函数
def hash_function(m, r):
    return int(sha256((m + str(r)).encode()).hexdigest(), 16) % q

# 哈希方案
def hash_scheme(m, r, s, y):
    e = hash_function(m, r)
    return (r - (pow(y, e, p) * pow(g, s, p)) % p) % q

# 碰撞寻找
def find_collision(C, m, y, x):
    k_prime = random.randint(1, q-1)
    r_prime = (C + pow(g, k_prime, p)) % q
    e_prime = hash_function(m, r_prime)
    s_prime = (k_prime - e_prime * x) % q
    return (m, r_prime, s_prime)

# 示例
x, y = key_generation()
m = "message"
r = random.randint(1, q-1)
s = random.randint(1, q-1)
C = hash_scheme(m, r, s, y)

# 寻找碰撞
m_prime, r_prime, s_prime = find_collision(C, m, y, x)
print("Collision found:", m_prime, r_prime, s_prime)

import random

# 假设 p, q, g, x, y 已经定义，如前一个示例

# 验证哈希方案
def verify_hash_scheme(m, r, s, y, e, C):
    # 计算哈希值 e
    calculated_e = hash_function(m, r)
    # 计算哈希值 C
    calculated_C = (r - (pow(y, calculated_e, p) * pow(g, s, p)) % p) % q
    return calculated_e == e and calculated_C == C

# 验证碰撞
def verify_collision(C, m_prime, r_prime, s_prime, y, x):
    # 计算新的哈希值 e'
    e_prime = hash_function(m_prime, r_prime)
    # 计算新的哈希值 C'
    C_prime = (r_prime - (pow(y, e_prime, p) * pow(g, s_prime, p)) % p) % q
    return C_prime == C

# 示例验证
m = "message"
r = random.randint(1, q-1)
s = random.randint(1, q-1)
e = hash_function(m, r)
C = hash_scheme(m, r, s, y)

# 验证哈希方案是否正确
is_hash_correct = verify_hash_scheme(m, r, s, y, e, C)
print("Hash scheme is correct:", is_hash_correct)

# 寻找碰撞并验证
m_prime, r_prime, s_prime = find_collision(C, m, y, x)
is_collision_correct = verify_collision(C, m_prime, r_prime, s_prime, y, x)
print("Collision is correct:", is_collision_correct)