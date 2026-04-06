from lightweight import lightweight_encrypt, lightweight_decrypt

msg = "HelloShivansh123"
key = "iotkey123"

cipher = lightweight_encrypt(msg, key)
decrypted = lightweight_decrypt(cipher, key)

print("Original :", msg)
print("Decrypted:", decrypted)
print("Match?   :", msg == decrypted)
