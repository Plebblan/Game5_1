#!/usr/bin/env python3
"""
Test script to verify Game03 multiplayer setup
"""

import os
import sys

def test_imports():
    """Test if all networking modules can be imported"""
    print("=" * 50)
    print("Testing imports...")
    print("=" * 50)
    
    try:
        print("✓ Importing network_protocol...")
        from network_protocol import NetworkMessage, MessageType
        
        print("✓ Importing network_server...")
        from network_server import NetworkServer
        
        print("✓ Importing network_client...")
        from network_client import NetworkClient
        
        print("✓ Importing network_manager...")
        from network_manager import NetworkManager, LocalNetworkManager
        
        print("✓ Importing network_utils...")
        from network_utils import NetworkStatistics
        
        print("✓ Importing network_config...")
        import network_config
        
        print("\n✅ All imports successful!\n")
        return True
    except ImportError as e:
        print(f"\n❌ Import failed: {e}\n")
        return False


def test_protocol():
    """Test message protocol"""
    print("=" * 50)
    print("Testing message protocol...")
    print("=" * 50)
    
    try:
        from network_protocol import NetworkMessage, MessageType
        
        # Test message creation
        msg = NetworkMessage(
            MessageType.PLAYER_ATTACK,
            {'damage': 50, 'attack_type': 'slash'}
        )
        print(f"✓ Created message: {msg.msg_type.value}")
        
        # Test serialization
        json_str = msg.to_json()
        print(f"✓ JSON: {json_str[:80]}...")
        
        # Test deserialization
        msg2 = NetworkMessage.from_json(json_str)
        print(f"✓ Deserialized: {msg2.msg_type.value}")
        
        # Test bytes
        msg_bytes = msg.to_bytes()
        print(f"✓ Converted to bytes: {len(msg_bytes)} bytes")
        
        # Test from bytes
        msg3, remaining = NetworkMessage.from_bytes(msg_bytes)
        print(f"✓ Converted from bytes: {msg3.msg_type.value}")
        
        print("\n✅ Protocol tests passed!\n")
        return True
    except Exception as e:
        print(f"\n❌ Protocol test failed: {e}\n")
        return False


def test_config():
    """Test configuration"""
    print("=" * 50)
    print("Testing configuration...")
    print("=" * 50)
    
    try:
        import network_config
        
        server_config = network_config.get_server_config()
        print(f"✓ Server config: {server_config}")
        
        client_config = network_config.get_client_config()
        print(f"✓ Client config: {client_config}")
        
        rates = network_config.get_update_rates()
        print(f"✓ Update rates: {rates}")
        
        print("\n✅ Configuration tests passed!\n")
        return True
    except Exception as e:
        print(f"\n❌ Config test failed: {e}\n")
        return False


def test_game_integration():
    """Test game integration"""
    print("=" * 50)
    print("Testing game integration...")
    print("=" * 50)
    
    try:
        # Check if game.py has network imports
        with open('game.py', 'r') as f:
            content = f.read()
            
        if 'NetworkManager' in content:
            print("✓ NetworkManager imported in game.py")
        else:
            print("❌ NetworkManager NOT imported in game.py")
            return False
        
        if 'enable_multiplayer' in content:
            print("✓ enable_multiplayer parameter found")
        else:
            print("❌ enable_multiplayer NOT found")
            return False
        
        if '_draw_remote_players' in content:
            print("✓ Remote player rendering found")
        else:
            print("❌ Remote player rendering NOT found")
            return False
        
        # Check main.py
        with open('main.py', 'r') as f:
            main_content = f.read()
        
        if 'ENABLE_MULTIPLAYER' in main_content:
            print("✓ ENABLE_MULTIPLAYER config in main.py")
        else:
            print("❌ ENABLE_MULTIPLAYER NOT in main.py")
            return False
        
        print("\n✅ Game integration tests passed!\n")
        return True
    except Exception as e:
        print(f"\n❌ Game integration test failed: {e}\n")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("Game03 Multiplayer Setup Tests")
    print("=" * 50 + "\n")
    
    # Change to Game03 directory
    if os.path.exists('game.py'):
        pass  # Already in correct directory
    elif os.path.exists('Game03/game.py'):
        os.chdir('Game03')
    else:
        print("❌ game.py not found. Make sure you're in Game03 directory")
        return False
    
    all_passed = True
    
    # Run tests
    all_passed &= test_imports()
    all_passed &= test_protocol()
    all_passed &= test_config()
    all_passed &= test_game_integration()
    
    # Summary
    print("=" * 50)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        print("\n🚀 Ready for multiplayer!")
        print("\nNext steps:")
        print("1. Start server: python3 network_server_app.py")
        print("2. Enable multiplayer in main.py: ENABLE_MULTIPLAYER = True")
        print("3. Run game: python3 main.py")
        print("\nSee MULTIPLAYER_SETUP.md for detailed guide")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        print("=" * 50)
        print("\nPlease check the errors above")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
