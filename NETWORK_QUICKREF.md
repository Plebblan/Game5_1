"""
    Quick Reference: Game03 Socket Programming
    Fast lookup for common networking tasks
"""

# ============================================================================
# 1. QUICK START
# ============================================================================

# Single-player (offline):
from network_manager import LocalNetworkManager
net = LocalNetworkManager()

# Multiplayer (online):
from network_manager import NetworkManager
net = NetworkManager(is_client=True, host='localhost', port=5000)

if net.connected:
    print("Connected!")


# ============================================================================
# 2. STARTING A SERVER
# ============================================================================

# Terminal:
# python network_server_app.py --host 0.0.0.0 --port 5000 --max-players 4

# In code:
from network_server import NetworkServer
server = NetworkServer(host='0.0.0.0', port=5000, max_players=4)
server.start()
server.stop()


# ============================================================================
# 3. SENDING DATA
# ============================================================================

# Send player movement
net.send_player_state(player)

# Send attack
net.send_player_attack(player, attack_type='slash')

# Send jump
net.send_player_jump(jump_type='single')

# Send dash
net.send_player_dash(direction='right')

# Custom message
from network_protocol import NetworkMessage, MessageType
msg = NetworkMessage(MessageType.PLAYER_ATTACK, {'damage': 50})
net.client.send_message(msg)


# ============================================================================
# 4. RECEIVING DATA
# ============================================================================

# Get remote players
remote_players = net.get_remote_players()
for player_id, player_data in remote_players.items():
    x = player_data['pos_x']
    y = player_data['pos_y']

# Get single player
player_data = net.get_remote_player('player-id-123')

# Get remote enemies
remote_enemies = net.get_remote_enemies()


# ============================================================================
# 5. NETWORK STATUS
# ============================================================================

# Check connection
is_connected = net.is_connected()
is_multiplayer = net.is_multiplayer_enabled()

# Get player count
count = net.get_player_count()

# Get connection info
player_id = net.client.player_id
connected = net.client.is_connected()


# ============================================================================
# 6. MESSAGE PROTOCOL
# ============================================================================

# Message types:
MessageType.CONNECT              # Connection/disconnect
MessageType.PLAYER_MOVE          # Movement update
MessageType.PLAYER_ATTACK        # Attack action
MessageType.PLAYER_JUMP          # Jump action
MessageType.PLAYER_DASH          # Dash action
MessageType.PLAYER_STATE         # Full state sync
MessageType.PLAYER_HEALTH        # Health/MP update
MessageType.ENEMY_MOVE           # Enemy movement
MessageType.ENEMY_ATTACK         # Enemy attack
MessageType.GAME_START           # Game started
MessageType.FULL_STATE           # Complete state from server
MessageType.SYNC_REQUEST         # Request state sync
MessageType.HEARTBEAT            # Keep-alive


# ============================================================================
# 7. CONFIGURATION
# ============================================================================

# Edit network_config.py:
NETWORK_HOST = 'localhost'
NETWORK_PORT = 5000
MAX_PLAYERS = 4
PLAYER_UPDATE_RATE = 0.033       # ~30 updates/sec
LERP_REMOTE_PLAYERS = True       # Smooth movement
DEBUG_NETWORK = False


# ============================================================================
# 8. GAME LOOP INTEGRATION
# ============================================================================

class Game:
    def __init__(self):
        self.net_manager = NetworkManager(is_client=True)
    
    def play(self):
        while self.running:
            delta_time = self.clock.tick(120) / 1000.0
            
            # Update network
            self.net_manager.update(delta_time)
            
            # Send local player state
            self.net_manager.send_player_state(self.player)
            
            # Handle attacks
            if self.player.attacking:
                self.net_manager.send_player_attack(self.player)
            
            # Get remote data
            remote_players = self.net_manager.get_remote_players()


# ============================================================================
# 9. DEBUGGING
# ============================================================================

# Enable debug output
net.enable_debug(True)

# Print statistics
from network_utils import NetworkStatistics
stats = NetworkStatistics()
stats.print_stats()

# Export stats to file
stats.export_stats_json('network_stats.json')

# Simulate latency (testing)
from network_utils import LatencySimulator
latency = LatencySimulator(latency_ms=100)

# Simulate packet loss (testing)
from network_utils import PacketLossSimulator
loss = PacketLossSimulator(loss_rate=0.05)


# ============================================================================
# 10. ERROR HANDLING
# ============================================================================

try:
    net = NetworkManager(is_client=True, host='localhost', port=5000)
    
    if not net.connected:
        print("Connection failed, running offline")
        net = LocalNetworkManager()
    
    # Continue with game...

except Exception as e:
    print(f"Network error: {e}")
    # Fallback to offline mode


# ============================================================================
# 11. COMMON PATTERNS
# ============================================================================

# Pattern 1: Fallback to offline on connection failure
net = NetworkManager(is_client=True) if use_multiplayer else LocalNetworkManager()

# Pattern 2: Conditional networking in game logic
if net.is_multiplayer_enabled():
    net.send_player_state(player)
    remote_players = net.get_remote_players()

# Pattern 3: Handle player disconnection
if not net.is_connected():
    net.disconnect()
    # Show offline warning or reconnect

# Pattern 4: Periodic sync requests
if time.time() - last_sync > 10:  # Every 10 seconds
    net.client.request_full_state()
    last_sync = time.time()


# ============================================================================
# 12. TROUBLESHOOTING
# ============================================================================

# Connection refused
# -> Check server is running
# -> Check port is open
# -> Check firewall settings

# High latency
# -> Check network connection
# -> Reduce update rate
# -> Enable movement prediction (PREDICT_PLAYER_MOVEMENT)

# Disconnections
# -> Enable heartbeat
# -> Increase timeout values
# -> Check for network drops

# Data sync issues
# -> Request full state sync
# -> Verify message format
# -> Check server logs


# ============================================================================
# 13. PERFORMANCE TIPS
# ============================================================================

# 1. Reduce update rate for non-critical data
PLAYER_UPDATE_RATE = 0.05  # 20 updates/sec instead of 30

# 2. Only send changed data (delta updates)
# 3. Use compression for large messages (future)
# 4. Batch multiple updates in single message
# 5. Cache remote player data locally
# 6. Use UDP for time-critical data (future)


# ============================================================================
# 14. FILES REFERENCE
# ============================================================================

# Core files:
# network_protocol.py      - Message serialization
# network_server.py        - Server implementation
# network_client.py        - Client implementation
# network_manager.py       - Game integration
# network_config.py        - Configuration

# Utilities:
# network_utils.py         - Stats, debugging, simulation
# network_server_app.py    - Standalone server

# Documentation:
# NETWORK.md               - Full documentation
# example_network.py       - Code examples
# NETWORK_QUICKREF.md      - This file


# ============================================================================
# 15. API REFERENCE
# ============================================================================

# NetworkManager
net.is_connected()                          # bool
net.is_multiplayer_enabled()                # bool
net.get_player_count()                      # int
net.get_remote_player(player_id)            # dict
net.get_remote_players()                    # dict
net.get_remote_enemies()                    # dict
net.update(delta_time)                      # None
net.send_player_state(player)               # None
net.send_player_attack(player, type)        # None
net.send_player_jump(type)                  # None
net.send_player_dash(direction)             # None
net.disconnect()                            # None
net.enable_debug(enabled)                   # None

# NetworkMessage
NetworkMessage(type, data, player_id)       # Create
msg.to_json()                               # str
msg.to_bytes()                              # bytes
NetworkMessage.from_json(str)               # NetworkMessage
NetworkMessage.from_bytes(bytes)            # (NetworkMessage, bytes)

# NetworkClient
client.connect()                            # bool
client.disconnect()                         # None
client.send_message(message)                # bool
client.get_message(timeout)                 # NetworkMessage
client.send_player_move(...)                # bool
client.send_player_attack(...)              # bool
client.is_connected()                       # bool

# NetworkServer
server.start()                              # None
server.stop()                               # None
server.handle_message(player_id, msg)       # None
server.broadcast_to_all(msg, exclude)       # None
server.send_full_state(player_id)           # None
