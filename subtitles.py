from moviepy import (
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    CompositeAudioClip,
    AudioFileClip
)
import os
from speech import generate_speech_from_file  # Your gTTS + MP3 duration generator


def create_video(input_folder, output_folder):
    # Load video
    video_path = os.path.join(input_folder, "vid.mp4")
    video_clip = VideoFileClip(video_path)

    # Get video dimensions
    width, height = video_clip.size

    # Load subtitle lines
    subtitles_path = os.path.join(input_folder, "subtitles.csv")
    with open(subtitles_path, "r", encoding="utf-8") as f:
        subtitles_lines = [line.strip() for line in f if line.strip()]

    # Generate MP3s and get durations
    mp3_durations = generate_speech_from_file(subtitles_path)

    if len(mp3_durations) != len(subtitles_lines):
        raise ValueError("Mismatch between subtitle lines and MP3 durations.")

    subtitle_clips = []
    audio_clips = []
    current_start = 0

    for i, (text, duration) in enumerate(zip(subtitles_lines, mp3_durations)):
        # Create subtitle TextClip
        subtitle = TextClip(
            text=text,
            font="impact",
            font_size=48,
            color="white",
            stroke_color="black",
            stroke_width=2
        )

        # Set position to center of screen
        subtitle = subtitle.with_position(('center', 'center')).with_duration(duration).with_start(current_start)

        subtitle_clips.append(subtitle)

        # Load corresponding audio
        mp3_path = os.path.join("mp3", f"line_{i + 1}.mp3")
        audio = AudioFileClip(mp3_path).with_start(current_start)
        audio_clips.append(audio)

        current_start += duration

    # Combine all subtitle text clips
    subtitle_layer = CompositeVideoClip(subtitle_clips, size=video_clip.size)

    # Combine all audio clips
    combined_audio = CompositeAudioClip(audio_clips)

    # Overlay video + subtitles + audio
    final_video = CompositeVideoClip([video_clip, subtitle_layer])
    final_video = final_video.with_audio(combined_audio)

    # Write the output video
    output_path = os.path.join(output_folder, "output_video.mp4")
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)


# Example usage
input_folder = "videos"
output_folder = "output"
create_video(input_folder, output_folder)