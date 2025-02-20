# 用户列表 (请配置要和 bot 交互的账号的**昵称**，不要写备注！)
LISTEN_LIST = ['和泉']

# ================== DeepSeek API 配置（用于文本对话） ==================
DEEPSEEK_API_KEY = 'sk-nafetebktnfghzuoqallhlbcgzzioqdzapevtljocmlnljaw'  # 你的 DeepSeek API Key
DEEPSEEK_BASE_URL = 'https://api.siliconflow.cn/v1/'  # 硅基流动 API

# 如果要使用 DeepSeek 官方 API，请取消下面一行的注释
# DEEPSEEK_BASE_URL = 'https://api.deepseek.com'

# 硅基流动 API 使用的 V3 模型
MODEL = 'deepseek-ai/DeepSeek-V3'

# 如果使用官方 API，则模型名应改为：
# MODEL = 'deepseek-chat'

# 回复最大 Token 数量（控制 AI 回复的长度）
MAX_TOKEN = 2000

# 温度参数（控制 AI 生成文本的随机性，越高越随机）
TEMPERATURE = 1.4

# 是否启用语音识别（True = 开启，False = 关闭）
ENABLE_VOICE_RECOGNITION = True

# ================== 智谱 API 配置（用于图片识别） ==================
ZHIPU_API_KEY = '366da5c5c7b84c7eb7222a7bcbea1206.wei7eK4dSVyqCWvl'  # 你的智谱 API Key
ZHIPU_BASE_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'  # 智谱 API 地址

# 指定使用 GLM-4V-Flash（仅用于图片文本提取）
ZHIPU_MODEL = "glm-4v-flash"

MESSAGE_QUEUE_TIMEOUT = 5
