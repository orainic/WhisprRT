# WhisprRT API 客户端示例

这个目录包含了各种语言的API客户端示例代码。

## Python 示例

### 1. WebSocket 客户端 (推荐)
```bash
python python_websocket_client.py
```

实时接收转写结果，低延迟，适合需要即时显示的场景。

**依赖:**
```bash
pip install websockets
```

### 2. REST API 客户端
```bash
python python_rest_client.py
```

提供交互式菜单，可以轮询或手动查询转写结果。

**依赖:**
```bash
pip install requests
```

## JavaScript/Node.js 示例

### WebSocket 客户端
```bash
node javascript_websocket_client.js
```

**依赖:**
```bash
npm install ws
```

## 快速测试

### 1. 使用 cURL 测试 REST API

```bash
# 获取API信息
curl http://localhost:8000/api/info

# 开始转写
curl http://localhost:8000/start

# 获取最新转写
curl http://localhost:8000/api/latest

# 获取所有转写记录
curl http://localhost:8000/api/transcripts
```

### 2. 使用浏览器测试 WebSocket

在浏览器控制台中运行：

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => console.log('已连接');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(data);
};

ws.onerror = (error) => console.error('错误:', error);

ws.onclose = () => console.log('连接关闭');
```

## 选择合适的方式

### WebSocket (推荐)
**优点:**
- 实时推送，低延迟
- 服务器主动推送，无需客户端轮询
- 节省带宽和资源

**适用场景:**
- 实时字幕显示
- 语音会议转写
- 直播转写
- 任何需要即时显示的场景

**示例代码:**
- `python_websocket_client.py`
- `javascript_websocket_client.js`

### REST API
**优点:**
- 简单易用
- 无需维持长连接
- 适合批量查询

**适用场景:**
- 定期查询转写历史
- 批量获取转写记录
- 不需要实时性的场景
- 系统集成和自动化

**示例代码:**
- `python_rest_client.py`

## API 端点说明

### REST API
- `GET /api/info` - 获取API信息
- `GET /api/transcripts` - 获取所有转写记录
- `GET /api/latest` - 获取最新转写记录
- `GET /api/transcripts/since/{timestamp}` - 获取指定时间后的记录

### 控制端点
- `GET /status` - 获取服务状态
- `GET /start` - 开始转写
- `GET /stop` - 停止转写
- `GET /clear` - 清空记录

### WebSocket
- `ws://localhost:8000/ws` - WebSocket连接端点

## 更多信息

查看完整的API文档：
- 文件: `../API_DOCUMENTATION.md`
- 在线: http://localhost:8000/api/docs
