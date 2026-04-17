"""
    Network Utilities for Game03
    Debugging, statistics, and helper functions
"""

import time
import json
from collections import deque
from threading import Lock


class NetworkStatistics:
    """Collects network statistics"""
    
    def __init__(self, max_samples=300):  # Keep last 5 seconds at 60 FPS
        self.max_samples = max_samples
        self.messages_sent = deque(maxlen=max_samples)
        self.messages_received = deque(maxlen=max_samples)
        self.bytes_sent = deque(maxlen=max_samples)
        self.bytes_received = deque(maxlen=max_samples)
        self.latency_samples = deque(maxlen=max_samples)
        self.lock = Lock()
        
        self.total_messages_sent = 0
        self.total_messages_received = 0
        self.total_bytes_sent = 0
        self.total_bytes_received = 0
    
    def record_sent(self, bytes_count):
        """Record outgoing message"""
        with self.lock:
            self.messages_sent.append(1)
            self.bytes_sent.append(bytes_count)
            self.total_messages_sent += 1
            self.total_bytes_sent += bytes_count
    
    def record_received(self, bytes_count):
        """Record incoming message"""
        with self.lock:
            self.messages_received.append(1)
            self.bytes_received.append(bytes_count)
            self.total_messages_received += 1
            self.total_bytes_received += bytes_count
    
    def record_latency(self, latency_ms):
        """Record latency sample"""
        with self.lock:
            self.latency_samples.append(latency_ms)
    
    def get_stats(self):
        """Get current statistics"""
        with self.lock:
            recent_sent = sum(self.messages_sent)
            recent_received = sum(self.messages_received)
            recent_bytes_sent = sum(self.bytes_sent)
            recent_bytes_received = sum(self.bytes_received)
            
            avg_latency = 0
            if self.latency_samples:
                avg_latency = sum(self.latency_samples) / len(self.latency_samples)
            
            return {
                'messages_sent': recent_sent,
                'messages_received': recent_received,
                'bytes_sent': recent_bytes_sent,
                'bytes_received': recent_bytes_received,
                'avg_latency_ms': avg_latency,
                'total_messages_sent': self.total_messages_sent,
                'total_messages_received': self.total_messages_received,
                'total_bytes_sent': self.total_bytes_sent,
                'total_bytes_received': self.total_bytes_received,
            }
    
    def print_stats(self):
        """Print statistics"""
        stats = self.get_stats()
        print("\n=== Network Statistics ===")
        print(f"Messages - Sent: {stats['messages_sent']}, Received: {stats['messages_received']}")
        print(f"Bytes - Sent: {stats['bytes_sent']}, Received: {stats['bytes_received']}")
        print(f"Average Latency: {stats['avg_latency_ms']:.2f}ms")
        print(f"Total - Sent: {stats['total_messages_sent']}, Received: {stats['total_messages_received']}")
        print("=" * 24)


class LatencySimulator:
    """Simulates network latency for testing"""
    
    def __init__(self, latency_ms=50):
        self.latency_ms = latency_ms
        self.pending_messages = deque()
        self.lock = Lock()
    
    def add_message(self, message, current_time):
        """Add message to queue with delay"""
        with self.lock:
            delivery_time = current_time + (self.latency_ms / 1000.0)
            self.pending_messages.append((message, delivery_time))
    
    def get_ready_messages(self, current_time):
        """Get messages ready for delivery"""
        ready = []
        with self.lock:
            while self.pending_messages and self.pending_messages[0][1] <= current_time:
                message, _ = self.pending_messages.popleft()
                ready.append(message)
        return ready
    
    def set_latency(self, latency_ms):
        """Update latency"""
        self.latency_ms = max(0, latency_ms)


class PacketLossSimulator:
    """Simulates packet loss for testing"""
    
    def __init__(self, loss_rate=0.0):
        """loss_rate: 0.0-1.0 (0% to 100%)"""
        self.loss_rate = max(0.0, min(1.0, loss_rate))
    
    def should_drop(self):
        """Return True if packet should be dropped"""
        import random
        return random.random() < self.loss_rate
    
    def set_loss_rate(self, loss_rate):
        """Update loss rate"""
        self.loss_rate = max(0.0, min(1.0, loss_rate))


class NetworkDebugger:
    """Network debugging utilities"""
    
    @staticmethod
    def log_message(msg, prefix="[NET]"):
        """Log a network message"""
        msg_type = msg.msg_type.value if hasattr(msg.msg_type, 'value') else str(msg.msg_type)
        player = msg.player_id or "SERVER"
        print(f"{prefix} [{player}] {msg_type}: {msg.data}")
    
    @staticmethod
    def log_connection(player_id, event, address=""):
        """Log connection event"""
        print(f"[CONN] {event}: {player_id} {address}")
    
    @staticmethod
    def validate_player_state(player_data):
        """Validate player state data"""
        required_fields = ['pos_x', 'pos_y', 'vel_x', 'vel_y', 'hp', 'mp', 'grounded']
        for field in required_fields:
            if field not in player_data:
                return False, f"Missing field: {field}"
        return True, "Valid"
    
    @staticmethod
    def validate_enemy_state(enemy_data):
        """Validate enemy state data"""
        required_fields = ['pos_x', 'pos_y', 'hp']
        for field in required_fields:
            if field not in enemy_data:
                return False, f"Missing field: {field}"
        return True, "Valid"
    
    @staticmethod
    def export_stats_json(stats, filename='network_stats.json'):
        """Export statistics to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(stats, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to export stats: {e}")
            return False


def create_network_summary(manager):
    """Create a summary of network status"""
    status = "OFFLINE"
    player_count = 0
    
    if hasattr(manager, 'is_multiplayer_enabled') and manager.is_multiplayer_enabled():
        status = "ONLINE"
        player_count = manager.get_player_count()
    
    summary = {
        'status': status,
        'player_count': player_count,
        'connected': manager.connected if hasattr(manager, 'connected') else False,
    }
    
    return summary
