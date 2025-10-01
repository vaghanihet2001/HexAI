from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create and train chatbot
bot = ChatBot("AssistantBot", read_only=True)
trainer = ChatterBotCorpusTrainer(bot)

# Train on English small talk
trainer.train("chatterbot.corpus.english")

def get_chatbot_reply(text):
    response = bot.get_response(text)
    return str(response)
