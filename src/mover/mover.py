import shutil
from pathlib import *
def mover(email: str, email_category: str, default_direction: str='Treated') -> str:
    email_path = Path(email)
    default_direction_path = Path(default_direction)
    new_direction_patrly = default_direction_path/email_category
    new_direction_patrly.mkdir(parents=True, exist_ok=True)
    new_direction_fully = new_direction_patrly / email_path.name
    shutil.move(str(email_path), str(new_direction_fully))
    return str(new_direction_fully)