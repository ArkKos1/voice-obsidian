from dataclasses import dataclass


@dataclass
class Entity:
  type:str
  value:str
  start:int
  end:int

@dataclass
class ParsedCommand:
  intent: str
  entities: list[Entity]
