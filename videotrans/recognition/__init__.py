from typing import Union, List, Dict

from videotrans.configure import config
# 判断各个语音识别模式是否支持所选语言
# 支持返回True，不支持返回错误文字字符串
from videotrans.winform import zh_recogn as zh_recogn_win, recognapi as recognapi_win, \
    openairecognapi as openairecognapi_win, doubao as doubao_win
from ._average import FasterAvg
from ._doubao import DoubaoRecogn
from ._google import GoogleRecogn
from ._openai import OpenaiWhisperRecogn
from ._openairecognapi import OpenaiAPIRecogn
from ._overall import FasterAll
from ._recognapi import APIRecogn
from ._zh import ZhRecogn

# 数字代表界面中的现实顺序
FASTER_WHISPER = 0
OPENAI_WHISPER = 1
GOOGLE_SPEECH = 2
ZH_RECOGN = 3
DOUBAO_API = 4
CUSTOM_API = 5
OPENAI_API = 6

RECOGN_NAME_LIST = [
    config.uilanglist['faster model'],
    config.uilanglist['openai model'],
    "Google识别api" if config.defaulelang == 'zh' else "Google Speech API",
    "zh_recogn中文识别" if config.defaulelang == 'zh' else "zh_recogn only Chinese",
    "豆包模型识别" if config.defaulelang == 'zh' else "Doubao",
    "自定义识别API" if config.defaulelang == 'zh' else "Custom Recognition API",
    "OpenAI识别API" if config.defaulelang == 'zh' else "OpenAI Speech API"
]


def is_allow_lang(langcode: str = None, recogn_type: int = None):
    if recogn_type == ZH_RECOGN and langcode[:2] != 'zh':
        return 'zh_recogn 仅支持中文语音识别' if config.defaulelang == 'zh' else 'zh_recogn Supports Chinese speech recognition only'

    if recogn_type == DOUBAO_API and langcode[:2] not in ["zh", "en", "ja", "ko", "es", "fr", "ru"]:
        return '豆包语音识别仅支持中英日韩法俄西班牙语言，其他不支持'

    return True


# 自定义识别、openai-api识别、zh_recogn识别是否填写了相关信息和sk等
# 正确返回True，失败返回False，并弹窗
def is_input_api(recogn_type: int = None):
    if recogn_type == ZH_RECOGN and not config.params['zh_recogn_api']:
        zh_recogn_win.openwin()
        return False

    if recogn_type == CUSTOM_API and not config.params['recognapi_url']:
        recognapi_win.openwin()
        return False

    if recogn_type == OPENAI_API and not config.params['openairecognapi_key']:
        openairecognapi_win.openwin()
        return False
    if recogn_type == DOUBAO_API and not config.params['doubao_appid']:
        doubao_win.openwin()
        return False
    return True


# 统一入口
def run(*,
        split_type="all",
        detect_language=None,
        audio_file=None,
        cache_folder=None,
        model_name=None,
        inst=None,
        uuid=None,
        recogn_type: int = 0,
        is_cuda=None,
        task_type="masterwin"
        ) -> Union[List[Dict], None]:
    if config.exit_soft or (config.current_status != 'ing' and config.box_recogn != 'ing'):
        return
    if model_name.startswith('distil-'):
        model_name = model_name.replace('-whisper', '')
    kwargs = {
        "detect_language": detect_language,
        "audio_file": audio_file,
        "cache_folder": cache_folder,
        "model_name": model_name,
        "uuid": uuid,
        "inst": inst,
        "is_cuda": is_cuda,
        "task_type": task_type
    }
    if recogn_type == OPENAI_WHISPER:
        return OpenaiWhisperRecogn(**kwargs).run()
    if recogn_type == GOOGLE_SPEECH:
        return GoogleRecogn(**kwargs).run()
    if recogn_type == ZH_RECOGN:
        return ZhRecogn(**kwargs).run()
    if recogn_type == DOUBAO_API:
        return DoubaoRecogn(**kwargs).run()
    if recogn_type == CUSTOM_API:
        return APIRecogn(**kwargs).run()
    if recogn_type == OPENAI_API:
        return OpenaiAPIRecogn(**kwargs).run()
    if split_type == 'avg':
        return FasterAvg(**kwargs).run()
    return FasterAll(**kwargs).run()
