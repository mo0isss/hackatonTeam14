import os
from src.parser.Email import Email

class EmailParser:
    def parseTxt(self, filePath) -> Email:
        content = None
        for enc in ['utf-8', 'cp1251', 'latin1']:
            try:
                with open(filePath, 'r', encoding=enc) as f:
                    lines = f.readlines()
                content = lines
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            raise ValueError("Invalid file encoding")
        
        result = [None] * 4
        sentFromIphone = False
        isAForward = False
        isAReply = False
        # result structure: 0 - sender, 1 - subject, 2 - recipient, 3 - date 
        inHeader = True
        body = ""
        attachments = []
        possibleHeaders = [("from", "от кого", "sender", "отправитель", "ot kogo"), ("тема", "subject", "topic", "tema"), ("recipient", "получатель", "кому", "komu", "to"), ("date", "дата", "data")]
        possibleAttachments = ("прикрепил", "вложение", "файл", "во вложении", "pinned", "attached", "prikrepil", "приложил", "прикладываю", "код", "code", "error", "ошибк")
        possibleFileExtensions = (".txt", ".pdf", ".jpeg", ".docx", ".png", ".xls", ".xlsx", ".jpg", ".json", ".bin", ".zip")

        for line in lines:
            line = line.rstrip('\n')

            if "Re:" in line:
                isAReply = True
                line = line.replace("Re: ", "").strip()
            
            if "Fwd:" in line:
                isAForward = True
                line = line.replace("Fwd: ", "").strip()

            if "Otpravleno s iPhone" in line:
                sentFromIphone = True
                line = line.replace("Otpravleno s iPhone", "").strip()

            
            lineCopy = line.lower()

            if inHeader and line == "" and result[0] is not None:
                inHeader = False
                continue
            
            if inHeader and ':' in line:
                counter = 0
                for possibleHeader in possibleHeaders:
                    if any([header + ":" in lineCopy for header in possibleHeader]):
                        line = line.replace(": ", " :", 1)
                        index = line.index(":")
                        if len(line) <= 1:
                            continue
                        else:
                            result[counter] = line[index + 1:] if len(line) > index + 1 else None
                            break
                    else:
                        counter += 1

            if not inHeader and line != "":
                if any([possibleAttachment in lineCopy for possibleAttachment in possibleAttachments]) and (any([possibleFileExtension in lineCopy for possibleFileExtension in possibleFileExtensions]) or any([str(i) in lineCopy for i in range(10)])) and ":" in line:
                    for file in line[line.index(":") + 2:].split():
                        attachments.append(file)
                else:
                    body += line + '\n'

        if result[0] is None:
            raise ValueError("File is not an email")
        
        return Email(result[0], 
                     body.strip(), 
                     result[1], 
                     result[2], 
                     result[3], 
                     attachments if attachments != [] else None, 
                     isAReply, 
                     isAForward, 
                     sentFromIphone)
    
    
    def parse(self, filePath) -> Email:
        if filePath is None:
            raise ValueError("File path cannot be None")
        if not os.path.exists(filePath):
            raise FileNotFoundError("The file doesn't exist")
        if not os.path.isfile(filePath):
            raise ValueError("The path doesn't lead to file")
        
        fileExtension = os.path.splitext(filePath)[1].lower()
        if fileExtension == ".txt":
            return self.parseTxt(filePath)
        else:
            try:
                with open(filePath, 'r', encoding='utf-8') as file:
                    sample = file.read(512).lower()
                if any([header in sample for header in ("from", "subject", "от кого", "тема", "topic", "ot kogo", "data", "date", "дата")]):
                    return self.parseTxt(filePath)
                else:
                    raise ValueError("File is not an email")
            except UnicodeDecodeError:
                raise ValueError("Invalid file extension, must be .txt")