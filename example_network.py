"""
    Example: Multiplayer Game03 Integration
    Shows how to integrate networking into the main game
"""

import pygame
from network_manager import NetworkManager, LocalNetworkManager
from network_utils import NetworkStatistics


class MultiplayerGame:
    """Example game class with networking support"""
    
    def __init__(self, enable_multiplayer=False, server_host='localhost', server_port=5000):
        """
        Initialize game with optional multiplayer
        
        Args:
            enable_multiplayer: Enable network multiplayer
            server_host: Server address
            server_port: Server port
        """
        self.enable_multiplayer = enable_multiplayer
        
        # Initialize network manager
        if enable_multiplayer:
            print("[GAME] Starting in multiplayer mode...")
            self.net_manager = NetworkManager(
                is_client=True,
                host=server_host,
                port=server_port
            )
            
            if not self.net_manager.connected:
                print("[GAME] Failed to connect to server, falling back to offline")
                self.enable_multiplayer = False
                self.net_manager = LocalNetworkManager()
        else:
            print("[GAME] Starting in single-player mode...")
            self.net_manager = LocalNetworkManager()
        
        # Network statistics
        self.stats = NetworkStatistics() if self.enable_multiplayer else None
        
        # Remote player rendering
        self.remote_player_surfaces = {}
    
    def update(self, delta_time):
        """Update network and game state"""
        if self.enable_multiplayer:
            # Update network
            self.net_manager.update(delta_time)
            
            # Get remote players
            remote_players = self.net_manager.get_remote_players()
            
            # Update remote player data
            for player_id, player_data in remote_players.items():
                print(f"[GAME] Remote player {player_id} at {player_data.get('pos_x')}, "
                      f"{player_data.get('pos_y')}")
    
    def handle_player_input(self, player):
        """Handle input and send to server"""
        # ... input handling code ...
        
        if self.enable_multiplayer:
            # Send player state periodically
            self.net_manager.send_player_state(player)
            
            # Handle attacks
            if player.is_attacking:
                self.net_manager.send_player_attack(player, 'slash')
            
            # Handle jumps
            if player.is_jumping:
                self.net_manager.send_player_jump('single')
    
    def render_remote_players(self, screen):
        """Render remote players on screen"""
        if not self.enable_multiplayer:
            return
        
        remote_players = self.net_manager.get_remote_players()
        
        for player_id, player_data in remote_players.items():
            pos_x = player_data.get('pos_x', 0)
            pos_y = player_data.get('pos_y', 0)
            
            # Draw remote player (example)
            pygame.draw.circle(screen, (0, 255, 0), (int(pos_x), int(pos_y)), 10)
            
            # Draw player ID
            font = pygame.font.SysFont(None, 24)
            text = font.render(player_id[:4], True, (0, 255, 0))
            screen.blit(text, (pos_x, pos_y - 20))
    
    def render_network_status(self, screen):
        """Render network status on screen"""
        font = pygame.font.SysFont(None, 24)
        
        if self.enable_multiplayer:
            status = "ONLINE"
            color = (0, 255, 0)
            player_count = self.net_manager.get_player_count()
            text = font.render(f"{status} ({player_count+1} players)", True, color)
        else:
            status = "OFFLINE"
            color = (255, 255, 255)
            text = font.render(status, True, color)
        
        screen.blit(text, (10, 10))
    
    def print_network_stats(self):
        """Print network statistics"""
        if self.enable_multiplayer and self.stats:
            self.stats.print_stats()
    
    def disconnect(self):
        """Disconnect from server"""
        if self.enable_multiplayer:
            self.net_manager.disconnect()
            print("[GAME] Disconnected from server")


def example_single_player():
    """Example: Single-player game (offline)"""
    print("=" * 50)
    print("Example 1: Single-Player Game")
    print("=" * 50)
    
    game = MultiplayerGame(enable_multiplayer=False)
    
    # Simulate game loop
    for i in range(5):
        game.update(0.016)  # 60 FPS
        print(f"Frame {i+1}: Multiplayer={'ON' if game.enable_multiplayer else 'OFF'}")
    
    game.disconnect()
    print()


def example_multiplayer_client():
    """Example: Multiplayer game (connect to server)"""
    print("=" * 50)
    print("Example 2: Multiplayer Client")
    print("=" * 50)
    print("(Make sure server is running on localhost:5000)")
    print()
    
    game = MultiplayerGame(
        enable_multiplayer=True,
        server_host='localhost',
        server_port=5000
    )
    
    # Simulate game loop
    for i in range(5):
        game.update(0.016)  # 60 FPS
        print(f"Frame {i+1}: Connected={game.net_manager.connected}")
    
    game.disconnect()
    print()


def example_network_detection():
    """Example: Detect and handle network failures"""
    print("=" * 50)
    print("Example 3: Network Failure Handling")
    print("=" * 50)
    
    # Try to connect with timeout
    game = MultiplayerGame(
        enable_multiplayer=True,
        server_host='localhost',
        server_port=5000
    )
    
    if game.enable_multiplayer:
        print("Successfully connected to server!")
    else:
        print("Failed to connect - running in offline mode")
    
    game.disconnect()
    print()


def example_custom_message():
    """Example: Send custom messages"""
    print("=" * 50)
    print("Example 4: Custom Messages")
    print("=" * 50)
    
    from network_protocol import NetworkMessage, MessageType
    
    # Create custom messages
    attack_msg = NetworkMessage(
        MessageType.PLAYER_ATTACK,
        {'attack_type': 'fireball', 'damage': 25}
    )
    
    print(f"Message type: {attack_msg.msg_type.value}")
    print(f"Message data: {attack_msg.data}")
    print(f"JSON: {attack_msg.to_json()}")
    print()


def example_server_startup():
    """Example: Starting a dedicated server"""
    print("=" * 50)
    print("Example 5: Server Startup")
    print("=" * 50)
    print("To start a dedicated server, run:")
    print("    python network_server_app.py")
    print("\nOr programmatically:")
    print("""
    from network_server import NetworkServer
    
    server = NetworkServer(host='0.0.0.0', port=5000, max_players=4)
    server.start()
    
    # Server runs in background
    """)
    print()


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("Game03 Network Programming Examples")
    print("=" * 50 + "\n")
    
    # Run examples
    example_single_player()
    example_network_detection()
    example_custom_message()
    example_server_startup()
    
    print("=" * 50)
    print("See NETWORK.md for complete documentation")
    print("=" * 50)
