#!/usr/bin/env bash
###############################################################################
# sagco-init.sh
#
# SAGCO-OS Boot Initialization Script
#
# Initializes the Self-Amplifying Generative Cognitive Operating System
# with TRIG6 orchestration, DNA evolution tracking, and telemetry monitoring.
#
# Part of: Self-Amplifying Generative Cognitive Operating System
# DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1-LOM1-TRIG6-WAVE1-HYBRID1-NEURO1-OPS1-BOOT1
#
# Copyright (c) 2026 Strategickhaos DAO LLC
# Inventor: Dom Garza
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SAGCO_ROOT="${SAGCO_ROOT:-/opt/sagco-os}"
LOG_DIR="${SAGCO_LOG_DIR:-/var/log/sagco}"
TELEMETRY_DIR="${TELEMETRY_DIR:-${SAGCO_ROOT}/telemetry}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

# Banner
print_banner() {
    cat << "EOF"
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ███████╗ █████╗  ██████╗  ██████╗ ██████╗        ██████╗ ███████╗      ║
║   ██╔════╝██╔══██╗██╔════╝ ██╔════╝██╔═══██╗      ██╔═══██╗██╔════╝      ║
║   ███████╗███████║██║  ███╗██║     ██║   ██║█████╗██║   ██║███████╗      ║
║   ╚════██║██╔══██║██║   ██║██║     ██║   ██║╚════╝██║   ██║╚════██║      ║
║   ███████║██║  ██║╚██████╔╝╚██████╗╚██████╔╝      ╚██████╔╝███████║      ║
║   ╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝        ╚═════╝ ╚══════╝      ║
║                                                                            ║
║        Self-Amplifying Generative Cognitive Operating System              ║
║                                                                            ║
║        DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-             ║
║             BENCH1-LOM1-TRIG6-WAVE1-HYBRID1-NEURO1-OPS1-BOOT1             ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
EOF
}

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Python
    if ! command -v ${PYTHON_BIN} &> /dev/null; then
        log_error "Python 3 not found. Please install Python 3.8 or later."
        exit 1
    fi
    
    local python_version=$(${PYTHON_BIN} --version 2>&1 | awk '{print $2}')
    log_success "Python ${python_version} found"
    
    # Check required Python modules
    local required_modules=("numpy" "json" "dataclasses")
    for module in "${required_modules[@]}"; do
        if ! ${PYTHON_BIN} -c "import ${module}" 2>/dev/null; then
            log_warning "Python module '${module}' not found (may need installation)"
        fi
    done
    
    # Check for graphviz (optional, for neurograph visualization)
    if command -v dot &> /dev/null; then
        log_success "Graphviz found (neurograph rendering enabled)"
    else
        log_warning "Graphviz not found (neurograph rendering will be limited)"
    fi
}

# Create directory structure
create_directories() {
    log_info "Creating directory structure..."
    
    local dirs=(
        "${SAGCO_ROOT}"
        "${SAGCO_ROOT}/bin"
        "${SAGCO_ROOT}/lib"
        "${SAGCO_ROOT}/config"
        "${LOG_DIR}"
        "${LOG_DIR}/trig6"
        "${LOG_DIR}/telemetry"
        "${TELEMETRY_DIR}"
        "${SAGCO_ROOT}/neurographs"
        "${SAGCO_ROOT}/dna"
    )
    
    for dir in "${dirs[@]}"; do
        if [ ! -d "${dir}" ]; then
            mkdir -p "${dir}"
            log_success "Created directory: ${dir}"
        else
            log_info "Directory exists: ${dir}"
        fi
    done
}

# Initialize DNA strand
initialize_dna() {
    log_info "Initializing DNA evolution tracking..."
    
    if [ -f "${SAGCO_ROOT}/dna_codon_registry.py" ]; then
        ${PYTHON_BIN} "${SAGCO_ROOT}/dna_codon_registry.py" > "${LOG_DIR}/dna_init.log" 2>&1
        
        if [ $? -eq 0 ]; then
            log_success "DNA strand initialized"
            log_info "DNA log: ${LOG_DIR}/dna_init.log"
        else
            log_warning "DNA initialization encountered issues (check logs)"
        fi
    else
        log_warning "DNA codon registry not found, skipping initialization"
    fi
}

# Start TRIG6 system
start_trig6() {
    log_info "Starting TRIG6 trigonometric orchestration system..."
    
    # Run a test orchestration
    if [ -f "${SAGCO_ROOT}/HybridWaveCoreState.py" ]; then
        ${PYTHON_BIN} "${SAGCO_ROOT}/HybridWaveCoreState.py" > "${LOG_DIR}/trig6/trig6_test.log" 2>&1
        
        if [ $? -eq 0 ]; then
            log_success "TRIG6 system operational"
            log_info "TRIG6 log: ${LOG_DIR}/trig6/trig6_test.log"
        else
            log_error "TRIG6 system failed to start (check logs)"
            return 1
        fi
    else
        log_error "TRIG6 core not found: ${SAGCO_ROOT}/HybridWaveCoreState.py"
        return 1
    fi
}

# Generate initial neurograph
generate_neurograph() {
    log_info "Generating initial neurograph visualization..."
    
    if [ -f "${SAGCO_ROOT}/neurograph_builder.py" ]; then
        ${PYTHON_BIN} "${SAGCO_ROOT}/neurograph_builder.py" > "${LOG_DIR}/neurograph_init.log" 2>&1
        
        if [ $? -eq 0 ]; then
            log_success "Neurograph generated"
            
            # Check for output files
            if [ -f "/tmp/neurograph_test_1.dot" ]; then
                cp /tmp/neurograph_test_*.dot "${SAGCO_ROOT}/neurographs/" 2>/dev/null || true
                cp /tmp/neurograph_test_*.json "${SAGCO_ROOT}/neurographs/" 2>/dev/null || true
                log_info "Neurographs saved to: ${SAGCO_ROOT}/neurographs/"
            fi
        else
            log_warning "Neurograph generation encountered issues"
        fi
    else
        log_warning "Neurograph builder not found, skipping"
    fi
}

# Start telemetry monitoring
start_telemetry() {
    log_info "Starting telemetry monitoring services..."
    
    local telemetry_scripts=("netmon" "cpumon" "memmon" "dskmon" "thrm")
    local started=0
    
    for script in "${telemetry_scripts[@]}"; do
        local script_path="${TELEMETRY_DIR}/${script}.sh"
        
        if [ -f "${script_path}" ] && [ -x "${script_path}" ]; then
            # Start telemetry script in background
            nohup "${script_path}" >> "${LOG_DIR}/telemetry/${script}.log" 2>&1 &
            local pid=$!
            echo ${pid} > "${LOG_DIR}/telemetry/${script}.pid"
            log_success "Started ${script} (PID: ${pid})"
            started=$((started + 1))
        else
            log_warning "Telemetry script not found or not executable: ${script_path}"
        fi
    done
    
    if [ ${started} -eq 0 ]; then
        log_warning "No telemetry services started"
    else
        log_success "Started ${started} telemetry service(s)"
    fi
}

# Display system status
display_status() {
    echo ""
    log_info "SAGCO-OS System Status"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Check TRIG6
    if [ -f "${LOG_DIR}/trig6/trig6_test.log" ]; then
        echo -e "  ${GREEN}✓${NC} TRIG6 Orchestration System: OPERATIONAL"
    else
        echo -e "  ${RED}✗${NC} TRIG6 Orchestration System: NOT STARTED"
    fi
    
    # Check DNA
    if [ -f "/tmp/sagco_dna_strand.json" ]; then
        local dna_strand=$(cat /tmp/sagco_dna_strand.json 2>/dev/null | grep -o '"strand":"[^"]*"' | cut -d'"' -f4)
        echo -e "  ${GREEN}✓${NC} DNA Evolution Tracking: ACTIVE"
        echo "    Strand: ${dna_strand:0:60}..."
    else
        echo -e "  ${YELLOW}○${NC} DNA Evolution Tracking: INITIALIZING"
    fi
    
    # Check Neurograph
    if [ -d "${SAGCO_ROOT}/neurographs" ] && [ "$(ls -A ${SAGCO_ROOT}/neurographs 2>/dev/null)" ]; then
        local graph_count=$(ls -1 "${SAGCO_ROOT}/neurographs"/*.dot 2>/dev/null | wc -l)
        echo -e "  ${GREEN}✓${NC} Neurograph Visualization: READY (${graph_count} graphs)"
    else
        echo -e "  ${YELLOW}○${NC} Neurograph Visualization: PENDING"
    fi
    
    # Check Telemetry
    local running_telemetry=$(ls -1 "${LOG_DIR}/telemetry"/*.pid 2>/dev/null | wc -l)
    if [ ${running_telemetry} -gt 0 ]; then
        echo -e "  ${GREEN}✓${NC} Telemetry Monitoring: ${running_telemetry} service(s) running"
    else
        echo -e "  ${YELLOW}○${NC} Telemetry Monitoring: NO SERVICES"
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    log_info "Log directory: ${LOG_DIR}"
    log_info "SAGCO root: ${SAGCO_ROOT}"
    echo ""
}

# Main initialization sequence
main() {
    print_banner
    echo ""
    
    log_info "Initializing SAGCO-OS..."
    echo ""
    
    # Run initialization steps
    check_prerequisites
    echo ""
    
    create_directories
    echo ""
    
    initialize_dna
    echo ""
    
    start_trig6
    echo ""
    
    generate_neurograph
    echo ""
    
    start_telemetry
    echo ""
    
    # Display final status
    display_status
    
    log_success "SAGCO-OS initialization complete!"
    echo ""
    log_info "To view logs: tail -f ${LOG_DIR}/trig6/trig6_test.log"
    log_info "To stop telemetry: kill \$(cat ${LOG_DIR}/telemetry/*.pid)"
    echo ""
}

# Run main
main "$@"
