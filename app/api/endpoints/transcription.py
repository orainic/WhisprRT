"""
转写相关的API端点
"""
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.models.schemas import ModelRequest, LanguageRequest, TimestampRequest
from app.services.transcription import transcription_service
from app.services.whisper import whisper_service
from app.config import AVAILABLE_MODELS, ANTI_HALLUCINATION_CONFIG, HALLUCINATION_PATTERNS

router = APIRouter()

class AntiHallucinationConfigRequest(BaseModel):
    """反幻觉配置请求模型"""
    temperature: float = None
    no_speech_threshold: float = None
    confidence_threshold: float = None
    energy_threshold: float = None
    silence_threshold: float = None

@router.get('/models')
def get_models():
    """返回可用的模型列表"""
    return {
        "models": AVAILABLE_MODELS,
        "current": whisper_service.model_name
    }

@router.post('/change_model')
def change_model(request: ModelRequest):
    """
    切换Whisper模型
    
    Args:
        request: 包含模型名称的请求对象
    
    Returns:
        操作状态和消息
    """
    model_name = request.model
    
    if model_name not in AVAILABLE_MODELS:
        return {"status": "error", "message": f"不支持的模型: {model_name}"}
    
    if transcription_service.running:
        return {"status": "error", "message": "请先停止转写再切换模型"}
    
    try:
        whisper_service.load_model(model_name)
        return {"status": "success", "message": f"已切换到模型: {model_name}"}
    except Exception as e:
        return {"status": "error", "message": f"切换模型失败: {str(e)}"}

@router.post('/change_language')
def change_language(request: LanguageRequest):
    """
    切换转写语言
    
    Args:
        request: 包含语言代码的请求对象
    
    Returns:
        操作状态和消息
    """
    return transcription_service.set_language(request.language)

@router.get('/anti_hallucination_config')
def get_anti_hallucination_config():
    """
    获取当前反幻觉配置
    
    Returns:
        当前的反幻觉配置参数
    """
    return {
        "status": "success",
        "config": {
            "temperature": ANTI_HALLUCINATION_CONFIG["temperature"],
            "no_speech_threshold": ANTI_HALLUCINATION_CONFIG["no_speech_threshold"],
            "confidence_threshold": transcription_service.confidence_threshold,
            "energy_threshold": transcription_service.energy_threshold,
            "silence_threshold": transcription_service.silence_threshold,
            "zcr_threshold": transcription_service.zcr_threshold
        },
        "hallucination_patterns": HALLUCINATION_PATTERNS
    }

@router.post('/update_anti_hallucination_config')
def update_anti_hallucination_config(request: AntiHallucinationConfigRequest):
    """
    更新反幻觉配置参数
    
    Args:
        request: 包含要更新的配置参数的请求对象
    
    Returns:
        操作状态和消息
    """
    if transcription_service.running:
        return {"status": "error", "message": "请先停止转写再调整参数"}
    
    try:
        updated_params = []
        
        # 更新转写服务的参数
        if request.confidence_threshold is not None:
            if 0.0 <= request.confidence_threshold <= 1.0:
                transcription_service.confidence_threshold = request.confidence_threshold
                updated_params.append(f"confidence_threshold={request.confidence_threshold}")
            else:
                return {"status": "error", "message": "confidence_threshold 必须在 0.0 到 1.0 之间"}
        
        if request.energy_threshold is not None:
            if request.energy_threshold >= 0.0:
                transcription_service.energy_threshold = request.energy_threshold
                updated_params.append(f"energy_threshold={request.energy_threshold}")
            else:
                return {"status": "error", "message": "energy_threshold 必须大于等于 0.0"}
        
        if request.silence_threshold is not None:
            if request.silence_threshold >= 0.0:
                transcription_service.silence_threshold = request.silence_threshold
                updated_params.append(f"silence_threshold={request.silence_threshold}")
            else:
                return {"status": "error", "message": "silence_threshold 必须大于等于 0.0"}
        
        # 更新全局配置（影响新的 Whisper 转写调用）
        if request.temperature is not None:
            if 0.0 <= request.temperature <= 1.0:
                ANTI_HALLUCINATION_CONFIG["temperature"] = request.temperature
                updated_params.append(f"temperature={request.temperature}")
            else:
                return {"status": "error", "message": "temperature 必须在 0.0 到 1.0 之间"}
        
        if request.no_speech_threshold is not None:
            if 0.0 <= request.no_speech_threshold <= 1.0:
                ANTI_HALLUCINATION_CONFIG["no_speech_threshold"] = request.no_speech_threshold
                updated_params.append(f"no_speech_threshold={request.no_speech_threshold}")
            else:
                return {"status": "error", "message": "no_speech_threshold 必须在 0.0 到 1.0 之间"}
        
        if updated_params:
            message = f"已更新参数: {', '.join(updated_params)}"
        else:
            message = "没有参数被更新"
        
        return {"status": "success", "message": message}
        
    except Exception as e:
        return {"status": "error", "message": f"更新配置失败: {str(e)}"}

@router.post('/reset_anti_hallucination_config')
def reset_anti_hallucination_config():
    """
    重置反幻觉配置为默认值
    
    Returns:
        操作状态和消息
    """
    if transcription_service.running:
        return {"status": "error", "message": "请先停止转写再重置参数"}
    
    try:
        # 重置为默认配置
        default_config = {
            "temperature": 0.0,
            "no_speech_threshold": 0.6,
            "condition_on_previous_text": False,
            "compression_ratio_threshold": 2.4,
            "log_prob_threshold": -1.0,
            "initial_prompt": "请只转写实际听到的语音内容，忽略背景音乐和噪音。不要生成广告或重复内容。",
            "energy_threshold": 0.02,
            "confidence_threshold": 0.6,
            "silence_threshold": 0.005,
            "zcr_threshold": 0.1,
        }
        
        # 更新全局配置
        ANTI_HALLUCINATION_CONFIG.update(default_config)
        
        # 更新转写服务配置
        transcription_service.energy_threshold = default_config["energy_threshold"]
        transcription_service.confidence_threshold = default_config["confidence_threshold"]
        transcription_service.silence_threshold = default_config["silence_threshold"]
        transcription_service.zcr_threshold = default_config["zcr_threshold"]
        
        return {"status": "success", "message": "反幻觉配置已重置为默认值"}
        
    except Exception as e:
        return {"status": "error", "message": f"重置配置失败: {str(e)}"}

@router.get('/status')
def get_status():
    """
    获取转写服务状态

    Returns:
        当前转写服务的运行状态
    """
    return {
        "status": "success",
        "running": transcription_service.running,
        "model": whisper_service.model_name,
        "language": transcription_service.current_language
    }

@router.get('/start')
def start_listening():
    """
    开始语音转写

    Returns:
        操作状态
    """
    return transcription_service.start()

@router.get('/stop')
def stop_listening():
    """
    停止语音转写
    
    Returns:
        操作状态
    """
    return transcription_service.stop()

@router.get('/clear')
def clear_transcription():
    """
    清空转写记录
    
    Returns:
        操作状态
    """
    return transcription_service.clear()

@router.get('/save')
def save_transcription():
    """
    保存转写结果
    
    Returns:
        文件下载响应
    """
    file_path = transcription_service.save()
    if isinstance(file_path, str):
        return FileResponse(file_path, filename="transcript_output.txt")
    return file_path

@router.post('/toggle_timestamp')
def toggle_timestamp_display(request: TimestampRequest):
    """
    切换时间戳显示

    Args:
        request: 包含时间戳显示设置的请求对象

    Returns:
        操作状态和消息
    """
    return {"status": "success", "message": f"时间戳显示已设置为: {request.show_timestamp}"}

@router.post('/change_display_mode')
def change_display_mode(request: dict):
    """
    切换显示模式

    Args:
        request: 包含显示模式的请求对象

    Returns:
        操作状态和消息
    """
    mode = request.get('mode')
    return transcription_service.set_display_mode(mode)

@router.get('/api/transcripts')
def get_transcripts():
    """
    获取所有转写记录 - 外部API接口

    Returns:
        所有转写记录的列表
    """
    return {
        "status": "success",
        "count": len(transcription_service.transcript),
        "transcripts": transcription_service.transcript
    }

@router.get('/api/latest')
def get_latest_transcript():
    """
    获取最新的转写记录 - 外部API接口

    Returns:
        最新的转写记录
    """
    if transcription_service.transcript:
        latest = transcription_service.transcript[-1]
        return {
            "status": "success",
            "transcript": latest
        }
    return {
        "status": "success",
        "transcript": None,
        "message": "暂无转写记录"
    }

@router.get('/api/transcripts/since/{timestamp}')
def get_transcripts_since(timestamp: str):
    """
    获取指定时间戳之后的转写记录 - 外部API接口

    Args:
        timestamp: 时间戳格式 HH:MM:SS

    Returns:
        指定时间之后的转写记录
    """
    filtered_transcripts = [
        t for t in transcription_service.transcript
        if t.get('timestamp', '') > timestamp
    ]
    return {
        "status": "success",
        "count": len(filtered_transcripts),
        "transcripts": filtered_transcripts
    }

@router.get('/api/info')
def get_api_info():
    """
    获取API信息和使用说明

    Returns:
        API信息
    """
    return {
        "status": "success",
        "version": "2.0.0",
        "service": "WhisprRT Real-time Transcription API",
        "endpoints": {
            "websocket": {
                "url": "ws://localhost:8000/ws",
                "description": "实时WebSocket连接，推送转写结果",
                "events": {
                    "status": "连接状态和配置信息",
                    "transcription": "实时转写结果",
                    "error": "错误信息"
                }
            },
            "rest": {
                "/api/info": "获取API信息",
                "/api/transcripts": "获取所有转写记录",
                "/api/latest": "获取最新转写记录",
                "/api/transcripts/since/{timestamp}": "获取指定时间后的记录"
            },
            "control": {
                "/status": "获取服务状态",
                "/start": "开始转写",
                "/stop": "停止转写",
                "/clear": "清空记录"
            }
        },
        "examples": {
            "websocket": "参见 /api/examples/websocket",
            "rest": "参见 /api/examples/rest",
            "python": "参见 /api/examples/python"
        }
    }