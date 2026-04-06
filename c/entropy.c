#include <stdio.h>
#include <stdint.h>
#include <math.h>

#define ROUNDS 10

// Functions from lightweight.c
uint64_t encrypt_block(uint64_t block, uint64_t round_keys[]);
void generate_round_keys(uint64_t round_keys[], uint8_t key[16]);

// Shannon entropy calculation
double calculate_entropy(unsigned long freq[], unsigned long total_bytes) {

    double entropy = 0.0;

    for (int i = 0; i < 256; i++) {
        if (freq[i] > 0) {
            double p = (double)freq[i] / total_bytes;
            entropy -= p * log2(p);
        }
    }

    return entropy;
}

int main() {

    uint8_t key[16] = "iotkey123456789";
    uint64_t round_keys[ROUNDS];
    generate_round_keys(round_keys, key);

    unsigned long blocks = 5000;  // Increase for more accuracy
    unsigned long total_bytes = blocks * 8;

    unsigned long freq[256] = {0};

    for (unsigned long i = 0; i < blocks; i++) {

        uint64_t plaintext = i;
        uint64_t cipher = encrypt_block(plaintext, round_keys);

        for (int b = 0; b < 8; b++) {
            uint8_t byte = (cipher >> (56 - 8*b)) & 0xFF;
            freq[byte]++;
        }
    }

    double entropy = calculate_entropy(freq, total_bytes);

    printf("Entropy: %.4f\n", entropy);
    printf("Maximum Possible Entropy: 8.0000\n");

    return 0;
}