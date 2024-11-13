# WomenHealth AI Assistant

An AI-powered medical Q&A system that provides reliable health information for women based on FDA-approved resources.

## 🌟 Project Overview

This project aims to create a reliable AI assistant for women's health inquiries by:
- Scraping and processing FDA-approved medical information
- Generating high-quality Q&A pairs using Gemini API
- Fine-tuning an AI model for accurate medical responses

## 🛠️ Technical Architecture

### Data Collection & Processing
- `collect.py`: Website scraping script
- `clean_text.py`: Text cleaning and preprocessing
- `scraper.ipynb`: Jupyter notebook for data collection
- `unique_links.json`: Storage for unique website URLs
- `content_list.json`: Raw scraped content

### Data Transformation
- `transform_csv.py`: Converts processed data to training format
- `final_filtered_qa.json`: Cleaned Q&A pairs
- `test_qa.json`: Test dataset
- `training_data_20241113.csv`: Training dataset

## 📦 Project Structure
```
.
├── _pycache_/
├── qa_output/          # Generated Q&A outputs
├── .gitignore         # Git ignore rules
├── clean_text.py      # Text cleaning utilities
├── collect.py         # Data collection script
├── content_list.json  # Scraped content
├── scraper.ipynb      # Scraping notebook
├── transform_csv.py   # CSV transformation
└── README.md         # Project documentation
```

## 🚀 Getting Started

1. **Environment Setup**
```bash
# Clone the repository
git clone https://github.com/yourusername/WomenHealth-AI.git

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your Gemini API key to .env
```

2. **Data Processing**
```bash
# Run data collection
python collect.py

# Clean and process text
python clean_text.py

# Generate Q&A pairs
python transform_csv.py
```

3. **Model Training**
- Upload the generated CSV to Google AI Studio
- Fine-tune the model with appropriate parameters
- Test the model with sample queries

## ⚙️ Configuration

Create a `.env` file with:
```
GEMINI_API_KEY=your_api_key_here
BASE_DIR=your_project_directory
```

## 🔑 Key Features

- FDA-approved medical information
- Structured Q&A generation
- Data cleaning and validation
- Model fine-tuning capabilities
- Comprehensive documentation

## 📊 Data Pipeline

1. Web Scraping → `collect.py`
2. Text Cleaning → `clean_text.py`
3. Q&A Generation → Gemini API
4. Data Transformation → `transform_csv.py`
5. Model Training → Google AI Studio

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
