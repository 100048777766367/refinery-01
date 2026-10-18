import re

class DecontaminationChamber:
    EMAIL_PATT = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    PHONE_PATT = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'

    @classmethod
    def decontaminate(cls, text):
        if not text: return ""
        cleaned = re.sub(cls.EMAIL_PATT, "[ANON_ENTITY]", str(text))
        cleaned = re.sub(cls.PHONE_PATT, "[ANON_CONTACT]", cleaned)
        cleaned = re.sub(r'[^\w\s\-_]', '', cleaned)
        return cleaned.strip()
