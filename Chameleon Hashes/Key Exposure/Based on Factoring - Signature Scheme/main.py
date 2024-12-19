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

def GenKey( len ):
    p , q = getPrime( len ) , getPrime( len )
    while p==q:#确保pq不相等
        q = getPrime( len )
    # print( p , q )
    N = p * q
    SK = p , q
    PK = N
    return SK , PK

def GenHash( SK ):
    p , q = SK
    return all_quadratic_residues_mod_n( p , q )

def Sign( m , SK , Hashed_list ):
    p , q = SK
    hashed = bytes_to_long(m) % (p*q)
    if not is_quadratic_residue_mod_n( hashed , SK ):
        #生成非二次剩余
        S = Gennon_quadratic_remainders(Hashed_list)
        hashed = S * hashed
    return hashed

def Verf( hashed , PK , Hashed_list ):
    N = PK
    if (hashed*hashed)%N in Hashed_list:
        return True
    else:
        return False

if __name__ == '__main__':
    SK , PK = GenKey( 5 )

    Hashed_list = GenHash( SK )
    # print( Hashed_list )
    random.shuffle(Hashed_list)#forge

    m = "痞老板会偷走美味蟹黄包秘方".encode()
    h = Sign( m , SK , Hashed_list )
    print( Verf( h , PK , Hashed_list ) )




    