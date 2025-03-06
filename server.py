from flask import Flask, request, jsonify
from docx import Document
import os

app = Flask(__name__)

def convert_docx_to_markdown(docx_path):
    """Конвертирует .docx в markdown"""
    doc = Document(docx_path)
    md_content = []

    for para in doc.paragraphs:
        if para.style.name.startswith("Heading"):
            level = int(para.style.name[-1]) 
            md_content.append(f"{'#' * level} {para.text}")
        else:
            md_content.append(para.text)

    return "\n\n".join(md_content)

@app.route('/convert', methods=['POST'])
def convert():
    """Обрабатывает загрузку файла и конвертирует его в Markdown"""
    file = request.files['file']
    temp_path = "temp.docx"
    file.save(temp_path)
    
    markdown_result = convert_docx_to_markdown(temp_path)
    os.remove(temp_path)

    return jsonify({'markdown': markdown_result})

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)

