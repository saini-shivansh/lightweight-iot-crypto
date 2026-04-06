#include <stdio.h>
#include <stdint.h>

#define ROUNDS 10

// Functions defined in lightweight.c
uint64_t encrypt_block(uint64_t block, uint64_t round_keys[]);
void generate_round_keys(uint64_t round_keys[], uint8_t key[16]);

int count_bits(uint64_t x) {
    int count = 0;
    while (x) {
        count += x & 1;
        x >>= 1;
    }
    return count;
}

int main() {

    uint8_t key[16] = "iotkey123456789";
    uint64_t round_keys[ROUNDS];

    generate_round_keys(round_keys, key);

    uint64_t base_plain = 0x4142434445464748ULL;
    uint64_t base_cipher = encrypt_block(base_plain, round_keys);

    int total_changed = 0;

    for (int bit = 0; bit < 64; bit++) {

        uint64_t modified_plain = base_plain ^ (1ULL << bit);
        uint64_t modified_cipher = encrypt_block(modified_plain, round_keys);

        uint64_t diff = base_cipher ^ modified_cipher;
        total_changed += count_bits(diff);
    }

    double avg_changed = total_changed / 64.0;
    double avalanche = (avg_changed / 64.0) * 100.0;

    printf("Average bits changed: %.2f\n", avg_changed);
    printf("Avalanche %%: %.2f%%\n", avalanche);

    return 0;
}