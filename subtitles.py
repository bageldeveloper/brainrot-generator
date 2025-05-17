from moviepy import (
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    CompositeAudioClip,
    AudioFileClip,
    ColorClip
)
import os
from speech import generate_speech_from_file  # Your gTTS + MP3 duration generator
import csv
import random

def create_video(input_folder, output_folder):
    # Target resolution (portrait)
    target_width, target_height = 360, 640

    # Load subtitle lines (sentences)
    subtitles_path = os.path.join(input_folder, "subtitles.csv")
    with open(subtitles_path, "r", encoding="utf-8") as f:
        subtitle_sentences = [line.strip() for line in f if line.strip()]

    # Generate MP3s per sentence
    temp_sentence_path = os.path.join(input_folder, "sentences.csv")
    with open(temp_sentence_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for sentence in subtitle_sentences:
            writer.writerow([sentence])

    mp3_durations = generate_speech_from_file(temp_sentence_path)
    if len(mp3_durations) != len(subtitle_sentences):
        raise ValueError("Mismatch between sentence count and MP3 durations.")

    total_subtitle_duration = sum(mp3_durations)

    # Load and resize video
    video_path = os.path.join(input_folder, "vid.mp4")
    video_clip = VideoFileClip(video_path).subclipped(0, total_subtitle_duration)
    video_clip = video_clip.resized(height=target_height)

    # Black background centered
    background = ColorClip(size=(target_width, target_height), color=(0, 0, 0), duration=video_clip.duration)
    video_clip = CompositeVideoClip([background, video_clip.with_position("center")])

    # Generate subtitle chunks (2-word) for each sentence, but sync to full sentence audio
    subtitle_clips = []
    audio_clips = []
    current_start = 0

    for i, (sentence, duration) in enumerate(zip(subtitle_sentences, mp3_durations)):
        words = sentence.split()
        duration-=0.5
        chunks = [" ".join(words[j:j + 2]) for j in range(0, len(words), 2)]

        chunk_start = current_start
        for chunk in chunks:
            chunk_duration = duration * (len(chunk.split()) / len(words))

            subtitle = TextClip(
                text=chunk,
                font="impact",
                font_size=40,
                color="white",
                stroke_color="black",
                stroke_width=2,
                size=(target_width - 40, None),
                method="caption"
            ).with_position(("center", target_height/2)).with_duration(chunk_duration).with_start(chunk_start)

            subtitle_clips.append(subtitle)
            chunk_start += chunk_duration

        mp3_path = os.path.join("mp3", f"line_{i + 1}.mp3")
        audio = AudioFileClip(mp3_path).with_start(current_start)
        audio_clips.append(audio)

        current_start += duration

    # Load background music if available
    randomNum = str(random.randint(1, 3))
    bg_music_path = os.path.join(input_folder, "music" + randomNum + ".mp3")
    if os.path.exists(bg_music_path):
        background_music = AudioFileClip(bg_music_path).with_duration(video_clip.duration)
        combined_audio = CompositeAudioClip(audio_clips + [background_music])
    else:
        combined_audio = CompositeAudioClip(audio_clips)

    subtitle_layer = CompositeVideoClip(subtitle_clips, size=(target_width, target_height))
    final_video = CompositeVideoClip([video_clip, subtitle_layer], size=(target_width, target_height))
    final_video = final_video.with_audio(combined_audio)

    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "output_video.mp4")
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)
