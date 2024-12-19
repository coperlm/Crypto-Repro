# 扩展欧几里得算法：用于计算模逆
def extended_gcd(a, b):
    """扩展欧几里得算法，计算 a 和 b 的最大公约数，同时返回 x 和 y，满足 ax + by = gcd(a, b)"""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

# 中国剩余定理：求解 x ≡ a1 (mod p) 和 x ≡ a2 (mod q)
def chinese_remainder_theorem(a1, p, a2, q):
    """使用中国剩余定理合并模 p 和模 q 下的解"""
    m1, m2 = p, q
    a = a1 - a2
    g, x, y = extended_gcd(m1, m2)
    if g != 1:
        raise Exception("无解")
    return (a * x * m2 + a2) % (m1 * m2)

# Tonelli-Shanks 算法 (计算模 p 下的平方根)
def tonelli_shanks(a, p):
    """Tonelli-Shanks 算法，求解模 p 下的平方根"""
    assert pow(a, (p - 1) // 2, p) == 1, "a 不是模 p 下的二次剩余"
    
    if a == 0:
        return 0
    
    # 如果 p ≡ 3 (mod 4)，可以直接返回
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    
    # 否则使用 Tonelli-Shanks 算法
    s = 0
    q = p - 1
    while q % 2 == 0:
        s += 1
        q //= 2
    
    # 初始猜测 z，z 是模 p 下的非二次剩余
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1
    
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    
    while t != 0 and t != 1:
        # 找到最小的 i 使得 t^(2^i) ≡ 1 (mod p)
        t2i = t
        i = 0
        for i in range(1, m):
            t2i = pow(t2i, 2, p)
            if t2i == 1:
                break
        
        b = pow(c, 2 ** (m - i - 1), p)
        m = i
        c = b * b % p
        t = t * b * b % p
        r = r * b % p
    
    return r

# 主函数：计算 a 在模 N     = p * q 下的平方根
def calculate_sqrt_mod_n(a, p, q):
    """计算 a 在模 N = pq 下的平方根"""
    # 计算模 p 下的平方根
    root_p = tonelli_shanks(a, p)
    # 计算模 q 下的平方根
    root_q = tonelli_shanks(a, q)
    
    # 使用中国剩余定理合并模 p 和模 q 下的平方根
    return chinese_remainder_theorem(root_p, p, root_q, q)

# 计算模 N = p * q 下的所有二次剩余
def all_quadratic_residues_mod_n(p, q):
    """计算模 N = pq 下的所有二次剩余"""
    # 1. 计算模 p 下的二次剩余
    qr_p = set()
    for x in range(p):
        qr_p.add(pow(x, 2, p))  # 计算 x^2 mod p
    
    # 2. 计算模 q 下的二次剩余
    qr_q = set()
    for y in range(q):
        qr_q.add(pow(y, 2, q))  # 计算 y^2 mod q
    
    # 3. 使用中国剩余定理合并模 p 和模 q 下的二次剩余
    quadratic_residues = set()
    for r_p in qr_p:
        for r_q in qr_q:
            # 对于每一对模 p 和模 q 下的二次剩余，使用中国剩余定理合并
            combined = chinese_remainder_theorem(r_p, p, r_q, q)
            quadratic_residues.add(combined)
    
    return sorted(list(quadratic_residues))


def Gennon_quadratic_remainders( list ):
    for i in range( 2 , 1000 ):
        if i not in list:
            return i

# 欧拉准则：判断一个数是否是模 p 的二次剩余
def is_quadratic_residue(a, p):
    """通过欧拉准则判断一个数 a 是否是模 p 的二次剩余"""
    if a % p == 0:
        return True  # 0 总是二次剩余
    return pow(a, (p - 1) // 2, p) == 1

# 主函数：判断一个数是否是模 N = p * q 下的二次剩余
def is_quadratic_residue_mod_n(a, SK):
    p , q = SK
    """判断一个数 a 是否是模 N = pq 下的二次剩余"""
    # 1. 判断 a 是否是模 p 的二次剩余
    is_residue_p = is_quadratic_residue(a, p)
    
    # 2. 判断 a 是否是模 q 的二次剩余
    is_residue_q = is_quadratic_residue(a, q)
    
    # 3. 如果 a 在模 p 和模 q 下都是二次剩余，则它是模 N = pq 下的二次剩余
    if is_residue_p and is_residue_q:
        return True
    return False

# # 示例使用
# p = 7
# q = 11
# a = 4
# N = p * q

# # 计算平方根
# sqrt_n = calculate_sqrt_mod_n(a, p, q)

# print(f"模 {N} 下，{a} 的平方根是：{sqrt_n}")
