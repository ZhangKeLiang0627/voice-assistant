import whisper

if __name__ == "__main__":
    file_path = "test.wav"
    model = whisper.load_model("base", device="cuda")
    result = model.transcribe(file_path, language="Chinese")
    print(result["text"])

