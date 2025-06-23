import streamlit as st
import os
import json
import time
from pathlib import Path
from collections import Counter
import tempfile

# Set page config
st.set_page_config(
    page_title="Metadata Generation System",
    page_icon="🔍",
    layout="wide"
)

def check_dependencies():
    """Check if optional dependencies are available"""
    deps = {
        'pdf': False,
        'docx': False,
        'textstat': False
    }
    
    try:
        import PyPDF2
        deps['pdf'] = True
    except ImportError:
        pass
    
    try:
        import docx
        deps['docx'] = True
    except ImportError:
        pass
    
    try:
        import textstat
        deps['textstat'] = True
    except ImportError:
        pass
    
    return deps

def extract_pdf_text(file_path):
    """Extract text from PDF"""
    try:
        import PyPDF2
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except ImportError:
        st.warning("⚠️ PDF extraction requires PyPDF2. Install with: pip install PyPDF2")
        return "[PDF extraction requires PyPDF2 library - install with: pip install PyPDF2]"
    except Exception as e:
        st.error(f"PDF extraction failed: {str(e)}")
        return f"[PDF extraction failed: {str(e)}]"

def extract_docx_text(file_path):
    """Extract text from DOCX"""
    try:
        from docx import Document
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except ImportError:
        st.warning("⚠️ DOCX extraction requires python-docx. Install with: pip install python-docx")
        return "[DOCX extraction requires python-docx library - install with: pip install python-docx]"
    except Exception as e:
        st.error(f"DOCX extraction failed: {str(e)}")
        return f"[DOCX extraction failed: {str(e)}]"

def preprocess_text(text):
    """Basic text preprocessing"""
    if not text:
        return ""
    # Remove extra whitespace and normalize
    text = ' '.join(text.split())
    return text

def classify_document_type(text):
    """Simple document type classification"""
    if not text:
        return "Unknown"
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['abstract', 'introduction', 'methodology', 'conclusion', 'references']):
        return "Academic Paper"
    elif any(word in text_lower for word in ['executive summary', 'business', 'market', 'strategy']):
        return "Business Document"
    elif any(word in text_lower for word in ['chapter', 'novel', 'story']):
        return "Literary Work"
    elif len(text.split()) < 100:
        return "Short Document"
    else:
        return "General Document"

def create_metadata_schema():
    """Create empty metadata schema"""
    return {
        'basic_info': {
            'filename': '',
            'file_type': '',
            'file_size': 0,
            'creation_date': '',
            'processing_date': ''
        },
        'content_analysis': {
            'word_count': 0,
            'character_count': 0,
            'document_type': '',
            'readability_score': 0
        },
        'semantic_data': {
            'summary': '',
            'key_topics': [],
            'entities': {}
        },
        'technical_metadata': {
            'extraction_method': '',
            'processing_time': 0,
            'confidence_score': 0
        }
    }

def generate_basic_metadata_from_text(text, filename):
    """Generate basic metadata from text content"""
    start_time = time.time()
    
    metadata = create_metadata_schema()
    
    # Basic file info
    metadata['basic_info']['filename'] = filename
    metadata['basic_info']['file_type'] = Path(filename).suffix
    metadata['basic_info']['processing_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Preprocess text
    text = preprocess_text(text) if text else ""
    
    # Basic content analysis
    words = text.split() if text else []
    metadata['content_analysis']['word_count'] = len(words)
    metadata['content_analysis']['character_count'] = len(text)
    metadata['content_analysis']['document_type'] = classify_document_type(text)
    
    # Try to calculate readability score
    try:
        import textstat
        if text and len(text.strip()) > 0:
            metadata['content_analysis']['readability_score'] = textstat.flesch_reading_ease(text)
        else:
            metadata['content_analysis']['readability_score'] = 0
    except ImportError:
        metadata['content_analysis']['readability_score'] = 0
        # Only show warning once
        if not hasattr(st.session_state, 'textstat_warning_shown'):
            st.warning("⚠️ For readability scores, install textstat: pip install textstat")
            st.session_state.textstat_warning_shown = True
    except Exception:
        metadata['content_analysis']['readability_score'] = 0
    
    # Simple summary (first 200 characters)
    if text:
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        summary_text = '. '.join(sentences[:2]) + '.' if sentences else text[:200]
        metadata['semantic_data']['summary'] = summary_text + "..." if len(summary_text) > 200 else summary_text
    else:
        metadata['semantic_data']['summary'] = "No text content extracted"
    
    # Basic topics (most frequent meaningful words)
    if text:
        stop_words = {'the', 'and', 'are', 'for', 'with', 'this', 'that', 'from', 'they', 'have', 'been', 'will', 'said', 'each', 'which', 'their', 'time', 'but', 'all', 'can', 'may', 'was', 'were', 'not', 'you', 'your'}
        words_clean = [word.lower().strip('.,!?;:"()[]') for word in words if len(word) > 3 and word.lower() not in stop_words]
        word_freq = Counter(words_clean)
        metadata['semantic_data']['key_topics'] = [word for word, count in word_freq.most_common(5)]
    else:
        metadata['semantic_data']['key_topics'] = []
    
    # Basic entities (simple pattern matching)
    entities = {'PERSON': [], 'ORG': [], 'DATE': [], 'PERCENT': []}
    if text:
        import re
        # Find capitalized words (potential names/organizations)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        entities['PERSON'] = list(set(capitalized))[:5]
        
        # Find dates
        dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}\b', text)
        entities['DATE'] = list(set(dates))[:3]
        
        # Find percentages
        percentages = re.findall(r'\b\d+(?:\.\d+)?%\b', text)
        entities['PERCENT'] = list(set(percentages))
    
    metadata['semantic_data']['entities'] = entities
    
    # Technical metadata
    metadata['technical_metadata']['extraction_method'] = 'Streamlit interface'
    metadata['technical_metadata']['processing_time'] = time.time() - start_time
    metadata['technical_metadata']['confidence_score'] = 0.8 if text else 0.1
    
    return metadata

def main():
    st.title("🔍 Automated Metadata Generation System")
    st.markdown("---")
    
    # Check dependencies and show installation info
    with st.sidebar:
        st.title("📋 System Info")
        
        # Check dependencies
        deps_status = check_dependencies()
        if not all(deps_status.values()):
            st.warning("⚠️ Some optional features require additional packages:")
            if not deps_status['pdf']:
                st.code("pip install PyPDF2")
            if not deps_status['docx']:
                st.code("pip install python-docx")
            if not deps_status['textstat']:
                st.code("pip install textstat")
        else:
            st.success("✅ All dependencies available!")
    
    # Sidebar for options
    st.sidebar.markdown("---")
    st.sidebar.title("Options")
    processing_mode = st.sidebar.selectbox(
        "Choose Processing Mode",
        ["Single File Upload", "Text Input", "Sample Text Demo"]
    )
    
    if processing_mode == "Single File Upload":
        st.header("📁 File Upload")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['txt', 'pdf', 'docx', 'md'],
            help="Supported formats: TXT, PDF, DOCX, MD"
        )
        
        if uploaded_file is not None:
            # Display file info
            st.info(f"**File:** {uploaded_file.name} | **Size:** {uploaded_file.size} bytes")
            
            if st.button("🚀 Generate Metadata", type="primary"):
                with st.spinner("Processing file... Please wait."):
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    try:
                        # Extract text based on file type
                        if uploaded_file.name.lower().endswith('.pdf'):
                            text = extract_pdf_text(tmp_file_path)
                        elif uploaded_file.name.lower().endswith('.docx'):
                            text = extract_docx_text(tmp_file_path)
                        else:
                            text = uploaded_file.getvalue().decode('utf-8', errors='ignore')
                        
                        # Generate metadata
                        metadata = generate_basic_metadata_from_text(text, uploaded_file.name)
                        
                        # Display results
                        display_metadata_results(metadata, text[:500])
                        
                    except Exception as e:
                        st.error(f"Error processing file: {str(e)}")
                    finally:
                        # Clean up temporary file
                        if os.path.exists(tmp_file_path):
                            os.unlink(tmp_file_path)
    
    elif processing_mode == "Text Input":
        st.header("📝 Text Input")
        text_input = st.text_area(
            "Paste your text here:",
            height=200,
            placeholder="Enter or paste the text you want to analyze..."
        )
        
        filename = st.text_input("Document name (optional):", value="user_input.txt")
        
        if st.button("🚀 Generate Metadata", type="primary") and text_input:
            with st.spinner("Analyzing text... Please wait."):
                metadata = generate_basic_metadata_from_text(text_input, filename)
                display_metadata_results(metadata, text_input[:500])
    
    elif processing_mode == "Sample Text Demo":
        st.header("🎯 Sample Text Demo")
        sample_texts = {
            "Academic Paper": """
            Abstract: This research paper investigates the applications of machine learning in natural language processing.
            Introduction: Natural language processing (NLP) has become increasingly important in artificial intelligence.
            The methodology employed in this study involves deep learning techniques and neural networks.
            Results show significant improvements in text classification accuracy.
            Conclusion: The findings demonstrate the effectiveness of modern NLP approaches.
            """,
            "Business Report": """
            Executive Summary: This quarterly business report outlines our company's performance and market strategy.
            Our revenue increased by 15% compared to the previous quarter, driven by strong sales in the technology sector.
            Market analysis indicates growing demand for our products in emerging markets.
            Strategic recommendations include expanding our digital marketing efforts and investing in new technology.
            """,
            "Technical Documentation": """
            Installation Guide: This document provides step-by-step instructions for installing the software.
            System Requirements: Python 3.8 or higher, 4GB RAM minimum, 10GB disk space.
            Configuration: Edit the config.json file to set your preferred settings.
            Troubleshooting: Common issues and their solutions are listed in the appendix.
            """
        }
        
        selected_sample = st.selectbox("Choose a sample text:", list(sample_texts.keys()))
        
        if st.button("🚀 Analyze Sample", type="primary"):
            with st.spinner("Analyzing sample text..."):
                metadata = generate_basic_metadata_from_text(
                    sample_texts[selected_sample], 
                    f"{selected_sample.lower().replace(' ', '_')}.txt"
                )
                display_metadata_results(metadata, sample_texts[selected_sample][:500])

def display_metadata_results(metadata, text_preview):
    """Display metadata results in a formatted way"""
    st.success("✅ Metadata generation completed!")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📝 Content Analysis", "🔍 Semantic Data", "⚙️ Technical Details"])
    
    with tab1:
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Filename", metadata['basic_info']['filename'])
            st.metric("File Type", metadata['basic_info']['file_type'])
            st.metric("Processing Date", metadata['basic_info']['processing_date'])
        
        with col2:
            st.metric("Word Count", metadata['content_analysis']['word_count'])
            st.metric("Character Count", metadata['content_analysis']['character_count'])
            st.metric("Document Type", metadata['content_analysis']['document_type'])
    
    with tab2:
        st.subheader("Content Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Readability Score", f"{metadata['content_analysis']['readability_score']:.1f}")
            st.info("Readability Score: 90-100 = Very Easy, 80-90 = Easy, 70-80 = Fairly Easy, 60-70 = Standard, 50-60 = Fairly Difficult, 30-50 = Difficult, 0-30 = Very Difficult")
        
        with col2:
            if metadata['semantic_data']['key_topics']:
                st.subheader("Key Topics")
                topics_text = ", ".join(metadata['semantic_data']['key_topics'])
                st.write(f"**Topics:** {topics_text}")
                # Display as badges using markdown
                topic_badges = " ".join([f"`{topic}`" for topic in metadata['semantic_data']['key_topics']])
                st.markdown(topic_badges)
    
    with tab3:
        st.subheader("Summary")
        st.write(metadata['semantic_data']['summary'])
        
        st.subheader("Entities Found")
        entities = metadata['semantic_data']['entities']
        
        col1, col2 = st.columns(2)
        with col1:
            if entities.get('PERSON'):
                st.write("**People/Names:**")
                for person in entities['PERSON'][:5]:
                    st.write(f"• {person}")
            
            if entities.get('DATE'):
                st.write("**Dates:**")
                for date in entities['DATE'][:3]:
                    st.write(f"• {date}")
        
        with col2:
            if entities.get('ORG'):
                st.write("**Organizations:**")
                for org in entities['ORG'][:5]:
                    st.write(f"• {org}")
            
            if entities.get('PERCENT'):
                st.write("**Percentages:**")
                for percent in entities['PERCENT']:
                    st.write(f"• {percent}")
    
    with tab4:
        st.subheader("Technical Metadata")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Processing Time", f"{metadata['technical_metadata']['processing_time']:.2f} seconds")
            st.metric("Confidence Score", f"{metadata['technical_metadata']['confidence_score']:.2f}")
        
        with col2:
            st.metric("Extraction Method", metadata['technical_metadata']['extraction_method'])
    
    # Download section
    st.markdown("---")
    st.subheader("💾 Download Results")
    
    col1, col2 = st.columns(2)
    with col1:
        # JSON download
        json_str = json.dumps(metadata, indent=2)
        st.download_button(
            label="📄 Download JSON",
            data=json_str,
            file_name=f"metadata_{metadata['basic_info']['filename']}.json",
            mime="application/json"
        )
    
    with col2:
        # Text preview download
        st.download_button(
            label="📝 Download Text Preview",
            data=text_preview,
            file_name=f"preview_{metadata['basic_info']['filename']}.txt",
            mime="text/plain"
        )
    
    # Raw JSON view (collapsible)
    with st.expander("🔍 View Raw JSON Data"):
        st.json(metadata)

if __name__ == "__main__":
    main()
