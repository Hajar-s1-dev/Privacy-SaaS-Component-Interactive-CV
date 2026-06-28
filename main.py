import os
import json
import uuid
from anonymizer import CVProcessor

INDEX_FILE = "cv_mapping_index.json"

def load_mapping_index():
   
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_mapping_index(index_data):
  
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=4, ensure_ascii=False)

def run_cv_anonymizer(pdf_filename):
    print(f"\n--- ⏳ Reading CV: {pdf_filename} ---")
    try:
       
        cv_id = f"CV_{uuid.uuid4().hex[:8].upper()}"
        processor = CVProcessor(pdf_filename)
        cleaned_text = processor.anonymize()
        
   
        output_txt_file = f"anonymized_{cv_id}.txt"
        with open(output_txt_file, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
            
        mapping_index = load_mapping_index()
        
       
        clean_search_content = " ".join(cleaned_text.lower().split())
        
        mapping_index[cv_id] = {
            "original_pdf": pdf_filename,
            "anonymized_file": output_txt_file,
            "search_content": clean_search_content
        }
        save_mapping_index(mapping_index)
        
        print(f"✅ Success! Generated ID: {cv_id} | Safe file: '{output_txt_file}'")
    except FileNotFoundError:
        print(f"❌ Error: File '{pdf_filename}' not found. Please check the folder.")
    except Exception as e:
        print(f"❌ Error processing CV: {e}")

def search_cv_by_keywords(keywords_string):
 
    keywords_list = [kw.strip().lower() for kw in keywords_string.replace(",", " ").split() if kw.strip()]
    
    if not keywords_list:
        print("⚠️ Please enter valid keywords.")
        return

    print(f"\n🔍 --- Searching for CVs containing: {keywords_list} ---")
    mapping_index = load_mapping_index()
    results = []

    for cv_id, info in mapping_index.items():
        cv_text = info.get("search_content", "")
        
   
        match_all = True
        for kw in keywords_list:
            if kw not in cv_text:
                match_all = False
                break
                
        if match_all:
            results.append({
                "cv_id": cv_id,
                "original_pdf": info["original_pdf"],
                "anonymized_file": info["anonymized_file"]
            })

    
    if results:
        print(f"\n🎯 Found {len(results)} matching CV(s):")
        for res in results:
            print(f"  📌 [{res['cv_id']}] -> Text File: {res['anonymized_file']} (Original: {res['original_pdf']})")
    else:
        print("❌ No matching CVs found with these keywords.")

# --- INTERACTIVE TERMINAL MENU ---
def main_menu():
    while True:
        print("\n" + "="*40)
        print("     💼 CV ANONYMIZER & SEARCH APP     ")
        print("="*40)
        print("[1] Anonymize a new CV PDF")
        print("[2] Search CVs by Keywords")
        print("[3] Exit")
        print("="*40)
        
        choix = input("👉 Choose an option (1-3): ").strip()
        
        if choix == "1":
            pdf_name = input("\n📝 Enter the exact PDF file name (e.g., test_cv): ").strip()
            if pdf_name:
                # Automatic fix ila nsayti .pdf l-ekher
                if not pdf_name.lower().endswith('.pdf'):
                    pdf_name = pdf_name + '.pdf'
                run_cv_anonymizer(pdf_name)
            else:
                print("⚠️ File name cannot be empty!")
                
        elif choix == "2":
            kws = input("\n🔑 Enter keywords (separated by spaces or commas): ").strip()
            search_cv_by_keywords(kws)
            
        elif choix == "3":
            print("\n👋 Goodbye! Application closed.")
            break
        else:
            print("⚠️ Invalid option! Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()