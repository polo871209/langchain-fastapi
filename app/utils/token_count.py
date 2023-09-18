from typing import Optional

import tiktoken


# Write function to take string input and return number of tokens
def num_tokens_from_string(
    string: str, encoding_name: Optional[str] = "gpt-3.5-turbo"
) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
