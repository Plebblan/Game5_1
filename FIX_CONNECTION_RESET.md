# 🔧 Game03 Network Error Fix Guide

## Error: "[CLIENT] ❌ Connection reset by peer"

This error means the **server closed the connection unexpectedly** after the client connected.

### What This Means

```
Client:                     Server:
  ✅ Connected ────────────→ ✅ Accepted
  ⏳ Waiting ←────────────── 🔴 Crashed/Closed
  ❌ Connection reset!
```

---

## ✅ Solution Steps

### 1. Check Server is Running

```bash
# Terminal 1: Start server
cd Game03
python3 network_server_app.py
```

**Expected output:**
```
[SERVER] Initialized on localhost:5000 with max players: 4
[SERVER] Started listening on localhost:5000
```

**Keep this terminal open!** The server must stay running.

### 2. Verify Client Configuration

Edit `main.py` and check:

```python
ENABLE_MULTIPLAYER = True        # Must be True
SERVER_HOST = 'localhost'        # Or your server IP
SERVER_PORT = 5000               # Must match server port
```

### 3. Start Game Client

```bash
# Terminal 2: Run game
cd Game03
python3 main.py
```

**Expected output:**
```
[GAME] Starting in multiplayer mode...
[CLIENT] Attempting to connect to localhost:5000...
[CLIENT] ✅ Connected to localhost:5000
[CLIENT] ✅ Authenticated - Player ID: abc12345
```

---

## 🔍 Troubleshooting

### Problem 1: Server Crashes Immediately

**Symptoms:**
```
[SERVER] Started listening on localhost:5000
[SERVER] Player abc-12345 connected from ('127.0.0.1', 54321)
[SERVER] Error with client abc-12345: ...
```

**Fix:**
1. Check server terminal for error messages
2. Run: `python3 test_multiplayer_setup.py` to verify setup
3. Restart server: `python3 network_server_app.py`

### Problem 2: Connection Works Then Drops

**Symptoms:**
```
[CLIENT] ✅ Connected
[CLIENT] ✅ Authenticated
[CLIENT] ❌ Connection reset by peer
```

**Possible causes:**
1. Server crashed (check server terminal)
2. Network interrupted (check WiFi/internet)
3. Firewall blocking (allow port 5000)

**Fix:**
```bash
# Restart server
python3 network_server_app.py

# Or use different port
python3 network_server_app.py --port 5001

# Then update main.py
SERVER_PORT = 5001
```

### Problem 3: Can't Connect at All

**Symptoms:**
```
[CLIENT] ❌ Connection timeout - server not responding
```

**Fix:**
1. Make sure server is running
2. Check SERVER_HOST in main.py
3. Check firewall: `python3 diagnose_network.py`

---

## 🛠️ Diagnostic Tool

Run diagnostic to identify the issue:

```bash
python3 diagnose_network.py
```

**Output will show:**
- ✅ Network files OK
- ✅ Configuration OK
- ✅ Server running
- ❌ Any issues found

---

## 📊 Server Terminal - What to Look For

### ✅ Good (Server Running Normally)
```
[SERVER] Player abc-12345 connected from ('127.0.0.1', 54321)
[SERVER] Player xyz-67890 connected from ('127.0.0.1', 54322)
```

### ❌ Bad (Server Crashing)
```
[SERVER] Error with client abc-12345: <error message>
[SERVER] ❌ Error receiving from abc-12345: ...
```

### 🔴 Very Bad (Server Not Running)
```
[CLIENT] ❌ Connection refused - server not running
```

---

## 🔌 Port Issues

### Check if Port 5000 is in Use

```bash
# macOS/Linux
lsof -i :5000

# Result should show game server or nothing
# If shows other process, kill it or use different port
```

### Use Different Port

**Terminal 1: Start server on port 5001**
```bash
python3 network_server_app.py --port 5001
```

**Terminal 2: Update main.py**
```python
SERVER_PORT = 5001  # Change this
```

**Terminal 2: Run game**
```bash
python3 main.py
```

---

## 🔗 Network Configuration

For **local testing** (same computer):
```python
SERVER_HOST = 'localhost'
SERVER_PORT = 5000
```

For **network gaming** (different computers):

**Computer A (Server):**
```bash
python3 network_server_app.py --host 0.0.0.0 --port 5000
```

**Computer B (Client) - main.py:**
```python
SERVER_HOST = '192.168.1.100'  # Computer A's IP
SERVER_PORT = 5000
```

Find your IP:
```bash
# macOS/Linux
ifconfig | grep inet

# Get something like 192.168.1.100
```

---

## 📝 Step-by-Step Quick Fix

```bash
# 1. Kill any existing servers
# (Close all Game03 terminals)

# 2. Start fresh server
cd Game03
python3 network_server_app.py
# Keep this terminal open!

# 3. In NEW terminal, run client
cd Game03
python3 main.py
```

---

## ✅ Verification Checklist

- [ ] Server running: `python3 network_server_app.py`
- [ ] Server terminal shows: `Started listening on localhost:5000`
- [ ] `ENABLE_MULTIPLAYER = True` in main.py
- [ ] `SERVER_HOST = 'localhost'` in main.py
- [ ] `SERVER_PORT = 5000` in main.py
- [ ] Game started: `python3 main.py`
- [ ] Game shows: `🟢 ONLINE` indicator
- [ ] Network files exist (6 files)

---

## 💡 Common Mistakes

❌ **Mistake 1:** Server not running
```python
# Game runs but shows: 🔴 OFFLINE
# Fix: Start server first!
```

❌ **Mistake 2:** Wrong server address
```python
# main.py has:
SERVER_HOST = '127.0.0.1'  # Should be 'localhost'
SERVER_PORT = 8000         # Should be 5000
# Fix: Match server configuration
```

❌ **Mistake 3:** Firewall blocking
```bash
# Can't connect even though server running
# Fix: Allow port 5000 in firewall
```

---

## 🆘 Still Having Issues?

### Check Server Logs

Server terminal will show the actual error:
```
[SERVER] Error with client abc-12345: <error details>
```

Look for keywords:
- `timeout` → Network lag
- `Connection reset` → Server crashed
- `Broken pipe` → Network interrupted
- `Socket error` → Network issue

### Check Network Files

Ensure these files exist in Game03 directory:
```
network_protocol.py
network_server.py
network_client.py
network_manager.py
network_config.py
network_server_app.py
```

If missing, re-run setup or re-create files.

### Run Full Test

```bash
python3 test_multiplayer_setup.py
```

Should show:
```
✅ ALL TESTS PASSED!
```

---

## 📞 Getting Help

1. Check **this file** for common issues
2. Run `python3 diagnose_network.py` for diagnostics
3. Check **MULTIPLAYER_SETUP.md** for setup guide
4. Check server terminal for error messages
5. Check game terminal for connection errors

---

## 🎮 Once Everything Works

When you see this in game:
```
🟢 ONLINE (2)  ← 2 players connected
```

You're ready to play multiplayer! 🎉

Green circles on screen = other players
Your character = normal rendering

---

## 🚀 Success Indicators

✅ Server running
✅ Client connects
✅ Game shows 🟢 ONLINE
✅ No errors in terminals
✅ Can see other players

**Game03 Multiplayer is working! 🎮**

---

**Last Updated:** April 17, 2026
**Status:** ✅ Complete & Tested
