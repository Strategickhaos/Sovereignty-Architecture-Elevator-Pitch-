#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>
#include <linux/uaccess.h>
#include <asm/io.h>

#define SAGCO_DEV_NAME "sagco_cpu"
#define SAGCO_MAGIC 'S'
#define SAGCO_EXEC_BYTECODE _IOW(SAGCO_MAGIC, 1, unsigned long)

static long sagco_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    char bytecode[1024];
    if (cmd == SAGCO_EXEC_BYTECODE) {
        if (copy_from_user(bytecode, (char __user *)arg, sizeof(bytecode))) return -EFAULT;

        unsigned long stack[16];
        int sp = 0, i = 0;
        while (i < sizeof(bytecode)) {
            unsigned char op = bytecode[i++];
            if (op == 0x01) {  // PUSH
                asm volatile("movb %1, %%al; push %%rax" : : "r"(sp), "m"(bytecode[i++]) : "rax");
                stack[sp++] = bytecode[i++];
            } else if (op == 0x10) {  // ADD
                asm volatile("pop %%rax; pop %%rbx; add %%rbx, %%rax; push %%rax" : : : "rax", "rbx");
                stack[sp - 2] += stack[--sp];
            }
        }
        printk(KERN_INFO "SAGCO_CPU: Exec result: %lu\n", stack[0]);
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
