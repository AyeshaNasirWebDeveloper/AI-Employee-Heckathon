from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

OBSIDIAN_VAULT = Path(os.getenv("OBSIDIAN_VAULT_PATH"))

def save_to_obsidian(content, folder="inbox", title="Note"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    target_folder = OBSIDIAN_VAULT / folder
    target_folder.mkdir(parents=True, exist_ok=True)

    filename = f"{title}_{timestamp}.md"
    file_path = target_folder / filename

    formatted_content = f"""# {title}

Generated on: {timestamp}

---

{content}
"""

    file_path.write_text(formatted_content, encoding="utf-8")

    print(f"✅ Saved to: {file_path}")