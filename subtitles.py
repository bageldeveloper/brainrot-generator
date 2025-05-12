from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import os

def create_video(input_folder, output_folder):
    # Load the video clip
    video_path = os.path.join(input_folder, "vid.mp4")
    video_clip = VideoFileClip(video_path)

    # Load subtitles from the subtitles.txt file
    subtitles_path = os.path.join(input_folder, "subtitles.csv")
    with open(subtitles_path, "r", encoding="utf-8") as subtitles_file:
        subtitles_lines = subtitles_file.readlines()

    # Create TextClip for each subtitle
    subtitle_clips = []
    for i, line in enumerate(subtitles_lines):
        # bg_color = "black",
        caption_clip = TextClip(text=line.strip(), font="impact", font_size=48, color="white", stroke_color = "black", stroke_width=2, method="caption", size=(1000, None))
        caption_clip = caption_clip.with_position("center", "center")
        caption_clip = caption_clip.with_duration(video_clip.duration / len(subtitles_lines))
        caption_clip = caption_clip.with_start(i * (video_clip.duration / len(subtitles_lines)))
        subtitle_clips.append(caption_clip)

    # Combine all caption clips into a single CompositeVideoClip
    subtitles = CompositeVideoClip(subtitle_clips)

    # Overlay subtitles at the bottom of the video
    final_clip = CompositeVideoClip([video_clip, subtitles.with_position(("center", "bottom"))])

    # Write the final video
    output_path = os.path.join(output_folder, "output_video.mp4")
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)

# Example usage:
input_folder = "videos"
output_folder = "output"
create_video(input_folder, output_folder)