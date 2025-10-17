"""
WhisprRT REST API 客户端示例 (Python)
使用轮询方式获取转写结果
"""
import requests
import time
import sys

API_BASE = "http://localhost:8000"

def check_server():
    """检查服务器是否运行"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_latest_transcription():
    """获取最新的转写记录"""
    try:
        response = requests.get(f"{API_BASE}/api/latest")
        return response.json()
    except Exception as e:
        print(f"❌ 获取失败: {str(e)}")
        return None

def get_transcriptions_since(timestamp):
    """获取指定时间后的转写记录"""
    try:
        response = requests.get(f"{API_BASE}/api/transcripts/since/{timestamp}")
        return response.json()
    except Exception as e:
        print(f"❌ 获取失败: {str(e)}")
        return None

def get_all_transcriptions():
    """获取所有转写记录"""
    try:
        response = requests.get(f"{API_BASE}/api/transcripts")
        return response.json()
    except Exception as e:
        print(f"❌ 获取失败: {str(e)}")
        return None

def start_transcription():
    """开始转写"""
    try:
        response = requests.get(f"{API_BASE}/start")
        return response.json()
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        return None

def poll_mode():
    """轮询模式 - 持续获取新的转写结果"""
    print("🔄 轮询模式已启动")
    print("按 Ctrl+C 停止")
    print("=" * 50)

    last_timestamp = "00:00:00"

    try:
        while True:
            # 获取新的转写记录
            result = get_transcriptions_since(last_timestamp)

            if result and result['status'] == 'success':
                count = result.get('count', 0)

                if count > 0:
                    transcripts = result.get('transcripts', [])
                    for transcript in transcripts:
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
                        last_timestamp = timestamp

            time.sleep(1)  # 每秒轮询一次

    except KeyboardInterrupt:
        print("\n\n⏹️ 已停止轮询")

def show_menu():
    """显示菜单"""
    print("\n📋 请选择操作:")
    print("1. 开始转写")
    print("2. 获取最新转写")
    print("3. 获取所有转写记录")
    print("4. 实时轮询模式")
    print("5. 获取API信息")
    print("0. 退出")
    print()
    return input("请输入选项: ").strip()

def main():
    """主函数"""
    print("🎙️ WhisprRT REST API 客户端")
    print()

    # 检查服务器
    if not check_server():
        print("❌ 无法连接到服务器")
        print("请确保WhisprRT服务正在运行 (http://localhost:8000)")
        sys.exit(1)

    print("✅ 已连接到服务器")

    while True:
        choice = show_menu()

        if choice == '1':
            print("\n🎬 正在开始转写...")
            result = start_transcription()
            if result:
                print(f"✅ {result.get('status', '')}")

        elif choice == '2':
            print("\n📝 获取最新转写...")
            result = get_latest_transcription()
            if result and result['status'] == 'success':
                transcript = result.get('transcript')
                if transcript:
                    print(f"[{transcript['timestamp']}] {transcript['text']}")
                    print(f"置信度: {transcript['confidence']:.2%}")
                else:
                    print("暂无转写记录")

        elif choice == '3':
            print("\n📚 获取所有转写记录...")
            result = get_all_transcriptions()
            if result and result['status'] == 'success':
                count = result.get('count', 0)
                print(f"共 {count} 条记录:")
                print("=" * 50)
                for t in result.get('transcripts', []):
                    print(f"[{t['timestamp']}] {t['text']}")
                print("=" * 50)

        elif choice == '4':
            print("\n🔄 启动实时轮询...")
            poll_mode()

        elif choice == '5':
            print("\n📖 获取API信息...")
            try:
                response = requests.get(f"{API_BASE}/api/info")
                info = response.json()
                print(f"服务: {info.get('service', '')}")
                print(f"版本: {info.get('version', '')}")
                print("\n可用端点:")
                for category, endpoints in info.get('endpoints', {}).items():
                    print(f"\n{category.upper()}:")
                    if isinstance(endpoints, dict):
                        for endpoint, desc in endpoints.items():
                            print(f"  {endpoint}: {desc}")
            except Exception as e:
                print(f"❌ 获取失败: {str(e)}")

        elif choice == '0':
            print("\n👋 再见!")
            break

        else:
            print("⚠️ 无效选项，请重新选择")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已退出")
