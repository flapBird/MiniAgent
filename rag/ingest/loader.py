import os

def load_documents(folder_path: str):
    docs = []

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)

        if file.endswith((".txt", ".md")):
            with open(path, "r", encoding="utf-8") as f:
                docs.append({
                    "content": f.read(),
                    "source": file
                })

    return docs