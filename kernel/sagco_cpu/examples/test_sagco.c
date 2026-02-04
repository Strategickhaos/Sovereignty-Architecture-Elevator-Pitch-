/*
 * SAGCO CPU Test Program
 * 
 * Demonstrates how to use the SAGCO CPU kernel module
 * from userspace.
 * 
 * Entity: Strategickhaos DAO LLC
 * License: GPL v2
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <errno.h>

#define SAGCO_DEV_PATH "/dev/sagco_cpu"
#define SAGCO_MAGIC 'S'

/* Must match kernel module definitions */
struct sagco_bc {
    uint8_t code[1024];
    size_t len;
};

#define SAGCO_EXEC_BYTECODE _IOW(SAGCO_MAGIC, 1, struct sagco_bc)
#define SAGCO_GET_VERSION   _IOR(SAGCO_MAGIC, 2, unsigned long)

/* Opcodes */
#define OP_NOP   0x00
#define OP_PUSH  0x01
#define OP_POP   0x02
#define OP_ADD   0x10
#define OP_SUB   0x11
#define OP_MUL   0x12
#define OP_DIV   0x13
#define OP_HALT  0xFF

void print_usage(const char *prog) {
    printf("Usage: %s [test_number]\n", prog);
    printf("Tests:\n");
    printf("  1 - Get version\n");
    printf("  2 - Simple addition (5 + 3)\n");
    printf("  3 - Multiplication (7 * 6)\n");
    printf("  4 - Complex expression (10 + 5) * 2\n");
    printf("  5 - Division (20 / 4)\n");
}

int test_version(int fd) {
    unsigned long version;
    int ret;

    printf("Test: Get Version\n");
    printf("-----------------\n");
    
    ret = ioctl(fd, SAGCO_GET_VERSION, &version);
    if (ret < 0) {
        perror("ioctl SAGCO_GET_VERSION failed");
        return -1;
    }
    
    printf("Module Version: 0x%06lx (v%ld.%ld.%ld)\n", 
           version,
           (version >> 16) & 0xFF,
           (version >> 8) & 0xFF,
           version & 0xFF);
    printf("✓ Test passed\n\n");
    return 0;
}

int test_addition(int fd) {
    struct sagco_bc bc;
    long result;

    printf("Test: Addition (5 + 3)\n");
    printf("----------------------\n");
    
    /* Bytecode: PUSH 5, PUSH 3, ADD, HALT */
    bc.code[0] = OP_PUSH;
    bc.code[1] = 5;
    bc.code[2] = OP_PUSH;
    bc.code[3] = 3;
    bc.code[4] = OP_ADD;
    bc.code[5] = OP_HALT;
    bc.len = 6;

    printf("Bytecode: [0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x]\n",
           bc.code[0], bc.code[1], bc.code[2], bc.code[3], bc.code[4], bc.code[5]);

    result = ioctl(fd, SAGCO_EXEC_BYTECODE, &bc);
    if (result < 0) {
        perror("ioctl SAGCO_EXEC_BYTECODE failed");
        return -1;
    }
    
    printf("Expected: 8\n");
    printf("Result:   %ld\n", result);
    printf("%s\n\n", result == 8 ? "✓ Test passed" : "✗ Test failed");
    return result == 8 ? 0 : -1;
}

int test_multiplication(int fd) {
    struct sagco_bc bc;
    long result;

    printf("Test: Multiplication (7 * 6)\n");
    printf("----------------------------\n");
    
    /* Bytecode: PUSH 7, PUSH 6, MUL, HALT */
    bc.code[0] = OP_PUSH;
    bc.code[1] = 7;
    bc.code[2] = OP_PUSH;
    bc.code[3] = 6;
    bc.code[4] = OP_MUL;
    bc.code[5] = OP_HALT;
    bc.len = 6;

    result = ioctl(fd, SAGCO_EXEC_BYTECODE, &bc);
    if (result < 0) {
        perror("ioctl SAGCO_EXEC_BYTECODE failed");
        return -1;
    }
    
    printf("Expected: 42\n");
    printf("Result:   %ld\n", result);
    printf("%s\n\n", result == 42 ? "✓ Test passed" : "✗ Test failed");
    return result == 42 ? 0 : -1;
}

int test_complex(int fd) {
    struct sagco_bc bc;
    long result;

    printf("Test: Complex Expression ((10 + 5) * 2)\n");
    printf("----------------------------------------\n");
    
    /* Bytecode: PUSH 10, PUSH 5, ADD, PUSH 2, MUL, HALT */
    bc.code[0] = OP_PUSH;
    bc.code[1] = 10;
    bc.code[2] = OP_PUSH;
    bc.code[3] = 5;
    bc.code[4] = OP_ADD;   /* Now stack has 15 */
    bc.code[5] = OP_PUSH;
    bc.code[6] = 2;
    bc.code[7] = OP_MUL;   /* 15 * 2 = 30 */
    bc.code[8] = OP_HALT;
    bc.len = 9;

    result = ioctl(fd, SAGCO_EXEC_BYTECODE, &bc);
    if (result < 0) {
        perror("ioctl SAGCO_EXEC_BYTECODE failed");
        return -1;
    }
    
    printf("Expected: 30\n");
    printf("Result:   %ld\n", result);
    printf("%s\n\n", result == 30 ? "✓ Test passed" : "✗ Test failed");
    return result == 30 ? 0 : -1;
}

int test_division(int fd) {
    struct sagco_bc bc;
    long result;

    printf("Test: Division (20 / 4)\n");
    printf("-----------------------\n");
    
    /* Bytecode: PUSH 20, PUSH 4, DIV, HALT */
    bc.code[0] = OP_PUSH;
    bc.code[1] = 20;
    bc.code[2] = OP_PUSH;
    bc.code[3] = 4;
    bc.code[4] = OP_DIV;
    bc.code[5] = OP_HALT;
    bc.len = 6;

    result = ioctl(fd, SAGCO_EXEC_BYTECODE, &bc);
    if (result < 0) {
        perror("ioctl SAGCO_EXEC_BYTECODE failed");
        return -1;
    }
    
    printf("Expected: 5\n");
    printf("Result:   %ld\n", result);
    printf("%s\n\n", result == 5 ? "✓ Test passed" : "✗ Test failed");
    return result == 5 ? 0 : -1;
}

int main(int argc, char *argv[]) {
    int fd;
    int test_num = 0;
    int ret = 0;

    printf("========================================\n");
    printf("  SAGCO CPU Kernel Module Test Suite\n");
    printf("  Strategickhaos DAO LLC\n");
    printf("========================================\n\n");

    /* Open device */
    fd = open(SAGCO_DEV_PATH, O_RDWR);
    if (fd < 0) {
        perror("Failed to open " SAGCO_DEV_PATH);
        printf("\nMake sure the kernel module is loaded:\n");
        printf("  sudo insmod sagco_cpu_mod.ko\n");
        return 1;
    }

    printf("✓ Device opened: %s\n\n", SAGCO_DEV_PATH);

    /* Parse arguments */
    if (argc > 1) {
        test_num = atoi(argv[1]);
    }

    /* Run tests */
    if (test_num == 0) {
        /* Run all tests */
        ret |= test_version(fd);
        ret |= test_addition(fd);
        ret |= test_multiplication(fd);
        ret |= test_complex(fd);
        ret |= test_division(fd);
    } else {
        /* Run specific test */
        switch (test_num) {
            case 1: ret = test_version(fd); break;
            case 2: ret = test_addition(fd); break;
            case 3: ret = test_multiplication(fd); break;
            case 4: ret = test_complex(fd); break;
            case 5: ret = test_division(fd); break;
            default:
                print_usage(argv[0]);
                ret = 1;
        }
    }

    close(fd);

    if (ret == 0 && test_num == 0) {
        printf("========================================\n");
        printf("  ALL TESTS PASSED ✓\n");
        printf("========================================\n");
    }

    return ret;
}
