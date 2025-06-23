# Automated Metadata Generation System

## 🎯 Project Overview

An intelligent automated metadata generation system that enhances document discoverability, classification, and analysis by producing scalable, consistent, and semantically rich metadata from various document formats.

## ✨ Key Features

### 🔄 **Automated Processing**
- **Multi-format Support**: PDF, DOCX, TXT, and MD files
- **OCR Integration**: Extracts text from image-based PDFs using Tesseract
- **Batch Processing**: Handle multiple documents simultaneously
- **Fallback Mechanisms**: Robust error handling with multiple extraction methods

### 🧠 **Advanced NLP & AI**
- **Entity Recognition**: Extracts persons, organizations, dates, locations, and more
- **Document Classification**: Automatically categorizes documents (Legal, Report, Manual, Proposal, etc.)
- **Intelligent Summarization**: AI-powered document summaries with fallback options
- **Topic Extraction**: Identifies key themes and subjects
- **Sentiment Analysis**: Analyzes document tone and sentiment
- **Readability Scoring**: Calculates document complexity metrics

### 📊 **Structured Output**
- **Comprehensive Metadata Schema**: Organized into basic info, content analysis, semantic data, and technical metadata
- **Multiple Export Formats**: JSON and CSV export options
- **Confidence Scoring**: Quality assessment for extracted metadata

### 🖥️ **User Interface**
- **Web Interface**: Streamlit-based GUI for easy document upload and metadata viewing
- **Command Line Interface**: Full CLI support for automation and scripting
- **Quick Start Mode**: Lightweight processing without heavy ML models

## 🚀 Installation

### Prerequisites
- Python 3.7+
- Tesseract OCR (for image-based PDF processing)

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from [Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki)

### Python Dependencies

1. **Clone the repository** (or download the notebook)
2. **Install required packages:**

```bash
# Core dependencies
pip install numpy==1.24.3
pip install --upgrade pip

# Document processing
pip install PyPDF2 python-docx pytesseract pillow PyMuPDF

# NLP and ML packages
pip install spacy transformers sentence-transformers
pip install nltk textstat

# Web framework
pip install streamlit pandas

# Download spaCy language model
python -m spacy download en_core_web_sm
```

## 📋 Usage

### Quick Start Mode (Recommended for first-time users)

```python
# Run the notebook and choose Quick Start mode
python automated_metadata_generator.py
# Choose option 2 for Quick Start
```

### Full System Mode

```python
# Initialize the system with all ML models
python automated_metadata_generator.py
# Choose option 1 for Full System
```

### Processing Options

#### 1. Single File Processing
```python
# Select mode 1 in the interface
# Enter file path when prompted
# Example: /path/to/your/document.pdf
```

#### 2. Batch Processing
```python
# Select mode 2 in the interface  
# Enter folder path containing documents
# System will process all supported files
```

#### 3. Web Interface

**Setup Instructions:**

1. **Create a separate Streamlit file** - Save your Streamlit code as `streamlit_app.py` in the same directory as your main script.

2. **Install Streamlit** if you haven't already:
   ```bash
   pip install streamlit
   ```

3. **Run the Streamlit app from your terminal** (not from a Jupyter notebook):
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Browser will open automatically** - Streamlit will automatically open your default browser to `http://localhost:8501`

**Web Interface Features:**
- File upload for PDF, DOCX, TXT, MD files
- Direct text input option
- Sample text demos for testing
- Interactive results display with organized tabs
- Download options for JSON and preview
- Real-time processing feedback and progress indicators

**Additional Dependencies for Web Interface:**
```bash
pip install streamlit PyPDF2 python-docx textstat
```

### Programmatic Usage

```python
from automated_metadata_generator import generate_metadata, generate_basic_metadata

# Generate full metadata (requires ML models)
metadata = generate_metadata("path/to/document.pdf")

# Generate basic metadata (no ML models required)
basic_metadata = generate_basic_metadata("path/to/document.pdf")

# Save results
save_metadata_to_json(metadata, "output.json")
```

## 📁 Supported File Types

- **PDF**: Standard PDFs and image-based PDFs (with OCR)
- **DOCX**: Microsoft Word documents
- **TXT**: Plain text files
- **MD**: Markdown files

## 🏗️ Architecture

### Core Components

1. **Document Processing Module**
   - Text extraction from multiple formats
   - OCR processing for image-based content
   - Content preprocessing and cleaning

2. **NLP Analysis Engine**
   - spaCy for entity recognition and linguistic analysis
   - Transformers for advanced summarization
   - NLTK for readability and text statistics

3. **Metadata Generation Pipeline**
   - Structured schema creation
   - Confidence scoring
   - Quality assessment

4. **Export & Interface Layer**
   - JSON/CSV export functionality
   - Streamlit web interface
   - CLI interface

### Data Flow

```
Input Document → Text Extraction → Preprocessing → NLP Analysis → Metadata Generation → Export
```

## 📊 Metadata Schema

The system generates structured metadata organized into four main categories:

### Basic Information
- Filename, file type, size
- Creation and processing dates

### Content Analysis
- Document type classification
- Word and character counts
- Readability scores
- Language detection

### Semantic Data
- Document summary
- Key topics and themes
- Named entities (people, organizations, dates, etc.)
- Key phrases

### Technical Metadata
- Extraction method used
- Processing time
- Confidence score

## 🔧 Configuration

### Model Configuration
The system uses multiple AI models with automatic fallbacks:

- **spaCy**: `en_core_web_sm` for entity recognition
- **Transformers**: Summarization pipeline
- **Sentence Transformers**: Semantic analysis

### Performance Tuning
- **Quick Start Mode**: Basic processing without heavy ML models
- **Batch Processing**: Optimized for multiple documents
- **Confidence Thresholds**: Adjustable quality controls

## 🚨 Error Handling

The system includes comprehensive error handling:

- **Model Loading Failures**: Automatic fallback to rule-based methods
- **File Processing Errors**: Graceful degradation with error reporting
- **OCR Failures**: Alternative text extraction methods
- **Memory Management**: Chunked processing for large documents

## 🔍 Examples

### Sample Output

```json
{
  "basic_info": {
    "filename": "research_paper.pdf",
    "file_type": ".pdf",
    "file_size": 2048576,
    "processing_date": "2025-06-22 10:30:45"
  },
  "content_analysis": {
    "document_type": "Report",
    "word_count": 5420,
    "character_count": 31205,
    "readability_score": 45.2
  },
  "semantic_data": {
    "summary": "This research paper examines the impact of artificial intelligence on document processing workflows...",
    "key_topics": ["artificial intelligence", "document processing", "machine learning", "automation", "efficiency"],
    "entities": {
      "PERSON": ["Dr. Smith", "John Doe"],
      "ORG": ["MIT", "Stanford University"],
      "DATE": ["2024", "March 2025"]
    }
  }
}
```

## 📝 Requirements

### Core Dependencies
```
numpy==1.24.3
PyPDF2
python-docx
pytesseract
pillow
PyMuPDF
spacy
transformers
sentence-transformers
nltk
textstat
streamlit
pandas
```

### System Requirements
- Python 3.7+
- 4GB+ RAM (recommended for ML models)
- Tesseract OCR
- Internet connection (for model downloads)

## 🐛 Troubleshooting

### Common Issues

**OCR Not Working:**
```bash
# Verify Tesseract installation
tesseract --version

# Install language packs if needed
sudo apt-get install tesseract-ocr-eng
```

**spaCy Model Missing:**
```bash
python -m spacy download en_core_web_sm
```
