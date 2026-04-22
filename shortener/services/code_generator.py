"""Service contracts for short code generation."""

from abc import ABC, abstractmethod


class ShortCodeGenerator(ABC):
    """Abstract service for short code generation."""

    @abstractmethod
    def generate(self, length: int = 6) -> str:
        """Generate a short code string.

        Args:
            length: Expected code length.

        Returns:
            A generated short code.
        """
