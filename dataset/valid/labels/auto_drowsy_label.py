import os

def replace_leading_zero_in_files(folder_path):
    """
    Goes through all .txt files in the given folder and replaces
    a leading '0 ' with '1 ' on each line where it occurs.

    Args:
        folder_path (str): The path to the folder containing the .txt files.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found at '{folder_path}'")
        return

    print(f"Searching for .txt files in: {folder_path}")
    processed_files_count = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            print(f"Processing file: {filepath}")

            try:
                # Read the original content
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                modified_lines = []
                changes_made_in_file = False
                for line in lines:
                    # Check if the line starts with '0 '
                    if line.startswith('0 '):
                        modified_lines.append('1 ' + line[2:]) # Replace '0 ' with '1 '
                        changes_made_in_file = True
                    else:
                        modified_lines.append(line)

                # Write the modified content back to the file if changes were made
                if changes_made_in_file:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(modified_lines)
                    print(f"  - Changes applied to '{filename}'")
                    processed_files_count += 1
                else:
                    print(f"  - No changes needed for '{filename}'")

            except Exception as e:
                print(f"  - Error processing '{filename}': {e}")

    print(f"\nFinished processing. Total files modified: {processed_files_count}")

# --- How to use the script ---
# IMPORTANT: Replace 'your_folder_path_here' with the actual path to your folder.
# Example:
# folder_to_process = "/Users/yourusername/Documents/my_text_files"
# folder_to_process = "C:\\Users\\yourusername\\Documents\\my_text_files"
# Or, if the script is in the same directory as your files, you can use '.'
# folder_to_process = "."

# Uncomment the line below and set your folder path to run the script:
# replace_leading_zero_in_files(folder_to_process)

# For demonstration, let's create a dummy folder and files if they don't exist
# You can remove this part when you use the script for your actual files.
def create_dummy_files(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created dummy folder: {path}")

    with open(os.path.join(path, "file1.txt"), "w") as f:
        f.write("0 This is line one.\n")
        f.write("1 This is line two.\n")
        f.write("0 Another line starting with zero.\n")
        f.write("Something else.\n")
    with open(os.path.join(path, "file2.txt"), "w") as f:
        f.write("0 Hello world.\n")
        f.write("No zero here.\n")
        f.write("0 End with zero.\n")
    with open(os.path.join(path, "other.log"), "w") as f:
        f.write("0 This should not change.\n")
    print("Created dummy .txt files for testing.")

# --- Demo Usage ---
# Create a temporary folder for testing
#test_folder = "test_text_files"
#create_dummy_files(test_folder)

# Now, run the main function on the test folder
replace_leading_zero_in_files(".")

# You can optionally clean up the dummy folder and files after testing
# import shutil
# shutil.rmtree(test_folder)
# print(f"Cleaned up dummy folder: {test_folder}")