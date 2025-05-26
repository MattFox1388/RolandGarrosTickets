#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
YELLOW='\033[1;33m'

echo -e "${YELLOW}🔧 Setting up virtual environment for Roland Garros Ticket Automation${NC}"
echo "=================================================="

# Check if Python 3.7+ is available
if command -v python3 >/dev/null 2>&1; then
    python_version=$(python3 -c 'import sys; v=sys.version_info; print(f"{v.major}.{v.minor}")')
    major=$(echo $python_version | cut -d. -f1)
    minor=$(echo $python_version | cut -d. -f2)
    
    if [ "$major" -gt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -ge 7 ]); then
        echo -e "${GREEN}✓ Found Python $python_version${NC}"
    else
        echo -e "${RED}✗ Python 3.7+ required, but found $python_version${NC}"
        echo "Please install Python 3.7 or higher"
        exit 1
    fi
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
python -m pip install --upgrade pip

# Install requirements
echo -e "\n${YELLOW}Installing requirements...${NC}"
pip install -r requirements.txt

echo -e "\n${GREEN}✓ Virtual environment setup complete!${NC}"
echo -e "\n${YELLOW}To activate the virtual environment:${NC}"
echo "source venv/bin/activate"
echo -e "\n${YELLOW}To run the automation script:${NC}"
echo "python roland_garros_automation.py"
echo -e "\n${YELLOW}To deactivate the virtual environment when done:${NC}"
echo "deactivate" 