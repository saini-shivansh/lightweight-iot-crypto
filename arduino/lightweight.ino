

#define ROUNDS 10

// 4-bit S-box
const uint8_t SBOX[16] = {
  0xC, 0x5, 0x6, 0xB,
  0x9, 0x0, 0xA, 0xD,
  0x3, 0xE, 0xF, 0x8,
  0x4, 0x7, 0x1, 0x2
};


// Key Schedule (unchanged)

void generate_round_keys(uint64_t round_keys[], uint8_t key[16]) {

  uint64_t k1 = *((uint64_t*)key);
  uint64_t k2 = *((uint64_t*)(key + 8));

  for (int round = 0; round < ROUNDS; round++) {

    round_keys[round] = k1;

    uint64_t new_hi = (k1 << 13) | (k2 >> (64 - 13));
    uint64_t new_lo = (k2 << 13) | (k1 >> (64 - 13));

    k1 = new_hi;
    k2 = new_lo;

    uint8_t left_nibble = (k1 >> 60) & 0xF;
    k1 &= ~(0xFULL << 60);
    k1 |= ((uint64_t)SBOX[left_nibble] << 60);

    k1 ^= ((uint64_t)round << 46);
  }
}


// Encryption (state as 8 bytes)

void encrypt_block(uint8_t block[8], uint64_t round_keys[]) {

  uint8_t state[8];

  // Copy input
  for (int i = 0; i < 8; i++)
    state[i] = block[i];

  for (int r = 0; r < ROUNDS - 1; r++) {

    // Add round key (byte-wise)
    for (int i = 0; i < 8; i++) {
      state[i] ^= (round_keys[r] >> (56 - 8*i)) & 0xFF;
    }

    // Substitution (nibble-wise)
    for (int i = 0; i < 8; i++) {
      uint8_t high = state[i] >> 4;
      uint8_t low  = state[i] & 0x0F;
      state[i] = (SBOX[high] << 4) | SBOX[low];
    }

    // Simple nibble permutation (4x4 transpose idea)
    uint8_t temp[8];
    temp[0] = state[0];
    temp[1] = state[2];
    temp[2] = state[4];
    temp[3] = state[6];
    temp[4] = state[1];
    temp[5] = state[3];
    temp[6] = state[5];
    temp[7] = state[7];

    for (int i = 0; i < 8; i++)
      state[i] = temp[i];

    // Byte-level mixing
    for (int i = 0; i < 8; i += 2) {
      uint8_t a = state[i];
      uint8_t b = state[i+1];

      state[i]   = a ^ ((b << 3) | (b >> 5));
      state[i+1] = b ^ ((a << 5) | (a >> 3));
    }
  }

  // Final round key
  for (int i = 0; i < 8; i++)
    state[i] ^= (round_keys[ROUNDS - 1] >> (56 - 8*i)) & 0xFF;

  // Copy back
  for (int i = 0; i < 8; i++)
    block[i] = state[i];
}


// Arduino Setup

void setup() {

  Serial.begin(9600);

  uint8_t key[16] = "iotkey123456789";
  uint64_t round_keys[ROUNDS];

  generate_round_keys(round_keys, key);

  // 64-bit block (8 bytes)
  uint8_t block[8] = {'A','B','C','D','E','F','G','H'};

  unsigned long start = micros();

  for (int i = 0; i < 1000; i++) {
    encrypt_block(block, round_keys);
  }

  unsigned long end = micros();

  Serial.print("Time (microseconds): ");
  Serial.println(end - start);

  Serial.print("Cipher: ");
  for (int i = 0; i < 8; i++) {
    if (block[i] < 16) Serial.print("0");
    Serial.print(block[i], HEX);
  }
  Serial.println();
}

void loop() {
}