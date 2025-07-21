import os
import shutil

def create_label_files(template_file_name="template.txt"):
    """
    Creates a copy of a template text file for each PNG image in the current directory,
    renames the copies to match the image names, and places them in a 'labels' subfolder.

    Args:
        template_file_name (str): The name of the template text file.
    """
    current_directory = os.getcwd()
    labels_folder = os.path.join(current_directory, "labels")

    # Create the 'labels' folder if it doesn't exist
    if not os.path.exists(labels_folder):
        os.makedirs(labels_folder)
        print(f"Created 'labels' folder: {labels_folder}")
    else:
        print(f"'labels' folder already exists: {labels_folder}")

    # Check if the template file exists
    template_path = os.path.join(current_directory, template_file_name)
    if not os.path.exists(template_path):
        print(f"Error: Template file '{template_file_name}' not found in the current directory.")
        return

    # Iterate through files in the current directory
    for filename in os.listdir(current_directory):
        if filename.lower().endswith(".png"):
            # Get the base name of the PNG file (e.g., "a" from "a.png")
            image_name_without_extension = os.path.splitext(filename)[0]
            new_txt_filename = f"{image_name_without_extension}.txt"
            destination_path = os.path.join(labels_folder, new_txt_filename)

            try:
                shutil.copyfile(template_path, destination_path)
                print(f"Copied '{template_file_name}' to '{destination_path}'")
            except Exception as e:
                print(f"Error copying file for {filename}: {e}")

# Call the function to run the script
if __name__ == "__main__":
    create_label_files()