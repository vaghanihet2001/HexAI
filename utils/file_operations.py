import os
def save_to_file(file_name, content):
    try:
        # if not os.path.exists(os.path.dirname(file_name)):
        #     os.makedirs(os.path.dirname(file_name))   
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"✅ File saved as: {file_name}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")



if __name__ =="__main__":
    
    # Example usage:
    file_name = "temp/example.txt"  # You can change this to any filename and extension
    content = "Hello, this is a test file.\nYou can write anything here."

    save_to_file(file_name, content)
