from lightweight import encrypt_block, generate_round_keys

def count_bit_diff(a, b):
    diff = 0
    for x, y in zip(a, b):
        diff += bin(x ^ y).count("1")
    return diff

key = "iotkey123"
round_keys = generate_round_keys(key)

block = b"ABCDEFGH"
cipher_base = encrypt_block(block, round_keys)

total_changed = 0

for bit in range(64):

    modified_block = bytearray(block)
    byte_index = bit // 8
    bit_index = bit % 8

    modified_block[byte_index] ^= (1 << bit_index)

    cipher_modified = encrypt_block(bytes(modified_block), round_keys)

    total_changed += count_bit_diff(cipher_base, cipher_modified)

avg_changed = total_changed / 64
avalanche = (avg_changed / 64) * 100

print("Average bits changed:", round(avg_changed, 2))
print("Avalanche %:", round(avalanche, 2))