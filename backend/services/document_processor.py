import os
import re
import json
import hashlib
from typing import List, Dict, Any
import docx
import PyPDF2
from backend.config.config import settings

class DocumentProcessor:
    def __init__(self, storage_dir: str = "data/embeddings"):
        self.supported_formats = ['.pdf', '.docx', '.txt', '.csv']
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def process_documents(self, file_paths: List[str]) -> Dict[str, Any]:
        results = {'processed_files': 0, 'total_files': len(file_paths), 'chunks_created': 0, 'errors': []}
        all_chunks = []
        for file_path in file_paths:
            try:
                if not self._is_supported_format(file_path):
                    results['errors'].append(f"Unsupported format: {file_path}")
                    continue
                text_content = self._extract_text(file_path)
                if not text_content:
                    results['errors'].append(f"Could not extract text from: {file_path}")
                    continue
                chunks = self.dynamic_chunking(text_content, self._get_file_type(file_path))
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{hashlib.md5(file_path.encode()).hexdigest()}_{i}"
                    chunk_data = {
                        'file_path': file_path,
                        'chunk_id': chunk_id,
                        'content': chunk,
                        'file_type': self._get_file_type(file_path),
                        'chunk_index': i
                    }
                    # store chunk as JSON for simple retrieval
                    with open(os.path.join(self.storage_dir, f"{chunk_id}.json"), 'w', encoding='utf-8') as f:
                        json.dump(chunk_data, f)
                    all_chunks.append(chunk_data)
                results['processed_files'] += 1
                results['chunks_created'] += len(chunks)
            except Exception as e:
                results['errors'].append(f"Error processing {file_path}: {str(e)}")
        return results

    def dynamic_chunking(self, content: str, doc_type: str) -> List[str]:
        if doc_type == 'resume':
            return self._chunk_resume(content)
        elif doc_type == 'contract':
            return self._chunk_contract(content)
        else:
            return self._chunk_general(content)

    def _chunk_resume(self, content: str) -> List[str]:
        chunks = []
        current = []
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            if self._is_section_header(line) and current:
                chunks.append(' '.join(current))
                current = []
            current.append(line)
            if len(' '.join(current).split()) >= settings.chunk_size:
                chunks.append(' '.join(current))
                current = []
        if current:
            chunks.append(' '.join(current))
        return chunks

    def _chunk_contract(self, content: str) -> List[str]:
        clauses = re.split(r'\n\s*(?:SECTION|CLAUSE|ARTICLE)\s+\d+[\.)]?\s*', content, flags=re.IGNORECASE)
        chunks = []
        for clause in clauses:
            clause = clause.strip()
            if not clause:
                continue
            words = clause.split()
            if len(words) <= settings.chunk_size:
                chunks.append(clause)
            else:
                # split into approx chunk_size parts
                for i in range(0, len(words), settings.chunk_size):
                    chunks.append(' '.join(words[i:i+settings.chunk_size]))
        return chunks

    def _chunk_general(self, content: str) -> List[str]:
        words = content.split()
        chunks = []
        for i in range(0, len(words), settings.chunk_size):
            chunks.append(' '.join(words[i:i+settings.chunk_size]))
        return chunks

    def _is_section_header(self, line: str) -> bool:
        header_indicators = ['experience', 'education', 'skills', 'projects', 'summary', 'objective']
        return any(ind in line.lower() for ind in header_indicators)

    def _extract_text(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return self._extract_pdf_text(file_path)
        elif ext == '.docx':
            return self._extract_docx_text(file_path)
        elif ext in ['.txt', '.csv']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except:
                return ""
        return ""

    def _extract_pdf_text(self, file_path: str) -> str:
        try:
            text = []
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    p = page.extract_text()
                    if p:
                        text.append(p)
            return '\n'.join(text)
        except Exception:
            return ""

    def _extract_docx_text(self, file_path: str) -> str:
        try:
            doc = docx.Document(file_path)
            paragraphs = [p.text.strip() for p in doc.paragraphs if p.text and p.text.strip()]
            return '\n'.join(paragraphs)
        except Exception:
            return ""

    def _get_file_type(self, file_path: str) -> str:
        fname = os.path.basename(file_path).lower()
        if 'resume' in fname or 'cv' in fname:
            return 'resume'
        if 'contract' in fname or 'agreement' in fname:
            return 'contract'
        return 'general'

