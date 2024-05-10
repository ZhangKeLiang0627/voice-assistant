# VoiceAssistant_DeployRecord
# 简易AI语音智能助手的部署记录
### Author：kkl
###  Project from：[voice-assistant](https://github.com/linyiLYi/voice-assistant) By linyiLYi

Original Markdown： [English](README-EN.md) | [简体中文](README-CN.md)
---

## 开始
背景：~~通过学习林哥的程序赶上林哥的步伐从而取代林哥~~，初步了解ASR+LLM+TTS的完整应用流程。

## 过程

- **克隆项目**文件到本地`git clone --recursive https://github.com/linyiLYi/voice-assistant`

- **环境配置** ，由于原项目的环境采用`Mac`，而作者的环境使用`Windows`，于是配置使用的命令和原项目稍微有一些区别（mlx使用openai-whisper替代，say使用pyttsx3替代。

```
# 环境配置
conda create -n VoiceAI python=3.11.5
conda activate VoiceAI
pip install -r requirements.txt # 注意请注释mlx，mlx是Mac的专有库
pip install llama-cpp-python

# 安装音频处理工具
pip install pyaudio

# 安装openai-whisper
pip install openai-whisper # 注意检查环境中是否安装ffmpeg

# 安装pyttsx3
pip install pyttsx3
```

> 关于遇到conda创建虚拟环境时报错的问题：

conda出现http429报错：CondaHTTPError: HTTP 429 TOO MANY REQUESTS for url ＜xxx＞，解决办法：https://blog.csdn.net/m0_67839004/article/details/137934614


> 关于安装openai-whisper的注意点：

1. 安装ffmpeg依赖，教程：https://blog.csdn.net/m0_61497715/article/details/129817641
2. 倘若发生报错：FileNotFoundError: [WinError 2] 系统找不到指定的文件。解决办法：https://blog.csdn.net/zdm_0301/article/details/133854913
3. openai-whisper使用cuda加速，需要修改torch为gpu版本，作者使用如下命令更新torch环境`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`，其他torch版本可以前往[torch官网](https://pytorch.org/)获取
4. **记得删除原项目当中的`whisper`文件夹！**

> 提供了两个test程序，可以方便测试openai-whisper和pyttsx3

- **获取模型**

Windows环境下，只需要获取llm的模型，模型文件存放于`models/`文件夹下，在脚本中通过变量`MODEL_PATH`指定。 推荐下载 TheBloke 与 XeIaso 的 gguf 格式模型，其中 6B 模型显存占用更小：
[yi-chat-6b.Q8_0.gguf](https://huggingface.co/XeIaso/yi-chat-6B-GGUF/blob/main/yi-chat-6b.Q8_0.gguf) or [yi-34b-chat.Q8_0.gguf](https://huggingface.co/TheBloke/Yi-34B-Chat-GGUF/blob/main/yi-34b-chat.Q8_0.gguf)

openai-whisper的模型可以根据自己的使用需求`('tiny', 'base', 'medium', 'large' ...)`来在线下载，如下
```python
# 修改load_model中的参数，执行程序会自动检查模型是否存在，模型不存在会自动开下载
import whisper

if __name__ == "__main__":
    file_path = "output.wav"
    model = whisper.load_model("base", device="cuda")
    result = model.transcribe(file_path, language="Chinese")
    print(result["text"])
```

- **文件创建**
请自行创建`models`和`recordings`文件夹。

## 运行

Windows环境下，对`main.py`有几处改动：

```python
# 1. 引入
import whisper
import pyttsx3
```

```python
# 2. 修改模型路径，这里选择6B的
# Model Configuration
WHISP_PATH = "models/whisper-large-v3"
MODEL_PATH = "models/yi-chat-6b.Q8_0.gguf"  # Or models/yi-34b-chat.Q8_0.gguf
```

```python
# 3. 用pyttsx3替换say命令
def text_to_speech(self, text):
        # 创建一个文本到语音转换器
        engine = pyttsx3.init()
        # 设置语速为200
        engine.setProperty("rate", 200)
        # 设置音量
        engine.setProperty("volume", 1.0)
        try:
            if LANG == "CN":
                engine.say(text)
                # 等待语音输出结束
                engine.runAndWait()
            else:
                engine.say(text)
                # 等待语音输出结束
                engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")

        engine.stop()
```

```python
# 4. 加载openai-whisper模型，一共两处修改，比较乱，具体见原代码
if __name__ == "__main__":
    if LANG == "CN":
        prompt_path = "prompts/example-cn.txt"
    else:
        prompt_path = "prompts/example-en.txt"
    
    # 1. 第一处
    whisper_model = whisper.load_model("base", device="cuda")  # 加载Whisper模型

    with open(prompt_path, "r", encoding="utf-8") as file:
        template = file.read().strip()  # {dialogue}
    prompt_template = PromptTemplate(template=template, input_variables=["dialogue"])

   # ...

    dialogue = ""
    try:
        while True:
            if voice_output_handler.tts_busy:  # Check if TTS is busy
                continue  # Skip to the next iteration if TTS is busy
            try:
                print("Listening...")
                record_audio()
                print("Transcribing...")
                time_ckpt = time.time()
                
                # user_input = whisper.transcribe("recordings/output.wav", path_or_hf_repo=WHISP_PATH)["text"]

                # 2. 第二处
                user_input = whisper_model.transcribe(
                    "recordings/output.wav", language="Chinese"
                )["text"] # 对录音做语音识别

                print(
                    "%s: %s (Time %d ms)"
                    % ("Guest", user_input, (time.time() - time_ckpt) * 1000)
                )

            # ...

```

## 鸣谢
~~这破项目怎么跑的怎么慢，破模型怎么这么蠢~~，感谢林哥linyiLYi，让我离拥有贾维斯又近了一步！同时对本文章中所有的教程的作者和报错问题的解决者表示衷心的感谢！






