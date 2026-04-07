class Chunker:

    def __init__(self, chunk_size=600, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text):
        paragraphs = text.split("\n\n")  # 按段落
        chunks = []

        for para in paragraphs:
            if len(para) <= self.chunk_size:
                chunks.append(para)
            else:
                # 太长才用滑动窗口
                start = 0
                while start < len(para):
                    end = start + self.chunk_size
                    chunks.append(para[start:end])
                    start += self.chunk_size - self.overlap

        return chunks