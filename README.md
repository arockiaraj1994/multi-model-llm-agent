# Multi-Model LLM Example

## Prerequisites

Ensure you have Python and pip installed. You can create virtual environments in two ways:

1. Using pip to install virtualenv (recommended):
   ```bash
   pip install --user virtualenv
   ```

2. Using built-in venv (alternative):
   ```bash
   python -m venv venv
   ```

## Setup

1. Create virtual environment using virtualenv:
```bash
# Navigate to project directory
cd your-project-directory
virtualenv venv
```

2. Activate virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Verify installation:
```bash
# Check pip is from virtual environment
which pip  # Linux/Mac
where pip  # Windows
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
multi-model-llm-example/
│
├── src/                    # Source code package
├── resources/             # Resource files
├── tests/                 # Test files
├── requirements.txt       # Project dependencies
├── .gitignore            # Git ignore file
└── README.md             # Project documentation
