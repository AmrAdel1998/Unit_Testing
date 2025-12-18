# Pytest Tool - Automated C Test Generator

A complete tool that automates test-case generation, selection, execution, and reporting for C projects using pytest.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Choose Your Interface

You have **3 options** to run the application:

#### Option A: Tkinter Desktop GUI (Easiest) ⭐

```bash
python gui_tkinter.py
```

Opens a native desktop application with tabs for all features.

#### Option B: Web Application (Flask) 🌐

```bash
python web_app.py
```

Then open your browser at `http://localhost:5000`

#### Option C: Streamlit Web App (Original)

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

## 📋 How to Use

### Step 1: Documents Tab
- **Tkinter**: Click "Browse & Upload" to select documents
- **Web**: Use the file input and click "Upload Document"
- Upload PDF, DOCX, TXT, or MD files containing requirements
- View or delete uploaded documents
- Documents are stored in `data/docs/`

### Step 2: Parse C Project Tab
- Enter the path to your C project folder (default: `examples`)
- Click "Parse project" to extract function signatures
- View extracted functions with their signatures
- Parsed data is saved to `data/parsed_c/functions.json`

### Step 3: Generated Tests Tab
- Click "Generate tests from parsed C and documents"
- View generated pytest test files
- Click on test files to view their content
- Tests are saved to `data/generated_tests/`

### Step 4: Run & Reports Tab
- Select which test files to run (checkboxes)
- Click "Run selected tests"
- View HTML and XML reports
- Reports are saved to `data/reports/`

## 📁 Project Structure

```
pytest_tool/
├─ app.py                    # Streamlit UI (original)
├─ gui_tkinter.py            # Tkinter Desktop GUI ⭐
├─ web_app.py                # Flask Web Application 🌐
├─ requirements.txt
├─ docs_parser.py           # Document parsing (PDF/DOCX/TXT/MD)
├─ c_parser.py              # C code parsing
├─ test_generator.py        # Test case generation
├─ test_runner.py           # Test execution engine
├─ utils.py                 # Helper utilities
├─ templates/
│ └─ index.html             # Web app HTML template
├─ data/
│ ├─ docs/                  # Uploaded documents
│ ├─ parsed_c/              # Parsed AST/JSON
│ ├─ generated_tests/        # Output .py test files
│ └─ reports/               # HTML/XML reports
└─ examples/
  └─ sample.c               # Sample C file
```

## ✨ Features

- **Document Parsing**: Extracts text from PDF, DOCX, TXT, and MD files
- **C Code Parsing**: Extracts function signatures from C source files
- **Test Generation**: Auto-generates pytest test cases with positive, negative, and boundary cases
- **Test Execution**: Runs selected tests with pytest, supports parallel execution
- **Reporting**: Generates HTML and JUnit XML reports
- **Multiple Interfaces**: Choose between Tkinter GUI, Flask web app, or Streamlit

## 🎯 Recommended Usage

- **For Desktop Users**: Use `gui_tkinter.py` - Simple, native, no browser needed
- **For Web Users**: Use `web_app.py` - Modern web interface, accessible from any device
- **For Quick Prototyping**: Use `app.py` (Streamlit) - Fast development

## 🔧 Requirements

- Python 3.7+
- All dependencies listed in `requirements.txt`
