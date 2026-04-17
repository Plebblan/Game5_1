#!/usr/bin/env python3
"""
Test improved network connection
"""

import time
from network_client import NetworkClient
from network_protocol import MessageType

print("="*50)
print("Testing Improved Network Connection")
print("="*50)

# Test connection
print("\n📡 Creating client and attempting connection...")
client = NetworkClient(host='localhost', port=5001)

print("\n⏳ Connecting...")
if client.connect():
    print("✅ Connection successful!")
    
    # Test sending a message
    print("\n📨 Sending test message...")
    msg = client.send_player_move(100, 200, 0, 0, True)
    if msg:
        print("✅ Message sent successfully!")
    else:
        print("❌ Failed to send message")
    
    # Wait a bit and get responses
    print("\n⏳ Waiting for server responses...")
    for i in range(5):
        time.sleep(0.5)
        msg = client.get_message(timeout=0.1)
        if msg:
            print(f"✅ Received: {msg.msg_type.value}")
    
    # Disconnect
    print("\n🔌 Disconnecting...")
    client.disconnect()
    print("✅ Disconnected gracefully")
    print("\n✅ CONNECTION TEST PASSED!")
else:
    print("❌ Connection failed!")
    print("\n❌ CONNECTION TEST FAILED!")
    print("\nMake sure server is running:")
    print("  python3 network_server_app.py")

print("\n" + "="*50)
