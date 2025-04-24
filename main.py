from flask import Flask, request, send_file
import subprocess
import os
import tempfile

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_pdf():
    data = request.json
    title = data.get('title', '無題論文')
    author = data.get('author', '名無し')
    body = data.get('body', '')
    references = data.get('references', '')

    latex_code = f"""
\\documentclass[a4paper,12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=30mm]{{geometry}}
\\usepackage{{hyperref}}
\\usepackage{{fontspec}}
\\setmainfont{{Noto Sans CJK JP}}
\\title{{{title}}}
\\author{{{author}}}
\\begin{{document}}
\\maketitle
\\tableofcontents
{body}
\\section*{{参考文献}}
\\begin{{itemize}}
{references}
\\end{{itemize}}
\\end{{document}}
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "output.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)

        subprocess.run(["lualatex", "-interaction=nonstopmode", tex_path], cwd=tmpdir)
        pdf_path = os.path.join(tmpdir, "output.pdf")

        if os.path.exists(pdf_path):
            return send_file(pdf_path, mimetype='application/pdf', as_attachment=True)
        else:
            return {"error": "PDF generation failed"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
