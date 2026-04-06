#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include <string.h>
#include "aes.h"

#define ROUNDS 10
#define ITERATIONS 200000

// Your cipher
uint64_t encrypt_block(uint64_t block, uint64_t round_keys[]);
void generate_round_keys(uint64_t round_keys[], uint8_t key[16]);

int main() {

    uint8_t key[16] = "iotkey123456789";
    uint64_t round_keys[ROUNDS];
    generate_round_keys(round_keys, key);

    struct AES_ctx ctx;
    AES_init_ctx(&ctx, key);

    uint64_t plaintext = 0x4142434445464748ULL;
    uint64_t result_light = 0;
    uint8_t aes_block[16] = {0};

    // Data sizes (bytes)
    int sizes[] = {8, 64, 256, 1024, 4096};
    int count = 5;

    // Open CSV
    FILE *fp = fopen("../results/data/c_vs_aes.csv", "w");    fprintf(fp, "Data Size,Lightweight Throughput,AES Throughput\n");

    for(int s = 0; s < count; s++) {

        int size = sizes[s];
        int blocks = size / 8;  // your cipher = 8-byte block

        // ===============================
        // Lightweight timing
        // ===============================
        clock_t start = clock();

        for(int i = 0; i < ITERATIONS; i++) {
            for(int b = 0; b < blocks; b++) {
                result_light = encrypt_block(plaintext, round_keys);
            }
        }

        clock_t end = clock();
        double time_light = (double)(end - start) / CLOCKS_PER_SEC;

        // ===============================
        // AES timing
        // ===============================
        clock_t start_aes = clock();

        for(int i = 0; i < ITERATIONS; i++) {
            for(int b = 0; b < blocks; b++) {
                AES_ECB_encrypt(&ctx, aes_block);
            }
        }

        clock_t end_aes = clock();
        double time_aes = (double)(end_aes - start_aes) / CLOCKS_PER_SEC;

        // Throughput calculation
        double total_bytes = (double)(ITERATIONS * size);

        double throughput_light = total_bytes / time_light;
        double throughput_aes = total_bytes / time_aes;

        // Print
        printf("Size: %d bytes\n", size);
        printf("Lightweight: %.2f bytes/sec\n", throughput_light);
        printf("AES: %.2f bytes/sec\n\n", throughput_aes);

        // Save
        fprintf(fp, "%d,%f,%f\n", size, throughput_light, throughput_aes);
    }

    fclose(fp);

    printf("CSV generated: results/data/c_vs_aes.csv\n");

    return 0;
}