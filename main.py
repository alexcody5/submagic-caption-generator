import os
import whisper

# ----------------- CONFIG -----------------
INPUT_FILE = "example.mp4"  # Rename or replace with your video/audio file
OUTPUT_DIR = "outputs"
STYLED_CAPTION_PATH = os.path.join(OUTPUT_DIR, "styled_captions.ass")

def transcribe_audio(filepath):
    print("🔍 Transcribing...")
    model = whisper.load_model("base")
    result = model.transcribe(filepath, word_timestamps=True)
    print("✅ Transcription complete.")
    return result['segments']

def emphasize_words(segments):
    styled_segments = []
    for seg in segments:
        words = seg.get("words", [])
        styled_words = []
        for word in words:
            text = word['word']
            # Apply basic emphasis rules (customize these as needed)
            if text.isupper() or '*' in text or len(text.strip()) > 6:
                style = "bold"
            else:
                style = "normal"
            styled_words.append({
                "start": word['start'],
                "end": word['end'],
                "text": text.strip("*"),
                "style": style
            })
        styled_segments.append(styled_words)
    return styled_segments

def export_ass(styled_segments, output_path):
    print("🎬 Exporting .ass styled captions...")
    with open(output_path, "w") as f:
        f.write("[Script Info]\nTitle: Styled Captions\n\n[V4+ Styles]\n")
        f.write("Format: Name, Fontname, Fontsize, PrimaryColour, Bold, Italic, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write("Style: bold,Arial,60,&H00FF9900,-1,0,2,20,20,20,0\n")  # Orange bold
        f.write("Style: normal,Arial,48,&H00FFFFFF,0,0,2,20,20,20,0\n")  # White regular
        f.write("\n[Events]\nFormat: Start, End, Style, Text\n")
        for segment in styled_segments:
            for word in segment:
                start = format_time(word["start"])
                end = format_time(word["end"])
                f.write(f"Dialogue: 0,{start},{end},{word['style']},{word['text']}\n")
    print(f"✅ Done! Captions saved to {output_path}")

def format_time(t):
    hrs = int(t // 3600)
    mins = int((t % 3600) // 60)
    secs = int(t % 60)
    ms = int((t % 1) * 100)
    return f"{hrs:d}:{mins:02d}:{secs:02d}.{ms:02d}"

# ----------------- RUN -----------------
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(INPUT_FILE):
        print(f"❌ File not found: {INPUT_FILE}")
        exit(1)

    segments = transcribe_audio(INPUT_FILE)
    styled = emphasize_words(segments)
    export_ass(styled, STYLED_CAPTION_PATH)

