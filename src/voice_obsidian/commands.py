from dataclasses import dataclass

@dataclass
class ParsedCommand:
  intent: str
  entities: dict