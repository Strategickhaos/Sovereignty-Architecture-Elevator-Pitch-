#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>
#include <linux/uaccess.h>
#include <linux/capability.h>
#include <asm/io.h>

#define SAGCO_DEV_NAME "sagco_cpu"
#define SAGCO_MAGIC 'S'
#define SAGCO_EXEC_BYTECODE _IOW(SAGCO_MAGIC, 1, unsigned long)
#define MAX_BYTECODE_SIZE 1024
#define MAX_STACK_SIZE 16

struct sagco_bytecode_request {
    unsigned int size;
    char __user *data;
};

static long sagco_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    char bytecode[MAX_BYTECODE_SIZE];
    struct sagco_bytecode_request req;
    unsigned long stack[MAX_STACK_SIZE];
    int sp = 0, i = 0;

    if (cmd != SAGCO_EXEC_BYTECODE)
        return -EINVAL;

    if (!capable(CAP_SYS_ADMIN))
        return -EPERM;

    if (copy_from_user(&req, (void __user *)arg, sizeof(req)))
        return -EFAULT;

    if (req.size == 0 || req.size > MAX_BYTECODE_SIZE)
        return -EINVAL;

    if (copy_from_user(bytecode, req.data, req.size))
        return -EFAULT;

    while (i < req.size) {
        unsigned char op = bytecode[i++];
        if (op == 0x00) {
            break;
        } else if (op == 0x01 && i < req.size) {  // PUSH
            if (sp >= MAX_STACK_SIZE) {
                printk(KERN_ERR "SAGCO_CPU: Stack overflow\n");
                return -EOVERFLOW;
            }
            stack[sp++] = bytecode[i++];
        } else if (op == 0x10) {  // ADD
            if (sp < 2) {
                printk(KERN_ERR "SAGCO_CPU: Stack underflow\n");
                return -EINVAL;
            }
            stack[sp - 2] += stack[sp - 1];
            sp--;
        }
    }
    
    if (sp > 0)
        printk(KERN_INFO "SAGCO_CPU: Exec result: %lu\n", stack[0]);
    return 0;
}

static const struct file_operations sagco_fops = {
    .owner = THIS_MODULE,
    .unlocked_ioctl = sagco_ioctl,
};

static struct miscdevice sagco_dev = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = SAGCO_DEV_NAME,
    .fops = &sagco_fops,
    .mode = 0600,
};

static int __init sagco_init(void) {
    int ret = misc_register(&sagco_dev);
    if (ret) printk(KERN_ERR "SAGCO_CPU: Register failed\n");
    else printk(KERN_INFO "SAGCO_CPU: Loaded - Ratio Ex Nihilo\n");
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
