import shutil
from pathlib import Path

def mover(email: str, email_category: str, default_direction: str = 'Treated') -> str:
    email_path = Path(email)
    default_direction_path = Path(default_direction)
    new_direction_partly = default_direction_path / email_category
    new_direction_partly.mkdir(parents=True, exist_ok=True)
    new_direction_fully = new_direction_partly / email_path.name
    if new_direction_fully.exists():
        counter = 1
        stem = email_path.stem
        suffix = email_path.suffix
        while new_direction_fully.exists():
            new_name = f"{stem}_{counter}{suffix}"
            new_direction_fully = new_direction_partly / new_name
            counter += 1
    shutil.move(str(email_path), str(new_direction_fully))
    return str(new_direction_fully)