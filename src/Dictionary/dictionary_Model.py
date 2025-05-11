from typing import List, Optional

class Phonetic():
    text: str
    audio: Optional[str] = None

class Definition():
    definition: str
    example: Optional[str] = None
    synonyms: List[str] = []
    antonyms: List[str] = []

class Meaning():
    partOfSpeech: str
    definitions: List[Definition]

class WordEntry():
    word: str
    phonetic: Optional[str] = None
    phonetics: List[Phonetic] = []
    origin: Optional[str] = None
    meanings: List[Meaning]