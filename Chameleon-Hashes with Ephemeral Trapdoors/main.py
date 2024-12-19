"""
File: main.py
Author: coperlm
Date Created: 2024-12-18
Description: 
 - 复现了《Chameleon-Hashes with Ephemeral Trapdoors And Applications to Invisible Sanitizable Signatures》
   一文中4.2第一个构造
 - NIZKPoK部分未完成
"""
from MyCode import get_g , SM3
from Crypto.Util.number import *
from gmpy2 import invert
import random

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
def CKGen( param ):
    g,p = param
    q = p-1
    x = random.randint( 1 , q )
    h = pow( g , x , p )
    sk_enc , pk_enc = KGen_enc( 512 , param )
    return ((x,sk_enc),(h,1,pk_enc))

def CHash( param , h , pi_pk , pk_enc , m ):
    g , p = param
    q = p-1
    if h >= p or h <= 0:
        return False
    if pi_pk != 1:
        return False
    r = random.randint( 1 , q )
    etd = random.randint( 1 , q )
    h2 = pow( g , etd , p )
    pi_t = 1
    k = random.randint( 1 , q )
    C = pow( g , k , p ) , r*pow( pk_enc , k , p )
    a = SM3( m )
    pp = pow( h , r , p )
    pi_p = 1
    b = pp*pow( h2 , a , p )
    return ((b,h2,pi_t),(pp,C,pi_p),etd)

def CHashCheck( param , pi_pk , m , tuple1 , tuple2 ):
    pp , C , pi_p = tuple1
    b , h2 , pi_t = tuple2
    g , p = param
    if pp >= p or pp <= 0 or h2 >= p or h2 <= 0:
        return False
    if pi_p != 1 or pi_pk != 1 or pi_t != 1:
        return False
    a = SM3( m )
    if b == pp*pow( h2 , a , p ):
        return True
    return False

def Adapt( param , C , m , m2 , pp , sk_enc , pk_enc , etd , x ):
    g , p = param
    q = p-1
    if 1 != 1:
        return False
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
        return ( pp , C , 1 )
    r2 = (r*x+a*etd-a2*etd)*invert(x,p)%p
    pp2 = pow( h , r2 , p )
    k2 = random.randint( 1 , q )
    C2 = pow( g , k2 , p ) , r2*pow( pk_enc , k2 , p )
    b = pp2*pow( h2 , a2 , p )
    pi_t2 = 1
    return pp2 , C2 , 1 , b , pi_t2

if __name__ == '__main__':
    param , crs = CParGen( 512 )
    (x,sk_enc),(h,pi_pk,pk_enc) = CKGen( param )
    m = "窝药次冰70!"
    (b,h2,pi_t),(pp,C,pi_p),etd =  CHash( param , h , pi_pk , pk_enc , m )
    if CHashCheck( param , pi_pk , m , ( pp , C , pi_p ) , ( b , h2 , pi_t ) ):
        print("验证成功")
    else:
        print("验证失败")
        assert 0
    m2 = "泥也药次冰70?"
    pp2 , C2 , pi_p2 , b2 , pi_t2 = Adapt( param , C , m , m2 , pp , sk_enc , pk_enc , etd , x )
    if CHashCheck( param , pi_pk , m2 , ( pp2 , C2 , pi_p2 ) , ( b2 , h2 , pi_t2 ) ):
        print("碰撞成功")
    else:
        print("碰撞失败")
        assert 0
    exit(0)