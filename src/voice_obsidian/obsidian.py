
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# class ObsidianClient:
#   def __init__(self):
#     self.api_key = os.getenv("OBSIDIAN_API_KEY")
#     self.url = os.getenv("OBSIDIAN_URL")
#     self.verify = os.getenv("OBSIDIAN_VERIFY_SSL","true").lower()=="true"

#   def create_folder(self,folder_path:str):
#     response = requests.put(
#       f"{self.url}/vault/{folder_path}",
#       headers={
#         "Authorization": f"Bearer {self.api_key}"
#       },
#       verify=self.verify
#     )
#     response.raise_for_status()
#     return response

class ObsidianClient:
  def __init__(self):
    self.vault_path=Path(os.getenv("OBSIDIAN_VAULT_PATH"))
    self.obsidian_vault_name = os.getenv("OBSIDIAN_VAULT_NAME")

  def create_folder(self,folder_path):
    path = self.vault_path/folder_path
    path.mkdir(parents=True,exist_ok=True)
    print("Папка создана")