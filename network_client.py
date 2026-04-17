"""
    Network Client for Game03 Multiplayer
    Connects to game server and receives updates
"""

import socket
import threading
import time
import queue
from network_protocol import NetworkMessage, MessageType


class NetworkClient:
    """Game client that connects to the server"""
    
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        
        self.socket = None
        self.connected = False
        self.player_id = None
        
        self.receive_thread = None
        self.message_queue = queue.Queue()
        self.receive_buffer = b''
        
        # Network stats
        self.ping = 0
        self.last_ping_time = 0
        self.server_time = 0
        
        print(f"[CLIENT] Initialized for {host}:{port}")
    
    def connect(self):
        """Connect to the server"""
        try:
            print(f"[CLIENT] ⏳ Attempting to connect to {self.host}:{self.port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)
            self.socket.connect((self.host, self.port))
            
            self.connected = True
            
            # Start receiving thread
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()
            
            print(f"[CLIENT] ✅ TCP Connection established to {self.host}:{self.port}")
            
            # Wait for welcome message
            start_time = time.time()
            while not self.player_id and time.time() - start_time < 5:
                try:
                    msg = self.message_queue.get(timeout=0.1)
                    if msg and msg.msg_type == MessageType.CONNECT:
                        self.player_id = msg.data.get('player_id')
                        print(f"[CLIENT] ✅ Authenticated - Player ID: {self.player_id}")
                except queue.Empty:
                    pass
            
            if not self.player_id:
                print(f"[CLIENT] ⚠️  No authentication from server (timeout)")
                self.connected = False
                return False
            
            return self.connected
        
        except socket.timeout:
            print("[CLIENT] ❌ Connection timeout - server not responding")
            print("     ➜ Is server running on port {0}?".format(self.port))
            print("     ➜ Start server: python3 network_server_app.py --port {0}".format(self.port))
            self.connected = False
            return False
        except ConnectionRefusedError:
            print(f"[CLIENT] ❌ Connection refused - server not running on {self.host}:{self.port}")
            print(f"     ➜ Start server: python3 network_server_app.py --host 0.0.0.0 --port {self.port}")
            self.connected = False
            return False
        except OSError as e:
            print(f"[CLIENT] ❌ Network error: {e}")
            print(f"     ➜ Check if server is running")
            print(f"     ➜ Check firewall settings")
            self.connected = False
            return False
        except Exception as e:
            print(f"[CLIENT] ❌ Connection error: {type(e).__name__}: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from the server"""
        self.connected = False
        
        try:
            self.socket.close()
        except:
            pass
        
        print("[CLIENT] Disconnected")
    
    def send_message(self, message):
        """Send a message to the server"""
        if not self.connected or not self.socket:
            return False
        
        try:
            message.player_id = self.player_id
            data = message.to_bytes()
            total_sent = 0
            while total_sent < len(data):
                sent = self.socket.send(data[total_sent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                total_sent += sent
            return True
        except Exception as e:
            print(f"[CLIENT] Send error: {e}")
            self.connected = False
            return False
    
    def _receive_loop(self):
        """Background thread that receives messages from server"""
        print("[CLIENT] 📡 Receive thread started, waiting for data...")
        while self.connected:
            try:
                data = self.socket.recv(4096)
                
                if not data:
                    print("[CLIENT] Server closed connection")
                    self.connected = False
                    break
                
                print(f"[CLIENT] 📨 Received {len(data)} bytes")
                self.receive_buffer += data
                
                # Process complete messages
                while True:
                    message, self.receive_buffer = NetworkMessage.from_bytes(self.receive_buffer)
                    
                    if not message:
                        break
                    
                    print(f"[CLIENT] 📥 Parsed message: {message.msg_type.value}")
                    self.message_queue.put(message)
            
            except socket.timeout:
                continue
            except ConnectionResetError as e:
                print(f"[CLIENT] ❌ Connection reset by server: {e}")
                print("     ➜ Make sure the server is running!")
                print("     ➜ Run: python3 network_server_app.py")
                self.connected = False
                break
            except BrokenPipeError as e:
                print(f"[CLIENT] ❌ Connection broken: {e}")
                self.connected = False
                break
            except OSError as e:
                print(f"[CLIENT] ❌ Network error: {e}")
                self.connected = False
                break
            except Exception as e:
                print(f"[CLIENT] ❌ Unexpected error: {type(e).__name__}: {e}")
                self.connected = False
                break
    
    def get_message(self, timeout=0.01):
        """Get next message from queue (non-blocking)"""
        try:
            return self.message_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def send_player_move(self, pos_x, pos_y, vel_x, vel_y, grounded):
        """Send player movement to server"""
        msg = NetworkMessage(
            MessageType.PLAYER_MOVE,
            {
                'pos_x': float(pos_x),
                'pos_y': float(pos_y),
                'vel_x': float(vel_x),
                'vel_y': float(vel_y),
                'grounded': grounded
            }
        )
        return self.send_message(msg)
    
    def send_player_attack(self, attack_type, pos_x, pos_y):
        """Send player attack to server"""
        msg = NetworkMessage(
            MessageType.PLAYER_ATTACK,
            {
                'attack_type': attack_type,
                'pos_x': float(pos_x),
                'pos_y': float(pos_y)
            }
        )
        return self.send_message(msg)
    
    def send_player_jump(self, jump_type='single'):
        """Send player jump to server"""
        msg = NetworkMessage(
            MessageType.PLAYER_JUMP,
            {'jump_type': jump_type}
        )
        return self.send_message(msg)
    
    def send_player_dash(self, direction):
        """Send player dash to server"""
        msg = NetworkMessage(
            MessageType.PLAYER_DASH,
            {'direction': direction}
        )
        return self.send_message(msg)
    
    def request_full_state(self):
        """Request full game state from server"""
        msg = NetworkMessage(MessageType.SYNC_REQUEST, {})
        return self.send_message(msg)
    
    def send_heartbeat(self):
        """Send heartbeat to keep connection alive"""
        msg = NetworkMessage(MessageType.HEARTBEAT, {})
        return self.send_message(msg)
    
    def is_connected(self):
        """Check if client is connected"""
        return self.connected and self.player_id is not None
