from __future__ import annotations
import re
from typing import List, Pattern

class NegativeNumberError(ValueError):
    """Raised when negatives are present in input.

    The message will include the negative numbers list as required by kata.
    """

    def __init__(self, negatives: List[int]) -> None:
        message = f"negative numbers not allowed {','.join(str(n) for n in negatives)}"
        super().__init__(message)
        self.negatives = negatives


class StringCalculator:
    """String calculator implementing the kata requirements.

    Features / design choices:
    - `add` receives a string and returns an int (sum).
    - Supports default delimiters: comma and newline.
    - Supports custom delimiter(s) declared at the beginning of the string as:
      `//<delimiter>\n<numbers...>` or `//[delim1][delim2]\n...` for multi and/or long delimiters.
    - Raises `NegativeNumberError` when any negative numbers are present and lists all of them.
    - Robustly handles whitespace around numbers.

    The implementation is intentionally small and well-factored to support unit testing and clarity.
    """

    DEFAULT_DELIMITERS = [",", "\n"]
    _delimiter_pattern: Pattern[str] = re.compile(r"//(.*?)\n(.*)", flags=re.S)

    def add(self, numbers: str) -> int:
        """Parse `numbers` and return their sum.

        Parameters
        ----------
        numbers: str
            Input string containing numbers separated by delimiters.

        Returns
        -------
        int
            Sum of the parsed integers. Empty input -> 0.

        Raises
        ------
        NegativeNumberError
            If one or more negative numbers are found.
        ValueError
            For malformed inputs that cannot be parsed as integers.
        """
        if numbers is None:
            raise ValueError("numbers must be a string (got None)")
        
        delimiters = list(self.DEFAULT_DELIMITERS)
        
        if numbers == "":
            return 0
        
        body = numbers

        # Check for custom delimiter header
        m = self._delimiter_pattern.match(numbers)
        if m:
            delim_part, body = m.group(1), m.group(2)
            delimiters_from_header = self._parse_delimiters_header(delim_part)
            delimiters = delimiters_from_header or delimiters

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
    

    def _parse_delimiters_header(self, header: str) -> List[str]:
        """Parse delimiter declaration header.

        Supported formats:
        - `;`  (single-char delimiter)
        - `[***][%]`  (one or multiple bracketed delimiters of any length)

        Returns a list of delimiters (strings) or an empty list if header is empty.
        """
        header = header or ""

        # If header uses bracket syntax, extract bracket contents
        if header.startswith("[") and header.endswith("]"):
            # find all bracketed groups
            parts = re.findall(r"\[(.*?)\]", header)
            return parts

        # Otherwise treat the whole header as the delimiter (single character common case)
        return [header]
