// hv_api.h – C ABI boundary between FlameLang and Rust KVM core

#ifndef SAGCO_HV_API_H
#define SAGCO_HV_API_H

#ifdef __cplusplus
extern "C" {
#endif

// Simple error codes (expand later)
typedef enum {
    HV_OK = 0,
    HV_ERR_INIT = 1,
    HV_ERR_CREATE = 2,
    HV_ERR_START = 3,
    HV_ERR_STOP = 4,
    HV_ERR_DESTROY = 5,
    HV_ERR_INVALID = 6
} hv_result_t;

// VM configuration struct
typedef struct {
    const char *name;        // "sagco_live_1"
    const char *disk_path;   // "/isos/sagco-live.iso"
    const char *kernel_path; // "/boot/vmlinuz-sagco" (optional for now)
    const char *cmdline;     // "root=/dev/vda console=ttyS0"
    unsigned int mem_mb;     // 256, 512, 1024...
    unsigned int vcpus;      // 1, 2, 4...
    unsigned int flags;      // reserved for future (networking, etc.)
} hv_vm_config_t;

// Lifecycle
hv_result_t hv_init(void);
hv_result_t hv_shutdown(void);

// VM management
hv_result_t hv_create_vm(const hv_vm_config_t *cfg);
hv_result_t hv_start_vm(const char *name);
hv_result_t hv_stop_vm(const char *name);
hv_result_t hv_destroy_vm(const char *name);

#ifdef __cplusplus
}
#endif

#endif // SAGCO_HV_API_H
