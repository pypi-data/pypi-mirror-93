from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional

ONE_DAY = 86400


@dataclass
class Translation:
    text: str
    to: str
    provider: 'BaseProvider'
    detectedLanguage: Optional[str] = None


class BaseProvider(ABC):
    icon = ""

    @property
    def name(self) -> str:
        """Shortcut to get name of the provider"""
        return self.__class__.__name__

    @abstractmethod
    async def get_languages(self, *args, **kwargs) -> Dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    async def detect(self, content) -> str:
        raise NotImplementedError

    @abstractmethod
    async def translate(self, content: str, to: str, fro="", **options) -> [Translation]:
        raise NotImplementedError
