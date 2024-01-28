import os
import json


def get_filenames_in_folder(folder_path):
    """Retrieves a list of filenames within a specified folder.

    Args:
        folder_path (str): The path to the folder to scan.

    Returns:
        list: A list of filenames within the folder.
    """

    filenames = []
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            filenames.append(filename)
    return filenames


# Example usage:
folder_to_scan = os.path.join(".", "mixamo-fbx")  # Replace with the actual folder path
filenames = get_filenames_in_folder(folder_to_scan)

print(len(filenames))  # This will print the list of filenames

# ... (previous code to get the filenames)

# Save filenames to a JSON file
with open("filenames.json", "w") as file:
    json.dump(filenames, file, indent=4)  # Indent for readability

print("Filenames saved to filenames.json")
