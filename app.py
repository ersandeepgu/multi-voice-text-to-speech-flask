from flask import Flask, render_template, request, send_file
import os, asyncio, uuid, shutil, subprocess, re
import edge_tts

app = Flask(__name__)

OUTPUT = "static/output"
os.makedirs(OUTPUT, exist_ok=True)

FFMPEG = shutil.which("ffmpeg")
if not FFMPEG:
    raise RuntimeError("FFmpeg not found")

# Fallback voices (SAFE)
HINDI_VOICE = "hi-IN-MadhurNeural"
ENGLISH_VOICE = "en-US-GuyNeural"

def is_hindi(text):
    return bool(re.search(r'[\u0900-\u097F]', text))

def safe_rate_pitch(emotion):
    # SAFE VALUES ONLY
    if emotion == "sad":
        return "-10%", "-3Hz"
    if emotion == "angry":
        return "+8%", "+3Hz"
    if emotion == "cheerful":
        return "+5%", "+2Hz"
    if emotion == "excited":
        return "+10%", "+3Hz"
    return "+0%", "+0Hz"

async def generate_voice(text, voice, emotion, out_file):
    if not text.strip():
        return False

    # Auto-correct voice if mismatch
    if is_hindi(text) and not voice.startswith("hi-"):
        voice = HINDI_VOICE
    if not is_hindi(text) and voice.startswith("hi-"):
        voice = ENGLISH_VOICE

    rate, pitch = safe_rate_pitch(emotion)

    try:
        communicate = edge_tts.Communicate(
            text=text.strip(),
            voice=voice,
            rate=rate,
            pitch=pitch
        )
        await communicate.save(out_file)
        return True
    except edge_tts.exceptions.NoAudioReceived:
        print(f"Skipped (no audio): {text[:30]}...")
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    raw = request.form.get("entry")
    if not raw:
        return "No input", 400

    uid = str(uuid.uuid4())
    base = os.path.abspath(OUTPUT)
    list_file = os.path.join(base, f"{uid}.txt")

    rows = raw.split("||")

    async def process():
        with open(list_file, "w", encoding="utf-8") as f:
            index = 0
            for row in rows:
                role, voice, rate, pitch, emotion, text = row.split("::")

                mp3 = os.path.join(base, f"{uid}_{index}.mp3")
                success = await generate_voice(text, voice, emotion, mp3)

                if success and os.path.exists(mp3):
                    f.write(f"file '{mp3}'\n")
                    index += 1

    asyncio.run(process())

    final_mp3 = os.path.join(base, f"{uid}_final.mp3")

    subprocess.run([
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c:a", "libmp3lame",
        "-q:a", "2",
        final_mp3
    ], check=True)

    return send_file(
        final_mp3,
        as_attachment=True,
        download_name="Audio.mp3",
        mimetype="audio/mpeg"
    )

if __name__ == "__main__":
    app.run(debug=True)
