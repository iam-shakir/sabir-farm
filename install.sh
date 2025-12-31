#!/bin/bash

# Installation script for Egg Farm Management System
# This script sets up the environment and installs dependencies

echo "================================"
echo "Egg Farm Management System Setup"
echo "================================"
echo

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo
echo "Installing dependencies..."
pip install -r requirements.txt

echo
echo "================================"
echo "Setup Complete!"
echo "================================"
echo
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: python egg_farm_system/app.py"
echo
echo "To build EXE for Windows:"
echo "  1. pip install pyinstaller"
echo "  2. pyinstaller --onefile --windowed egg_farm_system/app.py"
echo
