import re
import spacy
from PyPDF2 import PdfReader

class CVProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self._raw_text = ""
        self.anonymized_text = ""
        
    @property
    def raw_text(self):
        if not self._raw_text:
            reader = PdfReader(self.pdf_path)
            full_text = []
            for page in reader.pages:
                text_page = page.extract_text()
                if text_page:
                    full_text.append(text_page)
            self._raw_text = "\n".join(full_text)
        return self._raw_text

    def anonymize(self):
        text = self.raw_text
        
     
        lines = text.split('\n')
        cleaned_lines = []
        for i, line in enumerate(lines):
            
            if i < 3 and any(c.isupper() for c in line) and len(line.strip()) > 3:
              
                line = re.sub(r'\b[A-Z]{3,}\b', '[REDACTED_NAME]', line)
            cleaned_lines.append(line)
        text = "\n".join(cleaned_lines)

        # 2. FIX L-EMAIL 
        email_pattern = r'[a-zA-Z0-9._%+-]+\s*@\s*[a-zA-Z0-9.-]+\s*\.[a-zA-Z]{2,}'
        text = re.sub(email_pattern, "[REDACTED_EMAIL]", text)
        
        # 3. FIX LINKEDIN & GITHUB
        linkedin_pattern = r'(?i)linkedin:\s*[a-zA-Z0-9_\-\s]+'
        github_pattern = r'(?i)github\s*:\s*[a-zA-Z0-9_\-\s]+'
        text = re.sub(linkedin_pattern, "LinkedIn: [REDACTED_LINK]", text)
        text = re.sub(github_pattern, "GitHub: [REDACTED_LINK]", text)

        # 4. PHONE REGEX
        phone_pattern = r'\+?\d[\d\s-]{8,14}\d'
        text = re.sub(phone_pattern, "[REDACTED_PHONE]", text)

        try:
            
            nlp = spacy.load("xx_sent_ud_sm")
        except:
            nlp = spacy.load("en_core_web_sm")
            
        doc = nlp(text)
        for ent in doc.ents:
            
            if ent.label_ == "PERSON" and len(ent.text.strip()) > 2 and ent.text.lower() not in ["html", "css", "php", "sql", "mois", "partir"]:
                text = text.replace(ent.text, "[REDACTED_NAME]")
                
        self.anonymized_text = text
        return self.anonymized_text