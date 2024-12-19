"""
File: traditional-2.1.2基于二次剩余难分解性.py
Author: coperlm
Date Created: 2024-11-20
Resource: Chameleon Hashing and Signatures - 2.1.2
Remark: 基于二次剩余难分解性
"""
from Crypto.Util.number import getPrime, inverse, GCD
from sympy import jacobi_symbol

# Step 1: Generate RSA-like modulus n = p * q
bit_length = 256  # Bit length of primes
p = getPrime(bit_length)
q = getPrime(bit_length)
n = p * q

print(f"p = {p}")
print(f"q = {q}")
print(f"n = {n}")

# Step 2: Verify the quadratic residue condition
def is_quadratic_residue(x, n):
    # Check if x is a quadratic residue modulo n
    return jacobi_symbol(x, n) == 1

# Step 3: Find the square root mod n using the trapdoor (p, q)
def modular_sqrt(y, p, q, n):
    # Compute square root mod p
    r_p = pow(y, (p + 1) // 4, p)
    # Compute square root mod q
    r_q = pow(y, (q + 1) // 4, q)
    # Use Chinese Remainder Theorem to combine results
    m_p = inverse(p, q)
    m_q = inverse(q, p)
    x = (r_p * q * m_q + r_q * p * m_p) % n
    return x

# Step 4: Hashing function
def chameleon_hash(message, r, n):
    hash_value = pow(r, 2, n)
    for m_i in message:
        hash_value = (pow(hash_value, 2, n) * pow(4, m_i, n)) % n
    return hash_value

# Step 5: Collision generation
def generate_collision(original_message, new_message, r, p, q, n):
    # Calculate the original hash
    original_hash = chameleon_hash(original_message, r, n)
    
    # Compute the value needed for the new square root
    new_r_squared = original_hash
    for m_i in new_message:
        new_r_squared = (new_r_squared * pow(4, -m_i, n)) % n
    
    # Calculate the new random value r' using modular square root
    new_r = modular_sqrt(new_r_squared, p, q, n)
    return new_r

# Example usage:
message = [1, 0, 1]  # Original message
new_message = [0, 1, 0]  # New message for collision
r = 42  # Random starting value, must be in Z_n*
while GCD(r, n) != 1:  # Ensure r is coprime with n
    r += 1

# Compute the hash for the original message
original_hash = chameleon_hash(message, r, n)
print(f"Original hash: {original_hash}")

# Generate a collision
new_r = generate_collision(message, new_message, r, p, q, n)
collision_hash = chameleon_hash(new_message, new_r, n)

print(f"New random value (r'): {new_r}")
print(f"Collision hash: {collision_hash}")

# Verify the collision
assert original_hash == collision_hash
print("Collision successfully generated!")
