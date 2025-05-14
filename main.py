from gpt4all import GPT4All
import personalities

model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf") # downloads / loads a 4.66GB LLM
with model.chat_session():
    personality = personalities.personality[input("What personality do you want to use? ")]
    story = input("What do you want the AI to talk about? ")
    print(model.generate(personality + story, max_tokens=1024, temp=20))