"""Random short code generator implementation."""

import secrets
import string

from shortener.services.code_generator import ShortCodeGenerator


class RandomShortCodeGenerator(ShortCodeGenerator):
    """Creates random alphanumeric short codes."""

    _ALPHANUMERIC = string.ascii_letters + string.digits

    def generate(self, length: int = 6) -> str:
        """Generate an alphanumeric short code.

        Args:
            length: Code length.

        Returns:
            Random alphanumeric code.
        """
        return "".join(secrets.choice(self._ALPHANUMERIC) for _ in range(length))
