from gtts import gTTS
import os
from mutagen.mp3 import MP3  # For reading MP3 durations

# Path to the subtitles file
subtitles_path = os.path.join("videos", "subtitles.csv")

def generate_speech_from_file(subtitles_path):
    mp3_lengths = []
    # Make sure the "mp3" folder exists
    if not os.path.exists("mp3"):
        os.makedirs("mp3")

    with open(subtitles_path, "r", encoding="utf-8") as subtitles_file:
        subtitles_lines = subtitles_file.readlines()

    for i, line in enumerate(subtitles_lines):
        line = line.strip()  # Remove leading/trailing whitespace and newlines
        if line:  # Skip empty lines
            tts = gTTS(text=line, lang='en', slow=False)
            file_path = os.path.join("mp3", f"line_{i+1}.mp3")
            tts.save(file_path)

            # Get MP3 duration
            audio = MP3(file_path)
            duration = audio.info.length  # in seconds (float)
            mp3_lengths.append(duration)

    return mp3_lengths