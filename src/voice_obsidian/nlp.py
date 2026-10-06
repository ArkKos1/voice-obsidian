import joblib
import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer

model_list1 = {
  "jarvis": "models/jarvis.joblib",
}

LABELS = [
    "O",
    "B-NOTE",
    "I-NOTE",
    "B-FOLDER",
    "I-FOLDER",
    "B-PROPERTY",
    "I-PROPERTY",
    "B-VALUE",
    "I-VALUE",
    "B-FILE",
    "I-FILE",
    "B-TEXT",
    "I-TEXT",
    "B-HEADING",
    "I-HEADING",
    "B-FORMAT",
    "I-FORMAT",
    "B-POSITION",
    "I-POSITION",
]


class IntentClassifier:
  def __init__(self,model_list:dict=model_list1,model_name:str = "jarvis"):
    self.model = joblib.load(model_list[model_name])

  def predict(self,text:str) ->str:
    return self.model.predict([text])
  

    
class EntityExtractorModel:
  def __init__(self, model_path:str, labels:list = LABELS):
    num_labels = len(labels)
    self.LABEL2ID = {label:i for i,label in enumerate(labels)}
    self.LABELS = labels
    self.ID2LABEL = {i:label for i,label in enumerate(labels)}
    self.model = AutoModelForTokenClassification.from_pretrained(
      model_path,
      num_labels=num_labels,
      label2id=self.LABEL2ID,
      id2label=self.ID2LABEL
    )
    self.tokenizer = AutoTokenizer.from_pretrained(model_path)
  
  def predict(self,text: str):
    encoded = self.tokenizer(
      text,
      return_offsets_mapping=True,
      return_tensors="pt",
      truncation=True
    )
    offsets = encoded.pop("offset_mapping")[0]

    with torch.no_grad():
      outputs = self.model(**encoded)
    probabilities = torch.softmax(outputs.logits,dim=-1)
    predictions = probabilities.argmax(dim=-1)[0]

    result = {}
    current_label = None
    start = None
    end = None
    confidences = []
    

    for prediction,offset,probs in zip(predictions,offsets,probabilities[0]):
      token_start,token_end = offset.tolist()

      if token_start==token_end:
        continue
      label = self.ID2LABEL[prediction.item()]
      confidence = probs[prediction].item()

      if label.startswith("B-"):
        if current_label:
          result[current_label] = text[start:end]
        current_label = label[2:]
        start = token_start
        end=token_end
        confidences = [confidence]

      elif label.startswith("I-"):
        end=token_end
        confidences.append(confidence)

      else:
        if current_label:
          if min(confidences) <0.5:
            return {}
          result[current_label]=text[start:end]
          current_label=None
          start = None
          end=None
          confidences = []

    if current_label:
      if min(confidences) < 0.5:
        return {}
      result[current_label] = text[start:end]
    
    return result
 
