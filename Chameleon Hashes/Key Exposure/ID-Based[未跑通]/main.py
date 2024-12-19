"""
File: main.py
Author: coperlm
Date Created: 2024-12-3
Resource: Identity-based chameleon hashing and signatures without key exposure
Remark: 
"""
from Crypto.Util.number import *
import random
import hashlib

def getSecretKey(q):  # get SK,x
    x = random.randint(1, q)
    return x
def getPublicKey(g, x, q):  # get PK,h
    y = pow(g, x, q)
    return y

def fast_find_generator(p):
    """快速寻找素数p的最小生成元
    Args:
        p: 大素数
    Returns:
        最小生成元g
    """
    # 预先定义小素数表加速分解
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    # 先分解p-1的小因子
    phi = p - 1
    factors = []
    for prime in small_primes:
        if phi % prime == 0:
            factors.append(prime)
            while phi % prime == 0:
                phi //= prime
    # 如果剩余的phi还很大,只分解到这里
    if phi > 1:
        factors.append(phi)
    # 从小到大尝试候选生成元
    for g in range(2, min(100, p-1)):  # 只尝试前100个数
        is_generator = True
        # 快速判断:如果g是完全平方数就跳过
        if int(g**0.5)**2 == g:
            continue
        # 利用二次互反律快速判断
        if pow(g, 2, p) == 1:
            continue
        # 最后才做完整的生成元检验    
        for factor in factors:
            if pow(g, (p-1)//factor, p) == 1:
                is_generator = False
                break
        if is_generator:
            return g   
    # 如果前100个数都不是生成元,再暴力搜索
    for g in range(100, p):
        is_generator = True
        for factor in factors:
            if pow(g, (p-1)//factor, p) == 1:
                is_generator = False
                break
        if is_generator:
            return g
    return None

#直接调用hashlib库，返回消息的sm3摘要
def SM3( M ):
    H = hashlib.new('sm3')
    H.update(M.encode('utf-8'))
    return int(H.hexdigest(),16)

def init( len ):
    p = getPrime( len )
    g = fast_find_generator(p)
    return p , g

def Hash( h , m , q , ga ):
    return ga*pow(h,SM3(m),q)%q


def calc_c( m1 , a1 , m2 , SK , PK , g , q , h ):
    x = SK ; y = PK
    r2 = ( pow(g,a1,q)*pow(h,SM3(m1)-SM3(m2),q)%q , pow(y,a1,q)*pow(h,x*(SM3(m1)-SM3(m2)),q)%q )
    return r2
    
if __name__ == '__main__':
    p , g = init( 512 )
    SK = getSecretKey(p)
    PK = getPublicKey(g, SK, p)
    I = "111"
    h = SM3(str(PK)+I)
    q = p - 1
    a1 = random.randint(1,q)
    m1 = 'aaa'
    m2 = 'bbb'
    # r2 = ( pow(g,a2,q) , pow(PK,a2,q) )
    r2 = calc_c( m1 , a1 , m2 , SK , PK , g , q , h )
    ga2 , ya2 = r2
    ga1 , ya1 = r1
    print( Hash(h,m1,q,ga1) )
    print( Hash(h,m2,q,ga2) )
    print( Hash(h,m1,q,ga1) == Hash(h,m2,q,ga2) )
    