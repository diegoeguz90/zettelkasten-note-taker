import os

VAULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "storage", "vaults")
os.makedirs(VAULTS_DIR, exist_ok=True)

def get_note_path(note_id: str) -> str:
    return os.path.join(VAULTS_DIR, f"{note_id}.md")

def save_note_content(note_id: str, content: str) -> str:
    path = get_note_path(note_id)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def read_note_content(note_id: str) -> str:
    path = get_note_path(note_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""
