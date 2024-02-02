import os


# recursively rename files in a directory
def rename_files_in_dir(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)

            # get filename without extension
            filename, file_extension = os.path.splitext(file)
            # use new extension, .png to .jpg
            new_name = filename + ".jpg"

            os.rename(file_path, os.path.join(root, new_name))

            print(f"Renamed {file} to {new_name}")

        for dir in dirs:
            rename_files_in_dir(dir)


if __name__ == "__main__":
    # rename files in the current directory
    rename_files_in_dir(os.path.join(os.path.dirname(__file__), "data"))
    print("Done!")
