# Game03 Network Programming Guide

## Overview

Game03 now includes a complete socket programming system for multiplayer support. This guide explains how to use the networking features.

## Architecture

### Components

1. **network_protocol.py** - Message protocol and serialization
2. **network_server.py** - Game server implementation
3. **network_client.py** - Game client implementation
4. **network_manager.py** - Integration layer with game
5. **network_config.py** - Configuration settings
6. **network_utils.py** - Utilities and debugging
7. **network_server_app.py** - Standalone server application

## Quick Start

### Starting a Server

#### Option 1: Standalone Server

```bash
# Start server on localhost:5000
python network_server_app.py

# Start server on specific host/port
python network_server_app.py --host 0.0.0.0 --port 5001 --max-players 8
```

#### Option 2: Programmatic

```python
from network_server import NetworkServer

server = NetworkServer(host='localhost', port=5000, max_players=4)
server.start()

# Server runs in background thread
# To stop:
server.stop()
```

### Connecting as Client

```python
from network_manager import NetworkManager

# Create network manager
net_manager = NetworkManager(is_client=True, host='localhost', port=5000)

# Check connection
if net_manager.connected:
    print("Connected to server!")

# In game loop:
net_manager.update(delta_time)

# Send player state
net_manager.send_player_state(player)

# Receive updates
remote_players = net_manager.get_remote_players()
```

### Offline Mode

For single-player, use LocalNetworkManager:

```python
from network_manager import LocalNetworkManager

net_manager = LocalNetworkManager()
# No networking, game runs offline
```

## Message Types

### Connection Messages
- `CONNECT` - Client connects to server
- `DISCONNECT` - Player disconnects
- `HEARTBEAT` - Keep-alive ping

### Player Messages
- `PLAYER_MOVE` - Movement and velocity
- `PLAYER_ATTACK` - Attack action
- `PLAYER_JUMP` - Jump action
- `PLAYER_DASH` - Dash action
- `PLAYER_STATE` - Full state sync
- `PLAYER_HEALTH` - Health/MP update
- `PLAYER_SPAWN` - Spawn notification
- `PLAYER_DIE` - Death notification

### Enemy Messages
- `ENEMY_MOVE` - Enemy movement
- `ENEMY_ATTACK` - Enemy attack
- `ENEMY_SPAWN` - Enemy spawned
- `ENEMY_DIE` - Enemy died

### Game Messages
- `GAME_START` - Game started
- `GAME_PAUSE` - Game paused
- `GAME_RESUME` - Game resumed
- `GAME_END` - Game ended
- `SYNC_REQUEST` - Request full state
- `FULL_STATE` - Complete game state
- `ERROR` - Error message

## Integration with Game Loop

### Basic Integration

```python
class Game:
    def __init__(self):
        # ... existing code ...
        
        # Initialize network manager
        self.network_manager = NetworkManager(
            is_client=True,
            host='localhost',
            port=5000
        )
    
    def play(self):
        """Main game loop"""
        while self.running:
            delta_time = self._clock.tick(FPS) / 1000.0
            
            # Update network
            self.network_manager.update(delta_time)
            
            # Update game state
            self._update(delta_time)
            self._draw()
    
    def _update(self, delta_time):
        # ... existing update code ...
        
        # Send player state to other players
        self.network_manager.send_player_state(self.player)
        
        # Handle player attacks
        if self.player.is_attacking:
            self.network_manager.send_player_attack(self.player, 'slash')
```

## Network Configuration

Edit `network_config.py` to customize:

```python
# Server settings
NETWORK_HOST = 'localhost'
NETWORK_PORT = 5000
MAX_PLAYERS = 4

# Update rates
PLAYER_UPDATE_RATE = 0.033  # ~30 updates/sec
ENEMY_UPDATE_RATE = 0.05
PROJECTILE_UPDATE_RATE = 0.016

# Features
ENABLE_ANTI_CHEAT = True
PREDICT_PLAYER_MOVEMENT = True
LERP_REMOTE_PLAYERS = True
```

## Debugging

### Enable Debug Mode

```python
net_manager.enable_debug(True)
```

### View Network Statistics

```python
from network_utils import NetworkStatistics

stats = NetworkStatistics()
stats.print_stats()  # Print to console

# Or get stats dict
stats_dict = stats.get_stats()
print(f"Latency: {stats_dict['avg_latency_ms']}ms")
```

### Simulate Network Conditions

```python
from network_utils import LatencySimulator, PacketLossSimulator

# Simulate 100ms latency
latency = LatencySimulator(latency_ms=100)

# Simulate 5% packet loss
loss = PacketLossSimulator(loss_rate=0.05)
```

## Message Flow Examples

### Player Movement

```
Local Client              Server              Remote Client
    |                        |                      |
    |--PLAYER_MOVE---------->|                      |
    |                        |--PLAYER_MOVE-------->|
    |                        |                      |
    |                        |<--PLAYER_MOVE--------|
    |<--PLAYER_MOVE---------|                      |
    |                        |                      |
```

### Player Attack

```
Attacking Client         Server            Defending Client
    |                       |                     |
    |--PLAYER_ATTACK------->|                     |
    |                       |--PLAYER_ATTACK----->|
    |                       |                     |
    |                       |<--PLAYER_HEALTH----|
    |<--PLAYER_HEALTH-------|                     |
```

### Initial Sync

```
New Client              Server
    |                    |
    |--SYNC_REQUEST----->|
    |                    |
    |<--FULL_STATE-------|
    |                    |
```

## Performance Considerations

### Network Bandwidth
- Average player update: ~100 bytes
- At 30 updates/sec per player: ~3 KB/sec
- With 4 players: ~12 KB/sec total

### Latency Compensation
- Enabled by default for smooth gameplay
- `PREDICT_PLAYER_MOVEMENT` = True
- `LERP_REMOTE_PLAYERS` = True
- Adjust `LERP_FACTOR` for smoothness vs responsiveness

### Optimization Tips
1. Reduce update rates for non-critical entities
2. Only send changed data (delta updates)
3. Compress messages if bandwidth is limited
4. Use UDP for time-sensitive data (future)

## Troubleshooting

### Can't Connect to Server

```python
# Check server is running
# Check host/port are correct
net_manager = NetworkManager(host='your_ip', port=5000)
if not net_manager.connected:
    print("Connection failed")
```

### High Latency

- Check network conditions
- Reduce `LERP_FACTOR` for better prediction
- Increase update rate if needed

### Server Crashes

- Check error logs in console
- Verify max players not exceeded
- Check for malformed messages in debug mode

## Advanced Usage

### Custom Message Handling

```python
from network_protocol import NetworkMessage, MessageType

# Send custom message
msg = NetworkMessage(
    MessageType.PLAYER_ATTACK,
    {'attack_type': 'special', 'damage': 50}
)
net_manager.client.send_message(msg)

# Receive custom messages
msg = net_manager.client.get_message()
if msg and msg.msg_type == MessageType.PLAYER_ATTACK:
    print(f"Attack from {msg.player_id}: {msg.data}")
```

### Server State Management

```python
from network_server import NetworkServer

server = NetworkServer(host='0.0.0.0', port=5000)
server.start()

# Access game state
print(server.game_state)

# Broadcast to all players
msg = NetworkMessage(MessageType.GAME_START)
server.broadcast_to_all(msg)
```

## Security Considerations

1. **Input Validation** - Server validates all received data
2. **Anti-Cheat** - Basic validation of player movement
3. **Rate Limiting** - Future: implement message rate limiting
4. **Authentication** - Future: add player authentication

## Future Enhancements

- [ ] UDP for lower latency
- [ ] Message compression
- [ ] Player authentication
- [ ] Game recording/replay
- [ ] Voice chat integration
- [ ] Spectator mode
- [ ] Ranked matchmaking
- [ ] Lobby system

## References

- Python socket documentation: https://docs.python.org/3/library/socket.html
- JSON protocol: https://www.json.org/
- Network programming best practices: https://en.wikipedia.org/wiki/Client%E2%80%93server_model

## Support

For issues or feature requests, please refer to the Game03 repository.
