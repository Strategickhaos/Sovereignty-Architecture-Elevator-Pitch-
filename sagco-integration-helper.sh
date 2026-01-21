#!/bin/bash
# SAGCO OS Integration Helper Script
# This script automates the process of integrating SAGCO OS into the Strategickhaos ecosystem

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SAGCO_REPO="git@github.com:Strategickhaos/Strategickhaos-DAO-llc-sagco-os.git"
SAGCO_DIR="Strategickhaos-DAO-llc-sagco-os"
DEFAULT_BRANCH="main"

# Function to print colored messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if git is installed
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git and try again."
        exit 1
    fi
    
    # Check if unzip is installed
    if ! command -v unzip &> /dev/null; then
        print_error "unzip is not installed. Please install unzip and try again."
        exit 1
    fi
    
    # Check SSH connection to GitHub
    print_status "Verifying GitHub SSH connection..."
    if ! ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        print_error "GitHub SSH authentication failed. Please configure your SSH keys."
        exit 1
    fi
    
    print_success "All prerequisites met!"
}

# Function to clone SAGCO OS repository
clone_repository() {
    print_status "Cloning SAGCO OS repository..."
    
    if [ -d "$SAGCO_DIR" ]; then
        print_warning "Directory $SAGCO_DIR already exists."
        read -p "Do you want to remove it and start fresh? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$SAGCO_DIR"
            print_status "Removed existing directory."
        else
            print_error "Cannot proceed with existing directory. Exiting."
            exit 1
        fi
    fi
    
    git clone "$SAGCO_REPO" "$SAGCO_DIR"
    print_success "Repository cloned successfully!"
}

# Function to extract SAGCO OS files
extract_files() {
    local zip_path="$1"
    
    print_status "Extracting SAGCO OS files..."
    
    if [ ! -f "$zip_path" ]; then
        print_error "ZIP file not found: $zip_path"
        exit 1
    fi
    
    # Extract to temporary directory first
    local temp_dir=$(mktemp -d)
    unzip -q "$zip_path" -d "$temp_dir"
    
    # Move contents to SAGCO directory
    # Handle both cases: zip contains a folder or direct files
    local extracted_files=$(find "$temp_dir" -mindepth 1 -maxdepth 1)
    local file_count=$(echo "$extracted_files" | wc -l)
    
    if [ $file_count -eq 1 ] && [ -d "$extracted_files" ]; then
        # Zip contains a single folder
        print_status "Moving files from extracted folder..."
        mv "$extracted_files"/* "$SAGCO_DIR/"
    else
        # Zip contains files directly
        print_status "Moving extracted files..."
        mv "$temp_dir"/* "$SAGCO_DIR/"
    fi
    
    # Cleanup
    rm -rf "$temp_dir"
    print_success "Files extracted successfully!"
}

# Function to commit and push
commit_and_push() {
    print_status "Committing and pushing files..."
    
    cd "$SAGCO_DIR"
    
    # Add all files
    git add -A
    
    # Check if there are changes to commit
    if git diff --cached --quiet; then
        print_warning "No changes to commit."
        cd ..
        return
    fi
    
    # Show what will be committed
    print_status "Files to be committed:"
    git status --short
    
    # Commit
    git commit -m "feat: SAGCO OS v0.1.0 - Initial release

Initial release of SAGCO OS for Strategickhaos ecosystem.

Includes:
- Core OS components
- Integration modules
- Configuration files
- Documentation"
    
    # Push to main branch
    print_status "Pushing to GitHub..."
    git push -u origin "$DEFAULT_BRANCH"
    
    cd ..
    print_success "Files committed and pushed successfully!"
}

# Function to verify integration
verify_integration() {
    print_status "Verifying integration..."
    
    cd "$SAGCO_DIR"
    
    # Check if we're on the correct branch
    local current_branch=$(git branch --show-current)
    if [ "$current_branch" != "$DEFAULT_BRANCH" ]; then
        print_warning "Not on $DEFAULT_BRANCH branch (currently on $current_branch)"
    fi
    
    # Check if there are unpushed commits
    if git log origin/"$DEFAULT_BRANCH".."$DEFAULT_BRANCH" --oneline | grep -q .; then
        print_warning "There are unpushed commits!"
    else
        print_success "All commits are pushed!"
    fi
    
    # Show latest commit
    print_status "Latest commit:"
    git log -1 --oneline
    
    cd ..
    print_success "Integration verified!"
}

# Function to show completion message
show_completion() {
    echo
    print_success "=============================================="
    print_success "SAGCO OS Integration Complete!"
    print_success "=============================================="
    echo
    print_status "Repository: https://github.com/Strategickhaos/Strategickhaos-DAO-llc-sagco-os"
    echo
    print_status "Next steps:"
    echo "  1. Review the files at the repository URL above"
    echo "  2. Configure SAGCO OS for your environment"
    echo "  3. Run tests and validation"
    echo "  4. Deploy to your cluster"
    echo
    print_status "For more information, see:"
    echo "  - SAGCO_OS_INTEGRATION_GUIDE.md"
    echo "  - SAGCO_OS_QUICKSTART.md"
    echo
}

# Main function
main() {
    echo
    echo "======================================"
    echo "   SAGCO OS Integration Helper"
    echo "======================================"
    echo
    
    # Parse command line arguments
    if [ $# -eq 0 ]; then
        print_error "Usage: $0 <path-to-sagco-zip>"
        echo "Example: $0 ~/downloads/sagco-os-v0.1.0-full.zip"
        exit 1
    fi
    
    local zip_path="$1"
    
    # Check if zip file exists
    if [ ! -f "$zip_path" ]; then
        print_error "ZIP file not found: $zip_path"
        exit 1
    fi
    
    # Run integration steps
    check_prerequisites
    clone_repository
    extract_files "$zip_path"
    commit_and_push
    verify_integration
    show_completion
}

# Run main function
main "$@"
