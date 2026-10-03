import requests

class ObsidianClient:
  def __init__(self,base_url: str,api_key: str,verify_ssl:bool = True,):
    self.base_url = base_url.rstrip("/")
    self.api_key = api_key
    self.verify_ssl = verify_ssl

  def create_note(self,path:str,content:str):
    url = f"{self.base_url}/vault/{path}"

    headers = {
      "Authorization": f"Bearer {self.api_key}",
      "Content-Type": "text/markdown",
    }

    response = requests.put(
      url,
      headers=headers,
      data=content.encode("utf-8"),
      verify=self.verify_ssl,
    )

    response.raise_for_status()
