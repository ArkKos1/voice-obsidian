from .nlp import IntentClassifier,EntityExtractorModel
from .commands import ParsedCommand
from .executor import Executor
from .obsidian import ObsidianClient
from .context import Context

obsidian = ObsidianClient()
intent_classifier = IntentClassifier()
entity_extractor = EntityExtractorModel(model_path="models/entity_extractor1")
executor = Executor(obsidian=obsidian)

while True:
  text = input("Команда:")

  if text == "exit" or text == "выход":
    break
  intent = intent_classifier.predict(text)[0]
  entities = entity_extractor.predict(text)
  command = ParsedCommand(
    intent=intent,
    entities=entities
  )

  executor.execute(command)