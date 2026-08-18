import os
import yaml

vault_path = r"C:\Users\prahn\OneDrive\Documents\IITM-Pravartak\Pravartak_Practice"

print("Starting to scan vault...")

for root, dirs, files in os.walk(vault_path):
    # Skip hidden folders like .obsidian or .trash
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check if the file starts with the properties section
                if content.startswith("---"):
                    # Split into 3 parts: empty space before, YAML text, and note body
                    parts = content.split("---", 2)
                    
                    if len(parts) >= 3:
                        yaml_text = parts[1].strip()
                        
                        # Only parse if there is actually text inside the dashes
                        if yaml_text:
                            metadata = yaml.safe_load(yaml_text)
                            print(f"File: {file}")
                            print(f"Properties: {metadata}")
                            print("-" * 40)
                            
            except Exception as e:
                print(f"Could not read {file}: {e}")

print("Scan complete!")