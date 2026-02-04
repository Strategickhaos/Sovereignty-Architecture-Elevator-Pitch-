#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>
#include <linux/uaccess.h>

#define SAGCO_DEV_NAME "sagco_cpu"
#define SAGCO_MAGIC 'S'
#define SAGCO_EXEC_BYTECODE _IOW(SAGCO_MAGIC, 1, unsigned long)  // Ioctl for exec
#define MAX_BYTECODE_SIZE 256  // Reduced buffer size to avoid stack pressure

static long sagco_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    char bytecode[MAX_BYTECODE_SIZE];  // Smaller fixed buffer
    unsigned long stack[16];
    int sp = 0;
    int i = 0;
    
    if (cmd == SAGCO_EXEC_BYTECODE) {
        // Clear buffer first
        memset(bytecode, 0, sizeof(bytecode));
        
        if (copy_from_user(bytecode, (char __user *)arg, sizeof(bytecode)))
            return -EFAULT;

        // Interpreter loop - use software stack only (not hardware stack)
        // Terminate on null byte (0x00) or end of buffer
        while (i < sizeof(bytecode) && bytecode[i] != 0x00) {
            unsigned char op = bytecode[i++];
            
            if (op == 0x01) {  // PUSH
                if (sp >= 16) return -EOVERFLOW;
                if (i >= sizeof(bytecode)) return -EINVAL;
                stack[sp++] = bytecode[i++];
            } else if (op == 0x10) {  // ADD
                if (sp < 2) return -EINVAL;
                sp--;
                stack[sp - 1] += stack[sp];
            } else if (op == 0x00) {  // NOP/HALT
                break;
            }
            // Add more ops as needed
        }
        
        printk(KERN_INFO "SAGCO_CPU: Exec result: %lu\n", sp > 0 ? stack[sp-1] : 0);
        return 0;
    }
    return -EINVAL;
}

static const struct file_operations sagco_fops = {
    .owner = THIS_MODULE,
    .unlocked_ioctl = sagco_ioctl,
};

static struct miscdevice sagco_dev = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = SAGCO_DEV_NAME,
    .fops = &sagco_fops,
    .mode = 0666,
};

static int __init sagco_init(void) {
    int ret = misc_register(&sagco_dev);
    if (ret) printk(KERN_ERR "SAGCO_CPU: Device register failed\n");
    else printk(KERN_INFO "SAGCO_CPU: Loaded - Ratio Ex Nihilo (device minor: %d)\n", sagco_dev.minor);
    return ret;
}

static void __exit sagco_exit(void) {
    misc_deregister(&sagco_dev);
    printk(KERN_INFO "SAGCO_CPU: Unloaded\n");
}

module_init(sagco_init);
module_exit(sagco_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Strategickhaos DAO");
MODULE_DESCRIPTION("SAGCO CPU Primitives Module");
