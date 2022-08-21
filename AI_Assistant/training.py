from assistant_model import ModelAssistant

assitant = ModelAssistant('intents.json')
assitant.train_model()

assitant.save_model()