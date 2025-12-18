import os
from pdfminer.high_level import extract_text
from docx import Document


class DocumentManager:
    def __init__(self, storage_dir='data/docs'):
        os.makedirs(storage_dir, exist_ok=True)
        self.storage_dir = storage_dir

    def save_uploaded_file(self, uploaded_file):
        # Handle both Streamlit file uploads and Flask file uploads
        if hasattr(uploaded_file, 'name'):
            filename = uploaded_file.name
            content = uploaded_file.getbuffer()
        elif hasattr(uploaded_file, 'filename'):
            # Flask file upload
            filename = uploaded_file.filename
            content = uploaded_file.read()
            uploaded_file.seek(0)  # Reset file pointer
        else:
            raise ValueError("Unsupported file upload type")
        
        dest = os.path.join(self.storage_dir, filename)
        with open(dest, 'wb') as f:
            if isinstance(content, bytes):
                f.write(content)
            else:
                f.write(content)
        return dest

    def list_documents(self):
        return sorted(os.listdir(self.storage_dir))

    def delete_document(self, name):
        path = os.path.join(self.storage_dir, name)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def parse_document(self, name):
        path = os.path.join(self.storage_dir, name)
        if name.lower().endswith('.pdf'):
            return extract_text(path)
        elif name.lower().endswith('.docx'):
            doc = Document(path)
            return '\n'.join(p.text for p in doc.paragraphs)
        else:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()

    def get_all_parsed(self):
        result = {}
        for fn in self.list_documents():
            result[fn] = self.parse_document(fn)
        return result

