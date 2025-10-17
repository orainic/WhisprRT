/**
 * WhisprRT WebSocket 客户端示例 (JavaScript/Node.js)
 * 实时接收语音转文字结果
 *
 * 安装依赖: npm install ws
 */

const WebSocket = require('ws');

// 配置
const WS_URL = 'ws://localhost:8000/ws';

// 连接到WebSocket
const ws = new WebSocket(WS_URL);

ws.on('open', () => {
    console.log('✅ 已连接到WhisprRT服务');
    console.log('='.repeat(50));
});

ws.on('message', (data) => {
    try {
        const message = JSON.parse(data);

        // 处理不同类型的事件
        switch(message.event) {
            case 'status':
                // 连接状态信息
                const status = message.data;
                console.log(`📡 状态: ${status.status}`);
                console.log(`🤖 模型: ${status.model}`);
                console.log(`🌍 语言: ${status.language}`);
                console.log('='.repeat(50));
                break;

            case 'transcription':
                // 转写结果
                const transcript = message.data;
                const timestamp = transcript.timestamp || '';
                const text = transcript.text || '';
                const confidence = transcript.confidence || 0;

                // 根据置信度显示不同的标识
                let indicator;
                if (confidence >= 0.9) {
                    indicator = '✅';
                } else if (confidence >= 0.7) {
                    indicator = '⚠️';
                } else {
                    indicator = '❓';
                }

                console.log(`${indicator} [${timestamp}] ${text} (置信度: ${(confidence * 100).toFixed(1)}%)`);
                break;

            case 'error':
                // 错误信息
                const errorMsg = message.data.message || '未知错误';
                console.error(`❌ 错误: ${errorMsg}`);
                break;

            default:
                console.log(`ℹ️ 未知事件: ${message.event}`);
        }
    } catch (error) {
        console.error('⚠️ 无法解析消息:', error);
    }
});

ws.on('error', (error) => {
    console.error('❌ WebSocket错误:', error.message);
});

ws.on('close', () => {
    console.log('\n⚠️ 连接已关闭');
    process.exit(0);
});

// 优雅退出
process.on('SIGINT', () => {
    console.log('\n\n👋 正在断开连接...');
    ws.close();
});

console.log('🎙️ WhisprRT WebSocket 客户端');
console.log('正在连接到服务器...');
console.log();
