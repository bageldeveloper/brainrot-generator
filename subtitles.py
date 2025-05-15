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

def create_video(input_folder, output_folder):
    # Target resolution (portrait)
    target_width, target_height = 1080, 1920

    # Load subtitle lines
    subtitles_path = os.path.join(input_folder, "subtitles.csv")
    with open(subtitles_path, "r", encoding="utf-8") as f:
        subtitles_lines = [line.strip() for line in f if line.strip()]

    # Generate MP3s and get durations
    mp3_durations = generate_speech_from_file(subtitles_path)
    if len(mp3_durations) != len(subtitles_lines):
        raise ValueError("Mismatch between subtitle lines and MP3 durations.")

    # Calculate total duration of all subtitles
    total_subtitle_duration = sum(mp3_durations)

    # Load video and trim it to subtitle duration
    video_path = os.path.join(input_folder, "vid.mp4")
    video_clip = VideoFileClip(video_path).subclipped(0, total_subtitle_duration)

    # Resize and fit video to 1080x1920 (portrait)
    video_clip = video_clip.resized(height=target_height)

    # Create black background and center the video on it
    background = ColorClip(size=(target_width, target_height), color=(0, 0, 0), duration=video_clip.duration)
    video_clip = CompositeVideoClip([background, video_clip.with_position("center")])

    # Create subtitle and audio clips
    subtitle_clips = []
    audio_clips = []
    current_start = 0

    for i, (text, duration) in enumerate(zip(subtitles_lines, mp3_durations)):
        # Create subtitle TextClip
        subtitle = TextClip(
            text=text,
            font="impact",
            font_size=96,
            color="white",
            stroke_color="black",
            stroke_width=2,
            size=(target_width - 100, None),
            method="caption"
        ).with_position(("center", "center")).with_duration(duration).with_start(current_start)
        subtitle_clips.append(subtitle)

        # Load corresponding speech audio
        mp3_path = os.path.join("mp3", f"line_{i + 1}.mp3")
        audio = AudioFileClip(mp3_path).with_start(current_start)
        audio_clips.append(audio)

        current_start += duration

    # Load background music and set its duration to match the video
    bg_music_path = os.path.join(input_folder, "music.mp3")
    background_music = AudioFileClip(bg_music_path).with_duration(video_clip.duration)

    # Combine all speech audio clips and background music
    combined_audio = CompositeAudioClip(audio_clips + [background_music])

    # Create subtitle layer
    subtitle_layer = CompositeVideoClip(subtitle_clips, size=(target_width, target_height))

    # Final video composition
    final_video = CompositeVideoClip([video_clip, subtitle_layer], size=(target_width, target_height))
    final_video = final_video.with_audio(combined_audio)

    # Export final video
    output_path = os.path.join(output_folder, "output_video.mp4")
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)