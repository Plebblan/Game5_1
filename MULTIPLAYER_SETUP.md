# Game03 Multiplayer Setup Guide

## ⚡ Bước 1: Khởi động Server

Mở terminal và chạy:

```bash
cd /path/to/Game03
python3 network_server_app.py --host 0.0.0.0 --port 5000 --max-players 4
```

**Output:**
```
[SERVER] Initialized on 0.0.0.0:5000 with max players: 4
[SERVER] Started listening on 0.0.0.0:5000
```

Server hiện đang chạy và chờ các client kết nối.

### Tùy chọn Server:
- `--host 0.0.0.0` - Lắng nghe trên tất cả các interface (0.0.0.0 để cho phép remote)
- `--host localhost` - Chỉ local network
- `--host 192.168.1.100` - Specific IP address
- `--port 5000` - Port để lắng nghe (default: 5000)
- `--max-players 4` - Số lượng player tối đa (default: 4)

---

## ⚡ Bước 2: Cấu hình Game để Multiplayer

Mở `main.py` và sửa đổi:

```python
# ===== MULTIPLAYER CONFIGURATION =====
ENABLE_MULTIPLAYER = True  # ← Change to True
SERVER_HOST = 'localhost'  # ← Server address
SERVER_PORT = 5000         # ← Server port
```

**Ví dụ:**
```python
# Single-player
ENABLE_MULTIPLAYER = False

# Local multiplayer (same computer)
ENABLE_MULTIPLAYER = True
SERVER_HOST = 'localhost'
SERVER_PORT = 5000

# Remote multiplayer
ENABLE_MULTIPLAYER = True
SERVER_HOST = '192.168.1.100'  # Server IP
SERVER_PORT = 5000
```

---

## ⚡ Bước 3: Chạy Game

```bash
python3 main.py
```

**Output khi kết nối thành công:**
```
[GAME] Starting in multiplayer mode...
[CLIENT] Initialized for localhost:5000
[CLIENT] Connected to localhost:5000
[NETWORK] Client connected successfully
✅ Connected to multiplayer server!
```

**Output khi kết nối thất bại:**
```
[GAME] Starting in multiplayer mode...
[CLIENT] Initialized for localhost:5000
[CLIENT] Connection refused
[GAME] ⚠️  Failed to connect to server - falling back to offline
[GAME] Starting in single-player mode...
```

---

## 🎮 In-Game Network Features

### Network Status Display
- **🟢 ONLINE (X)** - Kết nối thành công, X player đang chơi
- **🔴 OFFLINE** - Đang chơi offline

### Remote Players
- Các player khác hiển thị bằng **vòng tròn xanh**
- Có ID player hiển thị phía trên

### State Synchronization
- Vị trí player được sync ~30 lần/giây
- HP/MP được cập nhật real-time
- Attack action được broadcast

---

## 🚀 Ví dụ Setup Multiplayer

### Setup 1: Local Testing (Same Computer)

**Terminal 1 - Start Server:**
```bash
cd Game03
python3 network_server_app.py --host localhost --port 5000
```

**Terminal 2 - Start Client 1:**
```bash
cd Game03
# Sửa main.py: ENABLE_MULTIPLAYER = True, SERVER_HOST = 'localhost'
python3 main.py
```

**Terminal 3 - Start Client 2:**
```bash
cd Game03
python3 main.py
```

> Lưu ý: để thấy 2 nhân vật cùng online, bạn phải chạy **2 cửa sổ game riêng biệt** (2 client khác nhau) kết nối vào cùng 1 server.
> Nếu chỉ mở 1 game, bạn sẽ chỉ thấy nhân vật của mình.

### Setup 2: Network Play (Different Computers)

**Computer A (Server):**
```bash
python3 network_server_app.py --host 0.0.0.0 --port 5000
```

**Computer B (Client 1):**
```python
# main.py
ENABLE_MULTIPLAYER = True
SERVER_HOST = '192.168.1.100'  # Computer A IP
SERVER_PORT = 5000
```

**Computer C (Client 2):**
```python
# main.py
ENABLE_MULTIPLAYER = True
SERVER_HOST = '192.168.1.100'  # Computer A IP
SERVER_PORT = 5000
```

---

## 🐛 Troubleshooting

### Problem: "Connection refused"
**Nguyên nhân:** Server không chạy hoặc port sai
**Giải pháp:**
1. Kiểm tra server đang chạy: `python3 network_server_app.py`
2. Kiểm tra port: Đảm bảo client dùng cùng port với server
3. Kiểm tra firewall: Cho phép port 5000

### Problem: "Connection timeout"
**Nguyên nhân:** Server không thể tiếp cận
**Giải pháp:**
1. Kiểm tra IP address: `ipconfig` (Windows) hoặc `ifconfig` (Mac/Linux)
2. Ping server: `ping 192.168.1.100`
3. Mở firewall: Cho phép Python access mạng

### Problem: "Multiplayer nhưng không thấy remote player"
**Giải pháp:**
1. Chắc chắn cả 2 client đã kết nối
2. Kiểm tra console log cho "[GAME] Remote player..."
3. Restart server và client

### Problem: Game lag/disconnects
**Giải pháp:**
1. Giảm update rate trong `network_config.py`
2. Kiểm tra network latency: `ping` server
3. Giảm số lượng player

---

## 📊 Monitoring Network

### Bật Debug Mode

```python
# In game code
if game.net_manager:
    game.net_manager.enable_debug(True)
```

**Console Output:**
```
[NETWORK] Remote attack from player-123: {'attack_type': 'slash', 'pos_x': 100, 'pos_y': 200}
```

### View Network Statistics

```python
# Sau game
if game.net_stats:
    game.net_stats.print_stats()
```

**Output:**
```
=== Network Statistics ===
Messages - Sent: 450, Received: 450
Bytes - Sent: 45000, Received: 45000
Average Latency: 25.50ms
Total - Sent: 2500, Received: 2500
========================
```

---

## 🔧 Network Configuration

Chỉnh sửa `network_config.py`:

```python
# Server
NETWORK_HOST = 'localhost'
NETWORK_PORT = 5000
MAX_PLAYERS = 4

# Update rates (updates per second)
PLAYER_UPDATE_RATE = 0.033  # ~30/sec
ENEMY_UPDATE_RATE = 0.05    # ~20/sec

# Latency compensation
PREDICT_PLAYER_MOVEMENT = True
LERP_REMOTE_PLAYERS = True
LERP_FACTOR = 0.1

# Debug
DEBUG_NETWORK = False
```

---

## 📝 Code Integration

### Trong game loop:

```python
# Network được update tự động trong play()
def play(self):
    while True:
        dt = self._clock.tick(FPS) / 1000.0
        
        # Network update
        if self.net_manager:
            self.net_manager.update(dt)
        
        # Game logic
        self.handleInput()
        if not self.in_menu:
            self.update(dt)
            self.check_collision()
            
            # Send player state
            if self.net_manager and self.enable_multiplayer:
                self.net_manager.send_player_state(self.player)
        
        self.draw()
```

### Gửi custom events:

```python
# Send attack
game.net_manager.send_player_attack(player, attack_type='fireball')

# Send jump
game.net_manager.send_player_jump(jump_type='double')

# Send dash
game.net_manager.send_player_dash(direction='right')
```

---

## 🎯 Advanced: Custom Networking

### Gửi custom message:

```python
from network_protocol import NetworkMessage, MessageType

msg = NetworkMessage(
    MessageType.PLAYER_ATTACK,
    {'damage': 50, 'crit': True}
)
game.net_manager.client.send_message(msg)
```

### Nhận messages:

```python
while True:
    msg = game.net_manager.client.get_message(timeout=0.01)
    if msg and msg.msg_type == MessageType.PLAYER_ATTACK:
        print(f"Attack from {msg.player_id}: {msg.data}")
```

---

## 📚 Tham khảo

- `NETWORK.md` - Full documentation
- `NETWORK_QUICKREF.md` - Quick reference
- `example_network.py` - Code examples
- `network_config.py` - Configuration options

---

## 💡 Tips & Tricks

1. **Auto-fallback**: Nếu server không available, game tự động chuyển sang offline
2. **Smooth movement**: Remote players được lerp để smooth
3. **Heartbeat**: Auto keep-alive để maintain connection
4. **Thread-safe**: Network chạy trong background thread, không block game loop

---

## ✅ Checklist

- [ ] Server running: `python3 network_server_app.py`
- [ ] `ENABLE_MULTIPLAYER = True` in main.py
- [ ] `SERVER_HOST` correct (localhost hoặc IP)
- [ ] `SERVER_PORT` match server port
- [ ] Client running: `python3 main.py`
- [ ] Network status hiển thị 🟢 ONLINE
- [ ] Remote players visible as green circles

---

**Enjoy multiplayer Game03! 🎮**
