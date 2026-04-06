#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#include "aes.h"

#define ROUNDS 10

uint64_t encrypt_block(uint64_t block, uint64_t round_keys[]);
void generate_round_keys(uint64_t round_keys[], uint8_t key[16]);

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

    struct AES_ctx ctx;
    AES_init_ctx(&ctx, key);

    unsigned long blocks = 100000;

    unsigned long freq_light[256] = {0};
    unsigned long freq_aes[256]   = {0};

    for (unsigned long i = 0; i < blocks; i++) {

        // Lightweight
        uint64_t cipher = encrypt_block(i, round_keys);
        for (int b = 0; b < 8; b++) {
            uint8_t byte = (cipher >> (56 - 8*b)) & 0xFF;
            freq_light[byte]++;
        }

        // AES
        uint8_t aes_block[16] = {0};
        memcpy(aes_block, &i, sizeof(i));
        AES_ECB_encrypt(&ctx, aes_block);

        for (int b = 0; b < 16; b++) {
            freq_aes[aes_block[b]]++;
        }
    }

    double ent_light = calculate_entropy(freq_light, blocks * 8);
    double ent_aes   = calculate_entropy(freq_aes, blocks * 16);

    printf("Lightweight Entropy: %.4f / 8.0\n", ent_light);
    printf("AES Entropy: %.4f / 8.0\n", ent_aes);

    return 0;
}