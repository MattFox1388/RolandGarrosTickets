#!/usr/bin/env python3
"""
Setup script for Roland Garros Ticket Automation
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_firefox():
    """Check if Firefox is installed"""
    print("Checking for Firefox installation...")
    
    # Common Firefox paths on macOS
    firefox_paths = [
        "/Applications/Firefox.app/Contents/MacOS/firefox",
        "/usr/bin/firefox",
        "/usr/local/bin/firefox"
    ]
    
    for path in firefox_paths:
        if os.path.exists(path):
            print(f"✅ Firefox found at: {path}")
            return True
    
    print("❌ Firefox not found. Please install Firefox from https://www.mozilla.org/firefox/")
    return False

def main():
    """Main setup function"""
    print("🎾 Roland Garros Ticket Automation Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check Firefox
    firefox_ok = check_firefox()
    
    # Install requirements
    requirements_ok = install_requirements()
    
    print("\n" + "=" * 50)
    if firefox_ok and requirements_ok:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Start your VPN (Proton VPN or preferred service)")
        print("2. Run: python roland_garros_automation.py")
        print("3. Manually log in when the browser opens")
        print("4. Wait for automation to start")
    else:
        print("❌ Setup incomplete. Please resolve the issues above.")
        if not firefox_ok:
            print("   - Install Firefox")
        if not requirements_ok:
            print("   - Fix Python package installation")

if __name__ == "__main__":
    main() 