import joblib

model_list1 = {
  "jarvis": "models/jarvis.joblib",
}

class IntentClassifier:
  def __init__(self,model_list:dict=model_list1,model_name:str = "jarvis"):
    self.model = joblib.load(model_list[model_name])

  def predict(self,text:str) ->str:
    return self.model.predict([text])
  
class EntityExtractor:
  def __init__(self):
    self.extractors = {
      "create_note": self._extract_note_name,
      "open_note": self._extract_note_name,
      "delete_note": self._extract_note_name,
      "navigate_folder": self._extract_foldere,
      "set_properity": self._extract_properity,
      "insert_image": self._extract_filename,
    }

  def extract(self,text:str,intent:str) -> dict:
    extractor = self.extractors.get(intent)

    if extractor in None:
      return {}
    
  # def _extract_note_name(self,text:str) -> dict:
#LABLES: 
# 1. NOTE
# 2. FOLDER
# 3. PROPERITY
# 4. VALUE 
# 5. FILE 
# 6. TEXT
# 7. TARGET
# 8. HEADING_LEVEL
# 9. FORMAT
# 10. POSITION 
 
