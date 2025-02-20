import logging
from datetime import datetime
import threading
import time
import os
import base64
from database import Session, ChatMessage
from config import (
    DEEPSEEK_API_KEY, MAX_TOKEN, TEMPERATURE, MODEL, DEEPSEEK_BASE_URL,
    LISTEN_LIST, ZHIPU_API_KEY, ZHIPU_BASE_URL, ZHIPU_MODEL
)
from wxauto import WeChat
from openai import OpenAI
import requests


wx = WeChat()

# 设置监听列表
listen_list = LISTEN_LIST
for i in listen_list:
    wx.AddListenChat(who=i, savepic=True, savevoice=True)

wait = 1  # 1秒轮询新消息
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

root_dir = os.path.dirname(os.path.abspath(__file__))
user_queues = {}
queue_lock = threading.Lock()
chat_contexts = {}

with open(os.path.join(root_dir, 'prompt.md'), 'r', encoding='utf-8') as file:
    prompt_content = file.read()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def save_message(sender_id, sender_name, message, reply):
    try:
        session = Session()
        chat_message = ChatMessage(sender_id=sender_id, sender_name=sender_name, message=message, reply=reply)
        session.add(chat_message)
        session.commit()
        session.close()
    except Exception as e:
        logger.error(f"保存消息失败: {str(e)}")


def call_zhipu_api(image_path):
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        headers = {"Authorization": f"Bearer {ZHIPU_API_KEY}", "Content-Type": "application/json"}
        data = {"model": ZHIPU_MODEL, "image": base64_image}
        response = requests.post(f"{ZHIPU_BASE_URL}/v1/image-to-text", json=data, headers=headers)
        response_data = response.json()

        return response_data.get("text", "图片识别失败")
    except Exception as e:
        logger.error(f"调用智谱 API 失败: {str(e)}", exc_info=True)
        return "图片识别出错"


def get_deepseek_response(message, user_id):
    try:
        with queue_lock:
            if user_id not in chat_contexts:
                chat_contexts[user_id] = []
            chat_contexts[user_id].append({"role": "user", "content": message})

            MAX_GROUPS = 5
            while len(chat_contexts[user_id]) > MAX_GROUPS * 2:
                chat_contexts[user_id] = chat_contexts[user_id][2:]

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": prompt_content}, *chat_contexts[user_id][-MAX_GROUPS * 2:]],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKEN,
            stream=False
        )

        reply = response.choices[0].message.content if response.choices else "服务响应异常，请稍后再试"
        with queue_lock:
            chat_contexts[user_id].append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        logger.error(f"DeepSeek调用失败: {str(e)}", exc_info=True)
        return "调用失败"


def process_user_messages(user_id):
    with queue_lock:
        if user_id not in user_queues:
            return
        user_data = user_queues.pop(user_id)
        messages = user_data['messages']
        sender_name = user_data['sender_name']
        username = user_data['username']

    merged_message = ' \\ '.join(messages)
    reply = get_deepseek_response(merged_message, user_id)

    try:
        if '\\' in reply:
            for part in reply.split('\\'):
                wx.SendMsg(part.strip(), user_id)
                time.sleep(wait)
        else:
            wx.SendMsg(reply, user_id)
    except Exception as e:
        logger.error(f"发送回复失败: {str(e)} - 用户: {user_id}")
    save_message(username, sender_name, merged_message, reply)


def message_listener():
    while True:
        try:
            msgs = wx.GetListenMessage()
            for chat in msgs:
                who = chat.who
                if who in ["Self", "SYS"]:
                    continue  # 忽略自身消息和系统消息
                one_msgs = msgs.get(chat)
                for msg in one_msgs:
                    handle_wxauto_message(msg)
        except Exception as e:
            logger.error(f"消息监听出错: {str(e)}")
        time.sleep(wait)


def handle_wxauto_message(msg):
    try:
        username = msg.sender
        sender_name = username
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if msg.type == 'Picture':
            image_path = msg.content
            recognized_text = call_zhipu_api(image_path)
            message_content = f"[图片转文字结果]：{recognized_text}"
        elif msg.type == 'Voice':
            voice_text = wx.VoiceToText(msg)
            message_content = f"[语音转文字]：{voice_text}"
        else:
            content = getattr(msg, 'content', None) or getattr(msg, 'text', None)
            if not content:
                return
            message_content = f"[{current_time}] {content}"

        with queue_lock:
            if username not in user_queues:
                user_queues[username] = {
                    'timer': threading.Timer(7.0, process_user_messages, args=[username]),
                    'messages': [message_content],
                    'sender_name': sender_name,
                    'username': username
                }
                user_queues[username]['timer'].start()
            else:
                user_queues[username]['messages'].append(message_content)
    except Exception as e:
        logger.error(f"消息处理失败: {str(e)}")


def main():
    try:
        global wx
        wx = WeChat()
        listener_thread = threading.Thread(target=message_listener)
        listener_thread.daemon = True
        listener_thread.start()
        print("开始运行BOT...")
        while True:
            time.sleep(wait)
    except Exception as e:
        logger.error(f"发生异常: {str(e)}")
    finally:
        print("程序退出")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("用户终止")
    except Exception as e:
        logger.error(f"发生异常: {str(e)}", exc_info=True)