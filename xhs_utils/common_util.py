import os
import time
import random
import hashlib
import binascii

from loguru import logger
from dotenv import load_dotenv

_A1_CHARSET = 'abcdefghijklmnopqrstuvwxyz1234567890'


def load_env():
    load_dotenv()
    cookies_str = os.getenv('COOKIES')
    return cookies_str


def poisson_sleep(mean_ms: float = None):
    """
    基于泊松过程（指数分布）的随机请求间隔，模拟自然的人类行为，降低被识别为机器人的风险。
    指数分布具有无记忆性，每次间隔相互独立，比固定 delay 更接近真实用户。
    :param mean_ms: 平均延迟（毫秒）。默认读取环境变量 REQUEST_DELAY_MS，回退到 1500ms。
                    设为 0 或负数时跳过等待（便于本地调试/关闭限速）。
    """
    import math
    if mean_ms is None:
        try:
            mean_ms = float(os.getenv('REQUEST_DELAY_MS', 1500))
        except (TypeError, ValueError):
            mean_ms = 1500
    if mean_ms <= 0:
        return
    # 指数分布采样：-ln(U) * mean，U ∈ (0, 1] 以避免 log(0)
    delay = -math.log(1 - random.random()) * mean_ms / 1000
    # 限制上下界，避免极端短或极端长的等待
    delay = max(0.3, min(delay, mean_ms * 5 / 1000))
    time.sleep(delay)



def init():
    media_base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../datas/media_datas'))
    excel_base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../datas/excel_datas'))
    for base_path in [media_base_path, excel_base_path]:
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            logger.info(f'创建目录 {base_path}')
    cookies_str = load_env()
    base_path = {
        'media': media_base_path,
        'excel': excel_base_path,
    }
    return cookies_str, base_path


def generate_a1():
    ts_hex = hex(int(time.time() * 1000))[2:]
    random_str = ''.join(random.choices(_A1_CHARSET, k=30))
    a_part = ts_hex + random_str + '5' + '0' + '000'
    crc = binascii.crc32(a_part.encode()) & 0xFFFFFFFF
    return (a_part + str(crc))[:52]


def generate_web_id(a1):
    return hashlib.md5(a1.encode()).hexdigest()
