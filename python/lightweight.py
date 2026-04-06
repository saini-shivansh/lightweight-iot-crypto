# ================================
# Lightweight 64-bit SPN Cipher
# ================================

# 4-bit S-box
SBOX = [
    0xC, 0x5, 0x6, 0xB,
    0x9, 0x0, 0xA, 0xD,
    0x3, 0xE, 0xF, 0x8,
    0x4, 0x7, 0x1, 0x2
]

# Generate inverse S-box
INV_SBOX = [0]*16
for i in range(16):
    INV_SBOX[SBOX[i]] = i


# Stronger Permutation Box
PBOX = [
     0, 16, 32, 48,  1, 17, 33, 49,
     2, 18, 34, 50,  3, 19, 35, 51,
     4, 20, 36, 52,  5, 21, 37, 53,
     6, 22, 38, 54,  7, 23, 39, 55,
     8, 24, 40, 56,  9, 25, 41, 57,
    10, 26, 42, 58, 11, 27, 43, 59,
    12, 28, 44, 60, 13, 29, 45, 61,
    14, 30, 46, 62, 15, 31, 47, 63
]

INV_PBOX = [0]*64
for i in range(64):
    INV_PBOX[PBOX[i]] = i


# -------------------------------
# Core Transformations
# -------------------------------

def substitute(state):
    output = 0
    for i in range(16):
        nibble = (state >> (i*4)) & 0xF
        output |= SBOX[nibble] << (i*4)
    return output


def inverse_substitute(state):
    output = 0
    for i in range(16):
        nibble = (state >> (i*4)) & 0xF
        output |= INV_SBOX[nibble] << (i*4)
    return output


def permute(state):
    output = 0
    for i in range(64):
        bit = (state >> i) & 1
        output |= bit << PBOX[i]
    return output


def inverse_permute(state):
    output = 0
    for i in range(64):
        bit = (state >> i) & 1
        output |= bit << INV_PBOX[i]
    return output


# -------------------------------
# NEW Mixing Layer (Diffusion Boost)
# -------------------------------

def mix_columns(state):
    w0 = (state >> 48) & 0xFFFF
    w1 = (state >> 32) & 0xFFFF
    w2 = (state >> 16) & 0xFFFF
    w3 = state & 0xFFFF

    w0 ^= ((w1 << 3) | (w1 >> 13)) & 0xFFFF
    w1 ^= ((w2 << 5) | (w2 >> 11)) & 0xFFFF
    w2 ^= ((w3 << 7) | (w3 >> 9)) & 0xFFFF
    w3 ^= ((w0 << 11) | (w0 >> 5)) & 0xFFFF

    return (w0 << 48) | (w1 << 32) | (w2 << 16) | w3


def inverse_mix_columns(state):
    w0 = (state >> 48) & 0xFFFF
    w1 = (state >> 32) & 0xFFFF
    w2 = (state >> 16) & 0xFFFF
    w3 = state & 0xFFFF

    w3 ^= ((w0 << 11) | (w0 >> 5)) & 0xFFFF
    w2 ^= ((w3 << 7) | (w3 >> 9)) & 0xFFFF
    w1 ^= ((w2 << 5) | (w2 >> 11)) & 0xFFFF
    w0 ^= ((w1 << 3) | (w1 >> 13)) & 0xFFFF

    return (w0 << 48) | (w1 << 32) | (w2 << 16) | w3


# -------------------------------
# Key Schedule (128-bit key)
# -------------------------------

def generate_round_keys(key):
    key_bytes = key.encode().ljust(16)[:16]
    key_int = int.from_bytes(key_bytes, 'big')

    round_keys = []

    for round in range(10):
        round_keys.append((key_int >> 64) & 0xFFFFFFFFFFFFFFFF)

        key_int = ((key_int << 13) | (key_int >> (128 - 13))) & ((1 << 128) - 1)

        left_nibble = (key_int >> 124) & 0xF
        key_int &= ~(0xF << 124)
        key_int |= SBOX[left_nibble] << 124

        key_int ^= round << 62

    return round_keys


# -------------------------------
# Block Encryption / Decryption
# -------------------------------

def encrypt_block(block, round_keys):
    state = int.from_bytes(block, 'big')

    for i in range(9):
        state ^= round_keys[i]
        state = substitute(state)
        state = permute(state)
        state = mix_columns(state)

    state ^= round_keys[9]

    return state.to_bytes(8, 'big')


def decrypt_block(block, round_keys):
    state = int.from_bytes(block, 'big')

    state ^= round_keys[9]

    for i in reversed(range(9)):
        state = inverse_mix_columns(state)
        state = inverse_permute(state)
        state = inverse_substitute(state)
        state ^= round_keys[i]

    return state.to_bytes(8, 'big')


# -------------------------------
# Public Encrypt / Decrypt API
# -------------------------------

def lightweight_encrypt(data, key):
    round_keys = generate_round_keys(key)
    data = data.encode()

    while len(data) % 8 != 0:
        data += b'\x00'

    ciphertext = b''

    for i in range(0, len(data), 8):
        block = data[i:i+8]
        ciphertext += encrypt_block(block, round_keys)

    return ciphertext


def lightweight_decrypt(ciphertext, key):
    round_keys = generate_round_keys(key)
    plaintext = b''

    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        plaintext += decrypt_block(block, round_keys)

    return plaintext.rstrip(b'\x00').decode()