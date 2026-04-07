class Chunker:

    def __init__(self, chunk_size=300, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text):
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)

            start += self.chunk_size - self.overlap

        return chunks