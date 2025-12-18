# AI Document Analysis Setup

The application now includes AI-powered document analysis to understand requirements and extract test scenarios from your documents.

## Features

1. **AI Document Analysis**: Analyzes uploaded documents to extract:
   - Functional requirements
   - Test scenarios and test cases
   - Edge cases and boundary conditions
   - Error handling requirements
   - Performance requirements

2. **Enhanced Test Generation**: Uses AI insights to generate better test cases

## Setup Instructions

### Option 1: Using OpenAI (Recommended)

1. **Get an OpenAI API Key**:
   - Sign up at https://platform.openai.com/
   - Go to API Keys section
   - Create a new API key

2. **Install OpenAI Library**:
   ```bash
   pip install openai
   ```

3. **Set API Key**:
   
   **Windows (PowerShell)**:
   ```powershell
   $env:OPENAI_API_KEY="your-api-key-here"
   ```
   
   **Windows (Command Prompt)**:
   ```cmd
   set OPENAI_API_KEY=your-api-key-here
   ```
   
   **Linux/Mac**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Or create a `.env` file** (optional):
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

### Option 2: Without AI (Fallback Mode)

If you don't set up an API key, the application will automatically use a fallback mode that:
- Extracts requirements using keyword matching
- Uses simple heuristics for test scenario detection
- Still works but with less intelligent analysis

## How to Use

1. **Upload Documents**: Go to the "Documents" tab and upload your PDF/DOCX/TXT files

2. **Analyze with AI**: 
   - Select a document from the list
   - Click "Analyze with AI" button
   - View the analysis results in the "AI Analysis Results" section

3. **Generate Tests**: 
   - The AI analysis will automatically be used when generating tests
   - Go to "Generated Tests" tab
   - Click "Generate Tests"
   - Tests will be enhanced with insights from AI analysis

## Cost Information

- OpenAI API usage is pay-per-use
- GPT-3.5-turbo is very affordable (~$0.001 per document analysis)
- You can set usage limits in your OpenAI account
- The application uses GPT-3.5-turbo by default (cheapest option)

## Troubleshooting

**Error: "No module named 'openai'"**
- Solution: `pip install openai`

**Error: "API key not found"**
- Solution: Set the OPENAI_API_KEY environment variable

**Error: "API rate limit exceeded"**
- Solution: Wait a few minutes or upgrade your OpenAI plan

**Analysis seems basic**
- Check that your API key is set correctly
- Verify you have credits in your OpenAI account

## Alternative AI Providers

The code can be extended to support:
- Local LLMs (Ollama, LM Studio)
- Other cloud providers (Anthropic Claude, Google Gemini)
- See `ai_document_analyzer.py` for extension points

