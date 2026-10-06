from .commands import ParsedCommand
from .obsidian import ObsidianClient

class Executor:
  def __init__(self,obsidian:ObsidianClient):
    self.obsidian = obsidian
    self.handlers = {
      "create_folder": self.create_folder,
      # "navigate_folder": self.navigate_folder,
      # "open_note": self.open_note,
      # "create_note": self.create_note,
      # "set_property": self.set_property,
      # "insert_text": self.insert_text,
      # "append_text": self.append_text,
      # "delete_text": self.delete_text,
      # "replace_text": self.replace_text,
      # "create_link": self.create_link,
      # "insert_image": self.insert_image,
    }

  def execute(self,command:ParsedCommand):
    handler = self.handlers.get(command.intent)

    if handler is None:
      raise ValueError(f"Unknown intent: {command.intent}")
    
    return handler(command)
  
  def create_folder(self,command):
    folder = command.entities["FOLDER"]
    
    return self.obsidian.create_folder(folder)
