"""
File: main.py
Author: coperlm
Date Created: 2024-12-3
Resource: Chameleon Hashes Without Key Exposure Based on Factoring
Remark: 
"""
from quadratic_remainders_finder import *
from Crypto.Util.number import *
import random
from gmssl import sm3, func

def log_star(x):
    # 先检查 x 是否大于 1，因为 log_star(x) 只对 x > 1 有意义
    if x <= 1:
        raise ValueError("x must be greater than 1")
    count = 0
    while x > 1:
        x = math.log(x)  # 计算 x 的对数
        count += 1  # 迭代次数加 1
    
    return count

def generate_binary_string(length):
    return ''.join(random.choice('01') for _ in range(length))

def GenKey( len ):
    p , q = getPrime( len ) , getPrime( len )
    while p==q:#确保pq不相等
        q = getPrime( len )
    # print( p , q )
    N = p * q
    SK = p , q
    PK = N
    return SK , PK

def sm3_hash(data):
    return sm3.sm3_hash(func.bytes_to_list(data.encode('utf-8')))

def Hash( PK , L , m , r , k ):
    N = PK
    J = int(sm3_hash(L),16)
    b = int(random.choice('02'))-1
    h = b*pow(J,m,N)*pow(r,2**log_star(k),N)%N
    return h

def Collision_Extension( m2 , r2 , k , PK , L ):
    N = PK
    m2 = int(sm3_hash(m2),16)
    print( m2 )
    b = int(random.choice('02'))-1
    if m2 > 2**(log_star(k)-1):
        m3 = m2 - 2**(log_star(k)-1)
        r3 = r2*b % N
    else:
        m3 = 2**(log_star(k)-1) + m2
        r3 = r2//b % N
    judge = (Hash(PK,L,m2,r2,k)==Hash(PK,L,m3,r3,k))
    print( Hash(PK,L,m2,r2,k) , Hash(PK,L,m3,r3,k) )
    return m3 , r3 , judge

if __name__ == '__main__':
    SK , PK = GenKey( 5 )
    k = 10
    L = 'I am a label'
    m1 = generate_binary_string( log_star(k) )
    r1 = random.randint( 1, PK )

    m2 = "痞老板会偷走美味蟹黄包秘方"
    r2 = random.randint( 1, PK )

    print( Collision_Extension(m2,r2,k,PK,L) )





    