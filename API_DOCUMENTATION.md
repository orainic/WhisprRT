# WhisprRT API 文档

WhisprRT 提供了实时语音转文字的API接口，支持WebSocket和REST两种方式。

## 快速开始

### 服务地址
- HTTP API: `http://localhost:8000`
- WebSocket: `ws://localhost:8000/ws`
- API文档: `http://localhost:8000/api/docs`

## API 端点

### 1. REST API

#### 1.1 获取API信息
```
GET /api/info
```
返回API的详细信息和使用说明。

**响应示例:**
```json
{
  "status": "success",
  "version": "2.0.0",
  "service": "WhisprRT Real-time Transcription API",
  "endpoints": { ... }
}
```

#### 1.2 获取所有转写记录
```
GET /api/transcripts
```
返回所有的转写记录。

**响应示例:**
```json
{
  "status": "success",
  "count": 5,
  "transcripts": [
    {
      "text": "你好世界",
      "timestamp": "00:00:15",
      "confidence": 0.95
    },
    ...
  ]
}
```

#### 1.3 获取最新转写记录
```
GET /api/latest
```
返回最新的一条转写记录。

**响应示例:**
```json
{
  "status": "success",
  "transcript": {
    "text": "最新的转写内容",
    "timestamp": "00:05:23",
    "confidence": 0.92
  }
}
```

#### 1.4 获取指定时间后的记录
```
GET /api/transcripts/since/{timestamp}
```
返回指定时间戳之后的所有记录。

**参数:**
- `timestamp`: 时间戳格式 HH:MM:SS

**示例:**
```
GET /api/transcripts/since/00:05:00
```

**响应示例:**
```json
{
  "status": "success",
  "count": 3,
  "transcripts": [ ... ]
}
```

### 2. 控制端点

#### 2.1 获取服务状态
```
GET /status
```

#### 2.2 开始转写
```
GET /start
```

#### 2.3 停止转写
```
GET /stop
```

#### 2.4 清空记录
```
GET /clear
```

### 3. WebSocket API

#### 连接
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

#### 接收事件

**连接成功:**
```json
{
  "event": "status",
  "data": {
    "status": "connected",
    "model": "large-v3-turbo",
    "language": "zh"
  }
}
```

**转写结果:**
```json
{
  "event": "transcription",
  "data": {
    "text": "转写的文字内容",
    "timestamp": "00:01:23",
    "confidence": 0.95,
    "show_timestamp": true,
    "mode": "segments"
  }
}
```

**错误信息:**
```json
{
  "event": "error",
  "data": {
    "message": "错误描述"
  }
}
```

## 使用示例

### Python 示例

#### 1. REST API 轮询方式
```python
import requests
import time

API_BASE = "http://localhost:8000"

# 开始转写
requests.get(f"{API_BASE}/start")

# 持续获取最新结果
last_timestamp = "00:00:00"
while True:
    # 获取新的转写记录
    response = requests.get(f"{API_BASE}/api/transcripts/since/{last_timestamp}")
    data = response.json()

    if data['count'] > 0:
        for transcript in data['transcripts']:
            print(f"[{transcript['timestamp']}] {transcript['text']}")
            last_timestamp = transcript['timestamp']

    time.sleep(1)  # 每秒轮询一次
```

#### 2. WebSocket 实时推送方式
```python
import asyncio
import websockets
import json

async def receive_transcriptions():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("已连接到WhisprRT")

        while True:
            message = await websocket.recv()
            data = json.loads(message)

            if data['event'] == 'transcription':
                transcript = data['data']
                print(f"[{transcript['timestamp']}] {transcript['text']}")
            elif data['event'] == 'status':
                print(f"状态: {data['data']}")
            elif data['event'] == 'error':
                print(f"错误: {data['data']['message']}")

# 运行
asyncio.run(receive_transcriptions())
```

### JavaScript 示例

#### 1. REST API (Node.js)
```javascript
const axios = require('axios');

const API_BASE = 'http://localhost:8000';

async function pollTranscriptions() {
    // 开始转写
    await axios.get(`${API_BASE}/start`);

    let lastTimestamp = '00:00:00';

    setInterval(async () => {
        try {
            const response = await axios.get(
                `${API_BASE}/api/transcripts/since/${lastTimestamp}`
            );

            const { count, transcripts } = response.data;

            if (count > 0) {
                transcripts.forEach(t => {
                    console.log(`[${t.timestamp}] ${t.text}`);
                    lastTimestamp = t.timestamp;
                });
            }
        } catch (error) {
            console.error('Error:', error.message);
        }
    }, 1000); // 每秒轮询
}

pollTranscriptions();
```

#### 2. WebSocket (浏览器/Node.js)
```javascript
const WebSocket = require('ws'); // Node.js
// 或浏览器中直接使用: const ws = new WebSocket(...)

const ws = new WebSocket('ws://localhost:8000/ws');

ws.on('open', () => {
    console.log('已连接到WhisprRT');
});

ws.on('message', (data) => {
    const message = JSON.parse(data);

    if (message.event === 'transcription') {
        const t = message.data;
        console.log(`[${t.timestamp}] ${t.text}`);
    } else if (message.event === 'status') {
        console.log('状态:', message.data);
    } else if (message.event === 'error') {
        console.error('错误:', message.data.message);
    }
});

ws.on('error', (error) => {
    console.error('WebSocket错误:', error);
});

ws.on('close', () => {
    console.log('连接已关闭');
});
```

### cURL 示例

```bash
# 获取API信息
curl http://localhost:8000/api/info

# 获取所有转写记录
curl http://localhost:8000/api/transcripts

# 获取最新记录
curl http://localhost:8000/api/latest

# 获取指定时间后的记录
curl http://localhost:8000/api/transcripts/since/00:05:00

# 开始转写
curl http://localhost:8000/start

# 停止转写
curl http://localhost:8000/stop

# 获取服务状态
curl http://localhost:8000/status
```

## 跨域访问 (CORS)

API已启用CORS，支持从任何域名访问：
- `Access-Control-Allow-Origin: *`
- 支持所有HTTP方法
- 支持所有请求头

## 错误处理

所有API响应都包含`status`字段：
- `success`: 请求成功
- `error`: 请求失败，包含`message`字段说明错误原因

**错误响应示例:**
```json
{
  "status": "error",
  "message": "请先停止转写再切换模型"
}
```

## 最佳实践

### 1. 实时场景推荐使用 WebSocket
- 低延迟，实时推送
- 无需轮询，节省带宽
- 适合需要即时显示转写结果的场景

### 2. 非实时场景可使用 REST API
- 简单易用，无需维持长连接
- 适合定期查询或批量获取的场景
- 可使用`/api/transcripts/since/{timestamp}`减少数据传输

### 3. 集成建议
```python
# 推荐：WebSocket + REST API 组合
# WebSocket用于实时接收，REST API用于历史查询

import asyncio
import websockets
import requests

API_BASE = "http://localhost:8000"
WS_URI = "ws://localhost:8000/ws"

async def main():
    # 先获取历史记录
    response = requests.get(f"{API_BASE}/api/transcripts")
    history = response.json()['transcripts']
    print(f"历史记录: {len(history)}条")

    # 然后通过WebSocket接收实时更新
    async with websockets.connect(WS_URI) as ws:
        while True:
            message = await ws.recv()
            # 处理实时消息...

asyncio.run(main())
```

## 技术支持

如有问题，请访问：
- GitHub: https://github.com/your-repo/WhisprRT
- 文档: http://localhost:8000/api/docs
