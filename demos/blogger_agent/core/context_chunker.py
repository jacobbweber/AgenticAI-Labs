"""
ContextChunker Primitive
Splits large inbox content exceeding context limits into logical chunks
at natural boundaries (file headers, paragraph double-newlines).
"""


class ContextChunker:
    """
    Splits aggregated text into chunks of <= max_chars (default 40,000 chars)
    at natural boundaries such as file headers ('--- File:') and paragraph double-newlines ('\\n\\n').
    """

    def __init__(self, default_max_chars: int = 40000):
        self.default_max_chars = default_max_chars

    def chunk_text(self, text: str, max_chars: int = 40000) -> list[str]:
        """
        Splits text into a list of strings where each element's length <= max_chars.
        If text <= max_chars, returns [text].
        """
        if not text or len(text) <= max_chars:
            return [text]

        blocks = self._split_into_logical_blocks(text, max_chars)

        chunks: list[str] = []
        current_chunk_blocks: list[str] = []
        current_length = 0

        for block in blocks:
            separator = "\n\n" if current_chunk_blocks else ""
            block_len = len(block)
            sep_len = len(separator)

            if current_length + sep_len + block_len <= max_chars:
                current_chunk_blocks.append(block)
                current_length += sep_len + block_len
            else:
                if current_chunk_blocks:
                    chunks.append("\n\n".join(current_chunk_blocks))
                    current_chunk_blocks = []
                    current_length = 0

                if block_len <= max_chars:
                    current_chunk_blocks.append(block)
                    current_length = block_len
                else:
                    sub_chunks = self._split_large_block(block, max_chars)
                    for sub in sub_chunks[:-1]:
                        chunks.append(sub)
                    if sub_chunks:
                        current_chunk_blocks.append(sub_chunks[-1])
                        current_length = len(sub_chunks[-1])

        if current_chunk_blocks:
            chunks.append("\n\n".join(current_chunk_blocks))

        return chunks

    def _split_into_logical_blocks(self, text: str, max_chars: int) -> list[str]:
        """
        Splits raw text by double newlines or file boundary headers.
        """
        raw_paragraphs = text.split("\n\n")
        blocks: list[str] = []

        for paragraph in raw_paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            if len(paragraph) <= max_chars:
                blocks.append(paragraph)
            else:
                lines = paragraph.split("\n")
                line_block: list[str] = []
                line_len = 0
                for line in lines:
                    if line_len + (1 if line_block else 0) + len(line) <= max_chars:
                        line_block.append(line)
                        line_len += (1 if line_block else 0) + len(line)
                    else:
                        if line_block:
                            blocks.append("\n".join(line_block))
                            line_block = []
                            line_len = 0
                        if len(line) <= max_chars:
                            line_block.append(line)
                            line_len = len(line)
                        else:
                            for i in range(0, len(line), max_chars):
                                blocks.append(line[i : i + max_chars])
                if line_block:
                    blocks.append("\n".join(line_block))

        return blocks if blocks else [text]

    def _split_large_block(self, block: str, max_chars: int) -> list[str]:
        """
        Fallback splitting for a single block larger than max_chars.
        """
        sub_chunks: list[str] = []
        lines = block.split("\n")
        current_lines: list[str] = []
        current_len = 0

        for line in lines:
            sep = "\n" if current_lines else ""
            if current_len + len(sep) + len(line) <= max_chars:
                current_lines.append(line)
                current_len += len(sep) + len(line)
            else:
                if current_lines:
                    sub_chunks.append("\n".join(current_lines))
                    current_lines = []
                    current_len = 0
                if len(line) <= max_chars:
                    current_lines.append(line)
                    current_len = len(line)
                else:
                    for i in range(0, len(line), max_chars):
                        sub_chunks.append(line[i : i + max_chars])

        if current_lines:
            sub_chunks.append("\n".join(current_lines))

        return sub_chunks
