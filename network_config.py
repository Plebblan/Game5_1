"""
    Network Configuration for Game03
    Configure network settings and features
"""

# Server settings
NETWORK_HOST = 'localhost'
NETWORK_PORT = 5001
MAX_PLAYERS = 4

# Client settings
CLIENT_CONNECT_TIMEOUT = 5.0  # seconds
CLIENT_HEARTBEAT_INTERVAL = 5.0  # seconds
CLIENT_MESSAGE_TIMEOUT = 0.01  # seconds

# Network update rates
PLAYER_UPDATE_RATE = 0.033  # ~30 updates per second
ENEMY_UPDATE_RATE = 0.05  # ~20 updates per second
PROJECTILE_UPDATE_RATE = 0.016  # ~60 updates per second

# Features
ENABLE_CHAT = False  # Not yet implemented
ENABLE_VOICE = False  # Not yet implemented
ENABLE_REPLAYS = True  # Save game replays
ENABLE_ANTI_CHEAT = True  # Basic anti-cheat validation

# Buffer sizes
SOCKET_BUFFER_SIZE = 4096
MAX_MESSAGE_SIZE = 65536  # 64KB

# Latency compensation
PREDICT_PLAYER_MOVEMENT = True
LERP_REMOTE_PLAYERS = True  # Smooth out remote player movement
LERP_FACTOR = 0.1  # 0-1, lower = smoother but more lag

# Debug settings
DEBUG_NETWORK = False
DEBUG_MESSAGES = False
DEBUG_LATENCY = False

# Network statistics
COLLECT_STATS = True
STATS_SAMPLE_RATE = 1.0  # seconds


def get_server_config():
    """Get server configuration dictionary"""
    return {
        'host': NETWORK_HOST,
        'port': NETWORK_PORT,
        'max_players': MAX_PLAYERS,
        'enable_anti_cheat': ENABLE_ANTI_CHEAT,
    }


def get_client_config():
    """Get client configuration dictionary"""
    return {
        'host': NETWORK_HOST,
        'port': NETWORK_PORT,
        'connect_timeout': CLIENT_CONNECT_TIMEOUT,
        'heartbeat_interval': CLIENT_HEARTBEAT_INTERVAL,
        'message_timeout': CLIENT_MESSAGE_TIMEOUT,
        'predict_movement': PREDICT_PLAYER_MOVEMENT,
        'lerp_remote_players': LERP_REMOTE_PLAYERS,
        'lerp_factor': LERP_FACTOR,
    }


def get_update_rates():
    """Get network update rates"""
    return {
        'player': PLAYER_UPDATE_RATE,
        'enemy': ENEMY_UPDATE_RATE,
        'projectile': PROJECTILE_UPDATE_RATE,
    }
