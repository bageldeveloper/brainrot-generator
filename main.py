from gpt4all import GPT4All
import personalities
import os
import csv
import random
import re
from subtitles import create_video

def split_into_sentences(text):
    # Split text by sentence boundaries (. ! ?) followed by space(s)
    sentence_endings = re.compile(r'(?<=[.!?]) +')
    sentences = sentence_endings.split(text)
    return [s.strip() for s in sentences if s.strip()]

# Ensure the videos directory exists
os.makedirs("videos", exist_ok=True)

# Use absolute path to your model file
model_path = os.path.abspath("models/greg.gguf")

# Load the model from local file
model = GPT4All(model_path)

with model.chat_session():
    personality = personalities.personality[input("What personality do you want to use? ")]
    story = input("What do you want the AI to talk about? ")

    print("Generating response...")

    # Generate AI response, limited to ~250 tokens and 1000 characters max in prompt instructions
    response = model.generate(
        personality +
    "\n\nTopic: " + story + "(keep the story under 256 characters)\n\n",
        max_tokens=256,
        temp=1
    ) + "\nRemember to like and subscribe!"
    print(response)

    # Split response into sentences for subtitles
    subtitle_chunks = split_into_sentences(response)

    # Write sentences to subtitles CSV file
    with open("videos/subtitles.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for chunk in subtitle_chunks:
            writer.writerow([chunk])

    # Create video using subtitles
    input_folder = "videos"
    output_folder = "output"
    create_video(input_folder, output_folder)
