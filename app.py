import streamlit as st
import os
from docs_parser import DocumentManager
from c_parser import CProjectParser
from test_generator import TestGenerator
from test_runner import TestRunner

st.set_page_config(page_title='Pytest Tool - C Test Generator', layout='wide')

st.title('🧪 Pytest Tool - Automated C Test Generator')
st.markdown('Upload documents, parse C code, generate tests, and run them with detailed reports.')

tabs = st.tabs(['📄 Documents', '🔍 Parse C Project', '📝 Generated Tests', '▶️ Run & Reports'])

# Documents tab
with tabs[0]:
    st.header('1) Upload and Manage Documents')
    st.markdown('Upload PDF, DOCX, TXT, or MD files containing requirements and specifications.')
    
    dm = DocumentManager('data/docs')
    
    uploaded_file = st.file_uploader('Upload document', type=['pdf', 'docx', 'txt', 'md'])
    if uploaded_file:
        if st.button('Save document'):
            dest = dm.save_uploaded_file(uploaded_file)
            st.success(f'Saved: {dest}')
            st.experimental_rerun()
    
    st.subheader('Uploaded Documents')
    docs = dm.list_documents()
    if not docs:
        st.info('No documents uploaded yet.')
    else:
        for d in docs:
            cols = st.columns([3, 1, 1])
            cols[0].write(f'📄 {d}')
            if cols[1].button('View', key=f'view_{d}'):
                parsed = dm.parse_document(d)
                st.code(parsed[:1000])
            if cols[2].button('Delete', key=f'del_{d}'):
                dm.delete_document(d)
                st.experimental_rerun()

# Parse C Project tab
with tabs[1]:
    st.header('2) Choose C project folder and parse')
    project_dir = st.text_input('Path to C project (folder)', value='examples')
    parse_button = st.button('Parse project')
    
    if parse_button:
        cpp = CProjectParser(project_dir)
        functions = cpp.parse_project()
        st.success(f'Found {len(functions)} functions')
        
        if functions:
            st.subheader('Extracted Functions:')
            for fn in functions:
                with st.expander(f"{fn['name']} - {os.path.basename(fn['file'])}"):
                    st.code(f"Return: {fn['return']}\nName: {fn['name']}\nArgs: {fn['args']}")
            
            # Save parsed data
            import json
            os.makedirs('data/parsed_c', exist_ok=True)
            with open('data/parsed_c/functions.json', 'w') as f:
                json.dump(functions, f, indent=2)
            st.info('Parsed functions saved to data/parsed_c/functions.json')

# Generated Tests tab
with tabs[2]:
    st.header('3) Generated Tests')
    
    if st.button('Generate tests from parsed C and documents'):
        cpp = CProjectParser('examples')
        functions = cpp.parse_project()
        dm = DocumentManager('data/docs')
        docs_meta = dm.get_all_parsed()
        tg = TestGenerator('data/generated_tests')
        tg.generate_tests(functions, docs_meta)
        st.success('Tests generated!')
        st.experimental_rerun()
    
    gen_files = os.listdir('data/generated_tests') if os.path.exists('data/generated_tests') else []
    if gen_files:
        st.subheader('Generated test files:')
        for f in gen_files:
            with st.expander(f'📝 {f}'):
                try:
                    content = open(os.path.join('data/generated_tests', f), 'r', encoding='utf-8').read()
                    st.code(content, language='python')
                except Exception as e:
                    st.error(f'Error reading file: {e}')
    else:
        st.info('No test files generated yet. Click "Generate tests" to create them.')

# Run & Reports tab
with tabs[3]:
    st.header('4) Select tests and run')
    
    tr = TestRunner('data/generated_tests', 'data/reports')
    files = tr.list_tests()
    
    if not files:
        st.info('No test files found. Generate tests first in the "Generated Tests" tab.')
    else:
        st.subheader('Select tests to run:')
        selected = []
        for f in files:
            if st.checkbox(f, value=True, key=f'select_{f}'):
                selected.append(f)
        
        if st.button('Run selected tests', type='primary'):
            if selected:
                with st.spinner('Running tests...'):
                    html, xml, error_info = tr.run_tests(selected)
                    st.success('Run finished!')
                    
                    if error_info:
                        st.error(f"Tests failed with return code {error_info['returncode']}")
                        with st.expander("Show Output"):
                            st.text(error_info['stdout'])
                            st.text(error_info['stderr'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.subheader('HTML Report')
                        if os.path.exists(html.lstrip('/')):
                            with open(html.lstrip('/'), 'r', encoding='utf-8') as f:
                                st.download_button('Download HTML Report', f.read(), 'report.html', 'text/html')
                            st.markdown(f'**Path:** `{html}`')
                    
                    with col2:
                        st.subheader('JUnit XML Report')
                        if os.path.exists(xml.lstrip('/')):
                            with open(xml.lstrip('/'), 'r', encoding='utf-8') as f:
                                st.download_button('Download XML Report', f.read(), 'junit.xml', 'application/xml')
                            st.markdown(f'**Path:** `{xml}`')
                            
                    with col3:
                        st.subheader('CSV Report')
                        csv_path = os.path.join('data/reports', 'report.csv')
                        if os.path.exists(csv_path):
                            with open(csv_path, 'r', encoding='utf-8') as f:
                                st.download_button('Download CSV Report', f.read(), 'report.csv', 'text/csv')
                            st.markdown(f'**Path:** `{csv_path}`')
            else:
                st.warning('Please select at least one test file to run.')
