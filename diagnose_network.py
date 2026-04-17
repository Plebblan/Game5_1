#!/usr/bin/env python3
"""
Game03 Network Diagnostics
Helps troubleshoot network connection issues
"""

import socket
import sys
import subprocess
import os
import time


def check_server_running(host='localhost', port=5001):
    """Check if server is running"""
    print(f"\n📡 Checking if server is running on {host}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Server is running on {host}:{port}")
            return True
        else:
            print(f"❌ No server found on {host}:{port}")
            print(f"   Solution: Start server with: python3 network_server_app.py")
            return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False


def check_port_available(port=5001):
    """Check if port is available"""
    print(f"\n🔌 Checking if port {port} is available...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        result = sock.bind(('', port))
        sock.close()
        print(f"✅ Port {port} is available")
        return True
    except OSError as e:
        print(f"❌ Port {port} is not available: {e}")
        print(f"   Solution: Use different port or kill process using it")
        return False
    except Exception as e:
        print(f"❌ Error checking port: {e}")
        return False


def check_hostname(host):
    """Check if hostname is valid"""
    print(f"\n🌐 Checking hostname: {host}...")
    
    try:
        ip = socket.gethostbyname(host)
        print(f"✅ {host} resolves to {ip}")
        return True
    except socket.gaierror:
        print(f"❌ Cannot resolve {host}")
        print(f"   Solution: Use 'localhost' or valid IP address")
        return False
    except Exception as e:
        print(f"❌ Error resolving hostname: {e}")
        return False


def test_connection(host='localhost', port=5001):
    """Test actual connection"""
    print(f"\n🔗 Testing connection to {host}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, port))
        print(f"✅ Successfully connected to {host}:{port}")
        sock.close()
        return True
    except socket.timeout:
        print(f"❌ Connection timeout (server not responding)")
        print(f"   Solution: Make sure server is running")
        return False
    except ConnectionRefusedError:
        print(f"❌ Connection refused (server not running)")
        print(f"   Solution: Run: python3 network_server_app.py")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def check_config():
    """Check game configuration"""
    print(f"\n⚙️  Checking game configuration...")
    
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        if 'ENABLE_MULTIPLAYER = True' in content:
            print("✅ ENABLE_MULTIPLAYER is set to True")
        else:
            print("⚠️  ENABLE_MULTIPLAYER is not set to True")
            print("   Solution: Set ENABLE_MULTIPLAYER = True in main.py")
            return False
        
        if 'localhost' in content or 'SERVER_HOST' in content:
            print("✅ SERVER_HOST configuration found")
        
        return True
    except Exception as e:
        print(f"❌ Error checking config: {e}")
        return False


def check_network_files():
    """Check if network files exist"""
    print(f"\n📁 Checking network files...")
    
    files = [
        'network_protocol.py',
        'network_server.py',
        'network_client.py',
        'network_manager.py',
        'network_config.py',
        'network_server_app.py',
    ]
    
    all_found = True
    for file in files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING!")
            all_found = False
    
    return all_found


def main():
    """Run all diagnostics"""
    print("\n" + "="*50)
    print("Game03 Network Diagnostics")
    print("="*50)
    
    # Change to Game03 directory
    if not os.path.exists('game.py'):
        if os.path.exists('Game03/game.py'):
            os.chdir('Game03')
        else:
            print("❌ game.py not found. Please run from Game03 directory")
            return False
    
    print("\n🔍 Running diagnostic tests...\n")
    
    checks = [
        ("Network files", check_network_files()),
        ("Configuration", check_config()),
        ("Hostname", check_hostname('localhost')),
        ("Port available", check_port_available(5000)),
        ("Server running", check_server_running()),
    ]
    
    print("\n" + "="*50)
    print("DIAGNOSTIC SUMMARY")
    print("="*50)
    
    all_passed = True
    for name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:.<40} {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("="*50)
        print("\n🚀 Ready to play multiplayer!")
        print("\nStart server: python3 network_server_app.py")
        print("Start game:  python3 main.py")
    else:
        print("❌ SOME CHECKS FAILED")
        print("="*50)
        print("\nCommon fixes:")
        print("1. Start server: python3 network_server_app.py")
        print("2. Enable multiplayer: Set ENABLE_MULTIPLAYER = True in main.py")
        print("3. Check network files exist in Game03 directory")
        print("4. Check firewall allows port 5000")
    
    print()
    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
