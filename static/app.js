// Multi-language support for WhisprRT
const translations = {
    zh: {
        title: "WhisprRT",
        subtitle: "基于 Whisper 的本地实时语音转文字工具 • 完全离线运行 • 保护隐私",
        statusReady: "准备就绪",
        statusTranscribing: "正在转写...",
        copyAll: "复制全文",
        startTranscription: "开始转写",
        stopTranscription: "停止转写",
        clearRecords: "清空记录",
        saveText: "保存文字",
        settings: "设置",
        audioDevice: "音频设备",
        selectModel: "模型",
        language: "语言",
        chinese: "中文",
        english: "English",
        autoDetect: "自动检测",
        showTimestamp: "时间戳",
        showTimestampLabel: "显示",
        displayMode: "显示模式",
        segmentMode: "分段",
        continuousMode: "连续",
        usageGuide: "使用说明",
        usageSteps: [
            "选择音频输入设备",
            "选择合适的模型和语言",
            "点击\"开始转写\"按钮",
            "开始说话进行转写",
            "完成后点击\"停止转写\"",
            "可复制或保存转写结果"
        ],
        toastConnected: "连接成功",
        toastConnectedMsg: "已连接到服务器",
        toastStarted: "开始转写",
        toastStartedMsg: "语音转写已开始！",
        toastStopped: "停止转写",
        toastStoppedMsg: "语音转写已停止",
        toastCleared: "清空成功",
        toastClearedMsg: "转写记录已清空",
        toastSaved: "保存成功",
        toastSavedMsg: "文件已保存",
        toastCopied: "复制成功",
        toastCopiedMsg: "文本已复制到剪贴板",
        toastError: "错误",
        toastInfo: "提示",
        toastReconnect: "重新连接",
        toastReconnectMsg: "正在尝试重新连接...",
        toastThemeSwitched: "主题已切换",
        toastLightMode: "已切换到浅色模式",
        toastDarkMode: "已切换到深色模式",
        toastWelcomeBack: "欢迎回来",
        toastRestored: "已恢复",
        toastRecords: "条转写记录",
        toastNoContent: "没有可保存的内容",
        toastNoCopyContent: "没有可复制的内容",
        toastStopFirst: "请先停止转写再切换",
        toastAlreadyRunning: "语音转写已经在运行中",
        toastSettingsUpdated: "设置已更新",
        toastTimestampOn: "时间戳显示已开启",
        toastTimestampOff: "时间戳显示已关闭",
        loadingDevices: "加载中...",
        defaultDevice: "系统默认设备",
        modelTiny: "Tiny - 最快速度",
        modelBase: "Base - 基础模型",
        modelSmall: "Small - 平衡性能",
        modelLarge: "Large V3 Turbo - 最高精度"
    },
    en: {
        title: "WhisprRT",
        subtitle: "Local Real-time Speech-to-Text Tool Based on Whisper • Fully Offline • Privacy Protected",
        statusReady: "Ready",
        statusTranscribing: "Transcribing...",
        copyAll: "Copy All",
        startTranscription: "Start",
        stopTranscription: "Stop",
        clearRecords: "Clear",
        saveText: "Save",
        settings: "Settings",
        audioDevice: "Audio Device",
        selectModel: "Model",
        language: "Language",
        chinese: "中文",
        english: "English",
        autoDetect: "Auto Detect",
        showTimestamp: "Timestamp",
        showTimestampLabel: "Show",
        displayMode: "Display Mode",
        segmentMode: "Segments",
        continuousMode: "Continuous",
        usageGuide: "Usage Guide",
        usageSteps: [
            "Select audio input device",
            "Choose model and language",
            "Click 'Start' button",
            "Start speaking to transcribe",
            "Click 'Stop' when finished",
            "Copy or save transcription"
        ],
        toastConnected: "Connected",
        toastConnectedMsg: "Connected to server",
        toastStarted: "Started",
        toastStartedMsg: "Transcription started!",
        toastStopped: "Stopped",
        toastStoppedMsg: "Transcription stopped",
        toastCleared: "Cleared",
        toastClearedMsg: "Transcription records cleared",
        toastSaved: "Saved",
        toastSavedMsg: "File saved successfully",
        toastCopied: "Copied",
        toastCopiedMsg: "Text copied to clipboard",
        toastError: "Error",
        toastInfo: "Info",
        toastReconnect: "Reconnecting",
        toastReconnectMsg: "Attempting to reconnect...",
        toastThemeSwitched: "Theme Switched",
        toastLightMode: "Switched to light mode",
        toastDarkMode: "Switched to dark mode",
        toastWelcomeBack: "Welcome Back",
        toastRestored: "Restored",
        toastRecords: "transcription records",
        toastNoContent: "No content to save",
        toastNoCopyContent: "No content to copy",
        toastStopFirst: "Please stop transcription first",
        toastAlreadyRunning: "Transcription is already running",
        toastSettingsUpdated: "Settings Updated",
        toastTimestampOn: "Timestamp display enabled",
        toastTimestampOff: "Timestamp display disabled",
        loadingDevices: "Loading...",
        defaultDevice: "System Default Device",
        modelTiny: "Tiny - Fastest",
        modelBase: "Base - Basic",
        modelSmall: "Small - Balanced",
        modelLarge: "Large V3 Turbo - Highest Accuracy"
    }
};

// Get current language from localStorage or default to Chinese
let currentLang = localStorage.getItem('app_language') || 'zh';

// Translation function
function t(key) {
    const keys = key.split('.');
    let value = translations[currentLang];

    for (const k of keys) {
        value = value?.[k];
    }

    return value || key;
}

// Update UI language
function updateUILanguage() {
    // Update text elements
    document.querySelector('h1').textContent = t('title');
    document.querySelector('.subtitle').textContent = t('subtitle');

    // Update buttons
    document.querySelector('#startBtn').innerHTML = `<i class="bi bi-mic-fill"></i> ${t('startTranscription')}`;
    document.querySelector('#stopBtn').innerHTML = `<i class="bi bi-stop-fill"></i> ${t('stopTranscription')}`;
    document.querySelectorAll('.btn-secondary')[1].innerHTML = `<i class="bi bi-trash"></i> ${t('clearRecords')}`;
    document.querySelector('.btn-success').innerHTML = `<i class="bi bi-download"></i> ${t('saveText')}`;
    document.querySelector('.card-header .btn-secondary').innerHTML = `<i class="bi bi-clipboard"></i> ${t('copyAll')}`;

    // Update settings
    document.querySelectorAll('.card-header span')[1].innerHTML = `<i class="bi bi-gear-fill"></i> ${t('settings')}`;
    document.querySelectorAll('.form-label')[0].textContent = t('audioDevice');
    document.querySelectorAll('.form-label')[1].textContent = t('selectModel');
    document.querySelectorAll('.form-label')[2].textContent = t('language');
    document.querySelectorAll('.form-label')[3].textContent = t('showTimestamp');
    document.querySelector('.switch-label').textContent = t('showTimestampLabel');
    document.querySelectorAll('.form-label')[4].textContent = t('displayMode');

    // Update model options
    const modelSelect = document.getElementById('modelSelect');
    modelSelect.options[0].text = t('modelTiny');
    modelSelect.options[1].text = t('modelBase');
    modelSelect.options[2].text = t('modelSmall');
    modelSelect.options[3].text = t('modelLarge');

    // Update language options
    const langSelect = document.getElementById('languageSelect');
    langSelect.options[0].text = t('chinese');
    langSelect.options[1].text = t('english');
    langSelect.options[2].text = t('autoDetect');

    // Update display mode buttons
    const modeButtons = document.querySelectorAll('.mode-btn');
    modeButtons[0].textContent = t('segmentMode');
    modeButtons[1].textContent = t('continuousMode');

    // Update usage guide
    document.querySelectorAll('.card-header span')[2].innerHTML = `<i class="bi bi-question-circle-fill"></i> ${t('usageGuide')}`;
    const usageList = document.querySelector('.usage-list');
    usageList.innerHTML = '';
    t('usageSteps').forEach(step => {
        const li = document.createElement('li');
        li.textContent = step;
        usageList.appendChild(li);
    });

    // Update status text
    const statusText = document.getElementById('status-text');
    if (statusText.textContent === t('statusTranscribing') || statusText.textContent === translations.zh.statusTranscribing || statusText.textContent === translations.en.statusTranscribing) {
        statusText.textContent = t('statusTranscribing');
    } else {
        statusText.textContent = t('statusReady');
    }
}

// Switch language
function switchLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('app_language', lang);
    updateUILanguage();
}

// Toggle language function
function toggleLanguage() {
    const newLang = currentLang === 'zh' ? 'en' : 'zh';
    switchLanguage(newLang);
    document.getElementById('lang-icon').textContent = newLang === 'zh' ? 'EN' : '中';
    // Toast notification will be shown by the main script if needed
}

// Initialize language on load
function initLanguage() {
    const savedLang = localStorage.getItem('app_language') || 'zh';
    currentLang = savedLang;
    document.getElementById('lang-icon').textContent = savedLang === 'zh' ? 'EN' : '中';
    updateUILanguage();
}

// Export functions and variables for use in HTML
window.t = t;
window.switchLanguage = switchLanguage;
window.updateUILanguage = updateUILanguage;
window.toggleLanguage = toggleLanguage;
window.initLanguage = initLanguage;
window.getCurrentLang = function() {
    return currentLang;
};
