from voice_obsidian.nlp import IntentClassifier

classifier = IntentClassifier()

test = [
    "создай заметку Тёмнолесье",
    "открой заметку Империя Леория",
    "перейди в папку Социум",
    "поставь население 13400",
]

for text in test:
  print(f"{text} -> {classifier.predict(text)}")