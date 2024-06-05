import os
import zipfile

def list_files(directory):
    """List all files in the given directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def delete_files(files, directory):
    """Delete the specified files from the given directory."""
    for file in files:
        os.remove(os.path.join(directory, file))

def extract_zip_files(directory):
    """Extract all zip files in the given directory and delete the zip files."""
    zip_files = [f for f in os.listdir(directory) if f.endswith('.zip')]
    for zip_file in zip_files:
        with zipfile.ZipFile(os.path.join(directory, zip_file), 'r') as zip_ref:
            zip_ref.extractall(directory)
        os.remove(os.path.join(directory, zip_file))

def display_files(directory):
    """Display all files in the given directory."""
    files = list_files(directory)
    print(f"Files in {directory}: {files}")

def extraction(directory):
    # Display and delete existing files
    #  existing_files = list_files(directory)
    # if existing_files:
    #     print("Existing files:")
    #     for file in existing_files:
    #         print(file)
    #     delete_files(existing_files, directory)
    #     print("Deleted existing files.")

    # Check for zip files, extract them and delete the zip files
    extract_zip_files(directory)
    print("Extraction Complete!")

    # Display the files present after extraction
    display_files(directory)

