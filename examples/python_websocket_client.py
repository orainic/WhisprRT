"""
WhisprRT WebSocket 客户端示例 (Python)
实时接收语音转文字结果
"""
import asyncio
import websockets
import json

async def receive_transcriptions():
    """连接WebSocket并接收实时转写结果"""
    uri = "ws://localhost:8000/ws"

    try:
        async with websockets.connect(uri) as websocket:
            print("✅ 已连接到WhisprRT服务")
            print("=" * 50)

            while True:
                try:
                    # 接收消息
                    message = await websocket.recv()
                    data = json.loads(message)

                    # 处理不同类型的事件
                    if data['event'] == 'status':
                        # 连接状态信息
                        status_data = data['data']
                        print(f"📡 状态: {status_data['status']}")
                        print(f"🤖 模型: {status_data['model']}")
                        print(f"🌍 语言: {status_data['language']}")
                        print("=" * 50)

                    elif data['event'] == 'transcription':
                        # 转写结果
                        transcript = data['data']
                        timestamp = transcript.get('timestamp', '')
                        text = transcript.get('text', '')
                        confidence = transcript.get('confidence', 0)

                        # 根据置信度显示不同的标识
                        if confidence >= 0.9:
                            indicator = "✅"
                        elif confidence >= 0.7:
                            indicator = "⚠️"
                        else:
                            indicator = "❓"

                        print(f"{indicator} [{timestamp}] {text} (置信度: {confidence:.2%})")

                    elif data['event'] == 'error':
                        # 错误信息
                        error_msg = data['data'].get('message', '未知错误')
                        print(f"❌ 错误: {error_msg}")

                except json.JSONDecodeError:
                    print(f"⚠️ 无法解析消息: {message}")
                except Exception as e:
                    print(f"❌ 处理消息时出错: {str(e)}")

    except websockets.exceptions.ConnectionClosed:
        print("⚠️ 连接已关闭")
    except ConnectionRefusedError:
        print("❌ 无法连接到服务器，请确保WhisprRT服务正在运行")
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")

if __name__ == "__main__":
    print("🎙️ WhisprRT WebSocket 客户端")
    print("正在连接到服务器...")
    print()

    try:
        asyncio.run(receive_transcriptions())
    except KeyboardInterrupt:
        print("\n\n👋 已断开连接")
