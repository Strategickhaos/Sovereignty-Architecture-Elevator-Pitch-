/*
 * SAGCO CPU Primitives Module
 * Sovereignty Architecture - Kernel-level bytecode interpreter
 * 
 * SAFE IMPLEMENTATION:
 * - Pure C interpreter (no inline assembly - portable across architectures)
 * - Bounds-checked execution (prevents overflow/OOB access)
 * - Structured input via ioctl (no unbounded copy_from_user)
 * - Auto device creation via miscdevice (no manual mknod)
 * - Stack validation on every operation
 * 
 * Author: Strategickhaos DAO
 * License: GPL v2
 * Motto: "Ratio Ex Nihilo" - Reason from Nothing
 */

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>
#include <linux/uaccess.h>
#include <linux/ioctl.h>

#define SAGCO_DEV_NAME "sagco_cpu"
#define SAGCO_MAGIC 'S'
#define SAGCO_EXEC_BYTECODE _IOW(SAGCO_MAGIC, 1, struct sagco_bc)

/* Bytecode structure with fixed size and length field for safety */
struct sagco_bc {
    uint8_t code[1024];
    size_t len;
};

/*
 * SAGCO Bytecode Interpreter
 * Pure C implementation with comprehensive bounds checking
 * 
 * Opcodes:
 *   0x01 - PUSH <byte>: Push value onto stack
 *   0x10 - ADD: Pop two values, push sum
 * 
 * Returns: 0 on success, negative error code on failure
 */
static long sagco_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    struct sagco_bc bc;
    unsigned long stack[16];
    int sp = 0;
    size_t i = 0;

    if (cmd != SAGCO_EXEC_BYTECODE) {
        return -EINVAL;
    }

    /* Safe structured copy from userspace */
    if (copy_from_user(&bc, (void __user *)arg, sizeof(bc))) {
        return -EFAULT;
    }

    /* Validate bytecode length to prevent buffer overrun */
    if (bc.len > sizeof(bc.code)) {
        return -EINVAL;
    }

    /* Execute bytecode with bounds checking on every operation */
    while (i < bc.len) {
        uint8_t op = bc.code[i++];

        switch (op) {
        case 0x01:  /* PUSH */
            /* Check stack overflow and bytecode bounds */
            if (sp >= 16 || i >= bc.len) {
                return -EINVAL;
            }
            stack[sp++] = bc.code[i++];
            break;

        case 0x10:  /* ADD */
            /* Check stack underflow */
            if (sp < 2) {
                return -EINVAL;
            }
            stack[sp - 2] += stack[sp - 1];
            sp--;
            break;

        default:
            /* Unknown opcode */
            return -EINVAL;
        }
    }

    /* Log result to kernel log */
    printk(KERN_INFO "SAGCO_CPU: Exec result = %lu\n", stack[0]);
    return 0;
}

/* File operations for the device */
static const struct file_operations sagco_fops = {
    .owner = THIS_MODULE,
    .unlocked_ioctl = sagco_ioctl,
};

/* Miscdevice structure - auto-creates /dev/sagco_cpu with proper permissions */
static struct miscdevice sagco_dev = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = SAGCO_DEV_NAME,
    .fops = &sagco_fops,
    .mode = 0666,  /* rw-rw-rw- */
};

/*
 * Module initialization
 * Registers the misc device - no need for manual mknod
 */
static int __init sagco_init(void) {
    int ret = misc_register(&sagco_dev);
    if (ret) {
        printk(KERN_ERR "SAGCO_CPU: Register failed\n");
    } else {
        printk(KERN_INFO "SAGCO_CPU: Loaded - Ratio Ex Nihilo\n");
    }
    return ret;
}

/*
 * Module cleanup
 * Unregisters the misc device
 */
static void __exit sagco_exit(void) {
    misc_deregister(&sagco_dev);
    printk(KERN_INFO "SAGCO_CPU: Unloaded\n");
}

module_init(sagco_init);
module_exit(sagco_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Strategickhaos DAO");
MODULE_DESCRIPTION("SAGCO CPU Primitives Module");
