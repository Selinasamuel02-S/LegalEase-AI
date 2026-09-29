# LegalEase LIGHT FIXED - No font-family bug
import os, http.server, socketserver, urllib.parse
from ai_core.gemini_generator import GeminiDocumentGenerator
from ai_core.formatters import format_docx, format_pdf, sanitize_text

gen = GeminiDocumentGenerator()
os.makedirs("downloads", exist_ok=True)

def get_html(result=""):
    if not result:
        result = "<p>Fill details & Generate</p>"
    return f"""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>LegalEase</title>
<style>
body{{font-family:sans-serif;background:#0f0f1a;color:white;padding:15px}}
input,select,textarea{{width:100%;padding:10px;margin:5px 0;border-radius:8px;border:none}}
button{{background:#6c5ce7;color:white;padding:12px;width:100%;border:none;border-radius:8px;font-size:16px}}
.card{{background:#1e1e2f;padding:15px;border-radius:12px;margin-top:15px;white-space:pre-wrap}}
a{{color:#00cec9;display:block;margin:8px 0;font-weight:bold}}
</style></head><body>
<h1>LegalEase</h1><p>AI Legal Document - PDF Book maathiri</p>
<form method="POST">
<select name="doc_type">
<option>Employment Contract</option>
<option>NDA (Non-Disclosure Agreement)</option>
<option>Lease Agreement</option>
<option>Freelance Work Contract</option>
</select>
<input name="parties" placeholder="Parties ex: Jane, TechNova" value="Jane Doe (Service Provider), TechNova Inc. (Client)" required>
<textarea name="terms" rows="4" placeholder="Terms use ;" required>Payment within 30 days; Confidentiality 2 years; Work from home; 15 days notice</textarea>
<input name="date" value="2026-09-29">
<button type="submit">Generate Document</button>
</form>
{result}
</body></html>
"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/downloads/"):
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
        self.wfile.write(get_html().encode())

    def do_POST(self):
        length = int(self.headers.get('content-length',0))
        data = urllib.parse.parse_qs(self.rfile.read(length).decode())
        doc_type = data.get('doc_type',['Employment Contract'])[0]
        parties = data.get('parties',[''])[0]
        terms = data.get('terms',[''])[0]
        date = data.get('date',['2026-09-29'])[0]

        raw = gen.generate_document(doc_type, parties, terms, date)
        clean = sanitize_text(raw)

        docx_path = format_docx(clean, doc_type, parties, terms)
        pdf_path = format_pdf(clean, doc_type)
        txt_path = os.path.join("downloads", f"{doc_type.replace(' ','_')}.txt")
        with open(txt_path,"w",encoding="utf-8") as f:
            f.write(clean)

        # copy to downloads
        import shutil
        try:
            shutil.copy(docx_path, "downloads/")
            shutil.copy(pdf_path, "downloads/")
        except: pass

        result_html = f"""
        <div class="card">{clean[:5000]}</div>
        <h3>Generated! Download:</h3>
        <a href="/downloads/{os.path.basename(docx_path)}" download>📄 Download DOCX</a>
        <a href="/downloads/{os.path.basename(pdf_path)}" download>📕 Download PDF</a>
        <a href="/{txt_path}" download>📝 Download TXT</a>
        """
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
        self.wfile.write(get_html(result_html).encode())

print("Starting LegalEase on http://0.0.0.0:7860...")
with socketserver.TCPServer(("0.0.0.0", 7860), Handler) as httpd:
    httpd.serve_forever()