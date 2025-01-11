"""
File: main.py
Author: coperlm
Date Created: 2024-12-18
Resource: Chameleon-Hashes with Ephemeral Trapdoors And Applications to Invisible Sanitizable Signatures - 4.2
Remark: 
"""
from MyCode import get_g , SM3
from Crypto.Util.number import *
from gmpy2 import invert
import random
import time


def CParGen( l ):
    p = getPrime( l )
    g = get_g( p )
    crs = getRandomInteger( l )
    return (g,p),crs

def KGen_enc( l , param ):
    g,p = param
    x = getPrime( l )
    y = pow( g , x , p )
    return x , y

def gen_NIZK( g , x , p ):
    h = pow( g , x , p )
    r = random.randint( 1 , p )
    t = pow( g , r , p )
    c = SM3("窝丝一个挑战")
    z = r+c*x
    return (t,c,z),(g,p,h)

def verf_NIZK( pi ):
    ( t , c , z ) , ( g , p , h ) = pi
    if pow( g , z , p ) == t * pow( h , c , p ) % p:
        return True
    return False

def CKGen( param ):
    g,p = param
    q = p-1
    x = random.randint( 1 , q )
    h = pow( g , x , p )
    sk_enc , pk_enc = KGen_enc( 512 , param )
    pi_pk = gen_NIZK( g , x , p )
    return ((x,sk_enc),(h,pi_pk,pk_enc))

def CHash( param , h , pi_pk , pk_enc , m ):
    g , p = param
    q = p-1
    if h >= p or h <= 0:
        return False
    if verf_NIZK(pi_pk) != True:
        print("nizk false")
        return False
    r = random.randint( 1 , q )
    etd = random.randint( 1 , q )
    h2 = pow( g , etd , p )
    pi_t = gen_NIZK( g , etd , p )
    k = random.randint( 1 , q )
    C = pow( g , k , p ) , r*pow( pk_enc , k , p )
    a = SM3( m )
    pp = pow( h , r , p )
    pi_p = gen_NIZK( h , r , p )
    b = pp*pow( h2 , a , p )
    return ((b,h2,pi_t),(pp,C,pi_p),etd)

def CHashCheck( param , pi_pk , m , tuple1 , tuple2 ):
    pp , C , pi_p = tuple1
    b , h2 , pi_t = tuple2
    g , p = param
    if pp >= p or pp <= 0 or h2 >= p or h2 <= 0:
        return False
    if verf_NIZK(pi_p) != True or verf_NIZK(pi_pk) != True or verf_NIZK(pi_t) != True:
        return False
    a = SM3( m )
    if b == pp*pow( h2 , a , p ):
        return True
    return False

def Adapt( param , C , m , m2 , pp , sk_enc , pk_enc , etd , x , msg_tuple ):
    g , p = param
    q = p-1
    # if CHashCheck( *msg_tuple ) != True:
    #     return False
    c1 , c2 = C
    s = pow( c1 , sk_enc , p )
    r = c2*invert(s,p)%p
    if r >= p or r <= 0:
        return False
    a = SM3( m )
    a2 = SM3( m2 )
    if pp != pow(g,x*r,p):
        return False
    if a == a2:
        return ( pp , C , pi_p )
    r2 = (r*x+a*etd-a2*etd)*invert(x,p)%p
    pp2 = pow( h , r2 , p )
    k2 = random.randint( 1 , q )
    C2 = pow( g , k2 , p ) , r2*pow( pk_enc , k2 , p )
    b = pp2*pow( h2 , a2 , p )
    pi_t2 = gen_NIZK( h , r2 , p )
    return pp2 , C2 , pi_t2 , b , pi_t2

if __name__ == '__main__':
    param , crs = CParGen( 512 )
    (x,sk_enc),(h,pi_pk,pk_enc) = CKGen( param )
    m = "窝药次冰70!"
    time1 = time.time()
    cnt = 1
    while cnt < 10000:
        cnt += 1
        (b,h2,pi_t),(pp,C,pi_p),etd = CHash( param , h , pi_pk , pk_enc , m )
    time2 = time.time()
    msg_tuple1 = (param , pi_pk , m , ( pp , C , pi_p ) , ( b , h2 , pi_t ))
    if CHashCheck( *msg_tuple1 ):
        print("验证成功")
    else:
        print("验证失败")
        assert 0
    m2 = "泥也药次冰70?"
    time3 = time.time()
    cnt = 1
    while cnt < 10000:
        cnt += 1
        pp2 , C2 , pi_p2 , b2 , pi_t2 = Adapt( param , C , m , m2 , pp , sk_enc , pk_enc , etd , x , msg_tuple1 )
    time4 = time.time()
    if CHashCheck( param , pi_pk , m2 , ( pp2 , C2 , pi_p2 ) , ( b2 , h2 , pi_t2 ) ):
        print("碰撞成功")
    else:
        print("碰撞失败")
        assert 0
    print( time2 - time1 , time4 - time3 )
    exit(0)