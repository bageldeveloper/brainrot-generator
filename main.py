from gpt4all import GPT4All
import personalities
import os
import csv
import random
from subtitles import create_video

def split_into_chunks(text, max_chars=20):
    """Split text into chunks of approximately max_chars without cutting words."""
    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        # Check if adding this word would exceed the limit
        if len(current_chunk) + len(word) + 1 > max_chars and current_chunk:
            # Add current chunk to our list and start a new one
            chunks.append(current_chunk.strip())
            current_chunk = word
        else:
            # Add the word to the current chunk with a space if needed
            if current_chunk:
                current_chunk += " " + word
            else:
                current_chunk = word

    # Don't forget the last chunk if there is one
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# Ensure the videos directory exists
os.makedirs("videos", exist_ok=True)

# Initialize the model
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")  # downloads / loads a 4.66GB LLM

with model.chat_session():
    personality = personalities.personality[input("What personality do you want to use? ")]
    story = input("What do you want the AI to talk about? ")

    # Generate the response
    response = model.generate(personality + story + "(Your response much be under 250 characters)", max_tokens=250, temp=random.randint(50, 75))

    # Split the response into chunks of approximately 20 characters
    subtitle_chunks = split_into_chunks(response)

    # Write the chunks to the CSV file
    with open("videos/subtitles.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write each chunk as a row in the CSV
        for chunk in subtitle_chunks:
            writer.writerow([chunk])

    input_folder = "videos"
    output_folder = "output"
    create_video(input_folder, output_folder)