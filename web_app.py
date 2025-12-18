from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import os
import json
from docs_parser import DocumentManager
from c_parser import CProjectParser
from test_generator import TestGenerator
from test_runner import TestRunner
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/docs'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Initialize managers
dm = DocumentManager('data/docs')
tr = TestRunner('data/generated_tests', 'data/reports')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Get list of uploaded documents"""
    docs = dm.list_documents()
    return jsonify(docs)


@app.route('/api/documents', methods=['POST'])
def upload_document():
    """Upload a document"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/documents/<filename>', methods=['GET'])
def view_document(filename):
    """Get document content"""
    try:
        content = dm.parse_document(filename)
        return jsonify({'content': content[:10000]})  # Limit to 10k chars
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/documents/<filename>', methods=['DELETE'])
def delete_document(filename):
    """Delete a document"""
    try:
        dm.delete_document(filename)
        return jsonify({'message': 'Document deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/parse', methods=['POST'])
def parse_project():
    """Parse C project"""
    data = request.json
    project_dir = data.get('project_dir', 'examples')
    
    if not os.path.exists(project_dir):
        return jsonify({'error': f'Path does not exist: {project_dir}'}), 400
    
    try:
        cpp = CProjectParser(project_dir)
        functions = cpp.parse_project()
        
        # Save to JSON
        os.makedirs('data/parsed_c', exist_ok=True)
        with open('data/parsed_c/functions.json', 'w') as f:
            json.dump(functions, f, indent=2)
        
        return jsonify({'functions': functions, 'count': len(functions)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tests/generate', methods=['POST'])
def generate_tests():
    """Generate test files"""
    try:
        cpp = CProjectParser('examples')
        functions = cpp.parse_project()
        docs_meta = dm.get_all_parsed()
        tg = TestGenerator('data/generated_tests')
        tg.generate_tests(functions, docs_meta)
        return jsonify({'message': 'Tests generated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tests', methods=['GET'])
def list_tests():
    """List generated test files"""
    try:
        files = tr.list_tests()
        test_files = []
        for f in files:
            filepath = os.path.join('data/generated_tests', f)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                test_files.append({'name': f, 'content': content})
        return jsonify(test_files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tests/run', methods=['POST'])
def run_tests():
    """Run selected tests"""
    data = request.json
    selected = data.get('selected', [])
    
    if not selected:
        return jsonify({'error': 'No tests selected'}), 400
    
    try:
        html, xml = tr.run_tests(selected)
        return jsonify({
            'message': 'Tests completed',
            'html_report': html,
            'xml_report': xml
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/html', methods=['GET'])
def get_html_report():
    """Get HTML report"""
    report_path = os.path.join('data/reports', 'report.html')
    if os.path.exists(report_path):
        return send_file(report_path)
    return jsonify({'error': 'Report not found'}), 404


@app.route('/api/reports/xml', methods=['GET'])
def get_xml_report():
    """Get XML report"""
    report_path = os.path.join('data/reports', 'junit.xml')
    if os.path.exists(report_path):
        return send_file(report_path, mimetype='application/xml')
    return jsonify({'error': 'Report not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

