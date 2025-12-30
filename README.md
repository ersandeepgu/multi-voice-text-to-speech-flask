# multi-voice-text-to-speech-flask
A Flask-based multi-voice Text-to-Speech web app supporting Hindi &amp; English voices with emotion, pitch, and speed control using Microsoft Edge TTS and FFmpeg.

A powerful **Text-to-Speech (TTS) web application** built using **Flask** and **Microsoft Edge TTS**, supporting **multiple voices, languages, emotions, pitch, and speed control**.

This tool allows you to generate **high-quality MP3 audio** from text using **male & female voices** in **Hindi and English**, and even combine multiple lines into a single audio file.

---

## 🚀 Features

- ✅ Multi-line Text to Speech
- 🎙️ Male & Female voices
- 🌐 Languages supported:
  - Hindi (India)
  - English (India, US, UK)
- 🎭 Emotion control (Neutral, Sad, Cheerful, Angry, Excited)
- ⏱️ Speed control (Slow / Normal / Fast)
- 🎵 Pitch control (Low / Normal / High)
- 🔁 Automatic voice correction (Hindi text → Hindi voice)
- 🎧 Final combined MP3 output
- 🧩 FFmpeg-based audio merging

---

## 🛠 Tech Stack

- **Backend:** Python, Flask
- **TTS Engine:** Microsoft Edge TTS
- **Audio Processing:** FFmpeg
- **Frontend:** HTML, CSS, JavaScript
- **Async Processing:** asyncio

---

## 📸 UI Preview

![UI Preview
<img width="1460" height="417" alt="image" src="https://github.com/user-attachments/assets/d8d5c781-65c0-4a1d-8d99-4144fca45e9a" />


---

## ⚙️ Installation

```bash
pip install flask edge-tts

---

## Install FFmpeg:
Windows: https://ffmpeg.org/download.html

Linux:
sudo apt install ffmpeg

▶️ Run the App
python app.py

Open in browser:

http://127.0.0.1:5000
