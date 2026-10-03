import os

from dotenv import load_dotenv

from voice_obsidian.obsidian import ObsidianClient

load_dotenv()

obsidian_url = os.getenv("OBSIDIAN_URL")
obsidian_api_key = os.getenv("OBSIDIAN_API_KEY")
obsidian_verify_ssl = os.getenv(
    "OBSIDIAN_VERIFY_SSL",
    "true",
).lower() == "true"

if not obsidian_url or not obsidian_api_key:
  raise RuntimeError("OBSIDIAN_KEY or OBSIDIAN_API_KEY is not set")

client = ObsidianClient(
  base_url=obsidian_url,
  api_key=obsidian_api_key,
  verify_ssl=obsidian_verify_ssl
)

client.append_to_note(
  "Test.md",
  "\n\nДобавил хуету")



print("Note created successfully")