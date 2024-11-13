import json
import google.generativeai as genai
import time
import re
import os
from dotenv import load_dotenv

# Configuration
load_dotenv()

# Configuration
API_KEY = os.getenv('GEMINI_API_KEY')

BASE_DIR = r"D:\geminiapisport"
OUTPUT_DIR = os.path.join(BASE_DIR, "qa_output")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def is_english(text):
    """Check if text is primarily in English"""
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    total_chars = len(re.findall(r'\w', text))
    return total_chars > 0 and (english_chars / total_chars) > 0.7

def clean_text(text):
    """Clean and format text"""
    # Remove FDA contact information and reporting instructions
    text = re.sub(r'report.*?FDA.*?1-\d{3}-\d{3}-\d{4}\.?', '', text, flags=re.IGNORECASE|re.DOTALL)
    text = re.sub(r'contact.*?FDA.*?\.', '', text, flags=re.IGNORECASE)
    text = re.sub(r'call.*?FDA.*?\.', '', text, flags=re.IGNORECASE)
    text = re.sub(r'visit.*?fda\.gov.*?\.', '', text, flags=re.IGNORECASE)
    text = re.sub(r'www\.fda\.gov\S*', '', text)
    
    # Remove phone numbers
    text = re.sub(r'1-\d{3}-\d{3}-\d{4}', '', text)
    
    # Remove line breaks and extra spaces
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Remove other common FDA phrases
    text = re.sub(r'Report problems to FDA[^.]*\.', '', text, flags=re.IGNORECASE)
    text = re.sub(r'FDA recommends[^.]*\.', '', text, flags=re.IGNORECASE)
    text = re.sub(r'FDA advises[^.]*\.', '', text, flags=re.IGNORECASE)
    text = re.sub(r'FDA encourages[^.]*\.', '', text, flags=re.IGNORECASE)
    
    # Clean extra spaces and punctuation
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'\s+\.', '.', text)
    
    return text.strip()

def generate_qa(text, index):
    """Generate Q&A pairs"""
    print(f"\nProcessing text block {index}")
    
    if not is_english(text):
        print("Non-English content, skipping")
        return []
    
    cleaned_text = clean_text(text)
    print("\nFirst 200 characters of cleaned text:")
    print(cleaned_text[:200] + "...")
    
    prompt = f"""Generate 3 medical question-answer pairs based on this text:
    {cleaned_text[:5000]}
    
    Format your response strictly as a JSON array:
    [
      {{"text_input": "question1", "output": "answer1"}},
      {{"text_input": "question2", "output": "answer2"}},
      {{"text_input": "question3", "output": "answer3"}}
    ]"""
    
    try:
        print("Sending request to API...")
        response = model.generate_content(prompt)
        print("Response received")
        
        try:
            json_text = re.search(r'\[(.*?)\]', response.text, re.DOTALL)
            if json_text:
                response_text = f'[{json_text.group(1)}]'
                qa_pairs = json.loads(response_text)
                print(f"Successfully parsed {len(qa_pairs)} Q&A pairs")
                
                # Add index and timestamp
                for qa in qa_pairs:
                    qa['index'] = index
                    qa['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Save current block results
                output_file = os.path.join(OUTPUT_DIR, f"qa_pairs_{index}.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "index": index,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "original_text": cleaned_text[:200] + "...",  # Save cleaned text snippet for verification
                        "qa_pairs": qa_pairs
                    }, f, ensure_ascii=False, indent=2)
                print(f"Saved to {output_file}")
                
                return qa_pairs
                
            else:
                print("No valid JSON data found in response")
                return []
            
        except json.JSONDecodeError as je:
            print(f"JSON parsing error: {str(je)}")
            return []
            
    except Exception as e:
        print(f"API request error: {str(e)}")
        return []

def process_all_content():
    """Process all content"""
    all_qa_pairs = []
    failed_indices = []
    skipped_indices = []
    
    try:
        print("Reading content_list.json...")
        content_file = os.path.join(BASE_DIR, "content_list.json")
        with open(content_file, 'r', encoding='utf-8') as file:
            content_list = json.load(file)
            
        total_items = len(content_list)
        print(f"Found {total_items} content blocks")
        
        for i, item in enumerate(content_list, 1):
            print(f"\nProcessing block {i}/{total_items}")
            
            content = item['content']
            if not is_english(content):
                print(f"Block {i} is not in English, skipping")
                skipped_indices.append(i)
                continue
                
            qa_pairs = generate_qa(content, i)
            
            if qa_pairs:
                all_qa_pairs.extend(qa_pairs)
                print(f"Successfully generated {len(qa_pairs)} Q&A pairs")
            else:
                failed_indices.append(i)
                print(f"Processing failed: Block {i}")
            
            time.sleep(2)
            
        # Save summary results
        if all_qa_pairs:
            final_output = {
                "total_items": total_items,
                "successful_items": total_items - len(failed_indices) - len(skipped_indices),
                "failed_items": len(failed_indices),
                "skipped_items": len(skipped_indices),
                "total_qa_pairs": len(all_qa_pairs),
                "qa_pairs": all_qa_pairs
            }
            
            with open(os.path.join(OUTPUT_DIR, 'all_qa_pairs.json'), 'w', encoding='utf-8') as f:
                json.dump(final_output, f, ensure_ascii=False, indent=2)
        
        print("\nProcessing complete!")
        print(f"Total content blocks: {total_items}")
        print(f"Successfully processed: {total_items - len(failed_indices) - len(skipped_indices)}")
        print(f"Processing failed: {len(failed_indices)}")
        print(f"Skipped non-English: {len(skipped_indices)}")
        print(f"Total Q&A pairs generated: {len(all_qa_pairs)}")
        print(f"\nAll results saved to {OUTPUT_DIR} directory")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")

if __name__ == "__main__":
    try:
        print("Initializing Gemini API...")
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        print("Starting content processing...")
        process_all_content()
        
    except Exception as e:
        print(f"Program execution error: {str(e)}")