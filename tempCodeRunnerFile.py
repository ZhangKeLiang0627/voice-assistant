el = whisper.load_model("tiny")
result = model.transcribe(r"test_8KHz.wav", fp16=False, language="Chinese")
print(result["text"])