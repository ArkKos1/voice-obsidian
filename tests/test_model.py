from voice_obsidian.nlp import IntentClassifier

classifier = IntentClassifier()

test = [
    ""
]

for text in test:
  print(f"{text} -> {classifier.predict(text)}")