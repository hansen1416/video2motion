import filecmp
import os
import re

data_dir = os.path.join(".", "anim-json")

filenames = []

counter = 0

# iterate ovedr folder /public/anim-json
for filename in os.listdir(data_dir):
    if filename.endswith(".json"):
        filenames.append(filename)

for fname1 in filenames:
    fname1_no_ext = os.path.splitext(fname1)[0]

    # check if another file with the same name exists
    for fname2 in filenames:
        if fname1 == fname2:
            continue

        # regexp match filenames like "fname1 (1).json"
        if re.match(r"^" + fname1_no_ext + r"\s\(\d+\)\.json$", fname2):
            # print(f"Files {fname1} and {fname2} are the same")

            file1_stats = os.stat(os.path.join(data_dir, fname1))
            file2_stats = os.stat(os.path.join(data_dir, fname2))

            if file1_stats.st_size == file2_stats.st_size:
                print(f"Files {fname1} and {fname2} are the same")

                # unlink fname2
                os.unlink(os.path.join(data_dir, fname2))

                counter += 1


print("Total duplicates: " + str(counter))
