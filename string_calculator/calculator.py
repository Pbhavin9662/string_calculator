from __future__ import annotations


class StringCalculator:

    def add(self, numbers: str) -> int:

        if numbers is None:
            raise ValueError("numbers must be a string (got None)")

        if numbers == "":
            return 0

      