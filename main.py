from pathlib import Path
from src.parser.EmailParser import EmailParser
from src.identifier.classification import Classification
from src.mover.mover import mover
def main():
    inbox_path = Path("inbox")
    if not inbox_path.exists():
        print("Eror: there is no such folder in directory")
        return
    parser = EmailParser()
    classifier = Classification()
    letters = list(inbox_path.glob("*"))
    if len(letters) == 0:
        print('Inbox folder is empty')
        return
    for letter in letters:
        try:
            email = parser.parse(str(letter))
            category = classifier.classify(email)
            mover(str(letter), category)
        except Exception as error:
            print(f"Error occured: {letter.name}:{error}")
            mover(str(letter), "other")
if __name__ == "__main__":
    main()