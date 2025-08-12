from __future__ import annotations
import re
from typing import List

class NegativeNumberError(ValueError):
    """Raised when negatives are present in input.

    The message will include the negative numbers list as required by kata.
    """

    def __init__(self, negatives: List[int]) -> None:
        message = f"negative numbers not allowed {','.join(str(n) for n in negatives)}"
        super().__init__(message)
        self.negatives = negatives


class StringCalculator:
    DEFAULT_DELIMITERS = [",", "\n"]

    def add(self, numbers: str) -> int:

        if numbers is None:
            raise ValueError("numbers must be a string (got None)")
        
        delimiters = list(self.DEFAULT_DELIMITERS)
        
        if numbers == "":
            return 0
        
        body = numbers
        
        # Build regex to split
        split_re = self._build_split_regex(delimiters)

        # Tokenize
        tokens = [t.strip() for t in re.split(split_re, body) if t.strip() != ""]

        nums: List[int] = []
        negatives: List[int] = []

        for token in tokens:
            try:
                n = int(token)
            except ValueError as exc:
                # Be explicit about bad tokens for easier debugging
                raise ValueError(f"Unable to parse integer from token: {token!r}") from exc

            if n < 0:
                negatives.append(n)
            nums.append(n)

        if negatives:
            raise NegativeNumberError(negatives)

        return sum(nums)

    def _build_split_regex(self, delimiters: List[str]) -> str:
        """Return a regex pattern string used for splitting the numbers string.

        Each delimiter is escaped with re.escape so special regex char are treated literally.
        The pattern is a union alternation of delimiters.
        """
        escaped = [re.escape(d) for d in delimiters if d != ""]
        # sort by length desc to ensure longer delimiters are matched first when needed
        escaped.sort(key=len, reverse=True)
        pattern = "|".join(escaped)
        return pattern
    

