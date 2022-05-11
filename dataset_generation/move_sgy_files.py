# Script for moving DAS files to external hard drive as soon as they appear
from configure_sh import configure_sh
import shutil
import time


def move_files():
    download_dir = "../src/"
    destination_dir = r"F:/Research/DAS/Data/"
    # Get the joined dataframe with the name of the file as well as the date
    joined = configure_sh(write_file=False)
    file_names = list(joined['name'])
    num_files = len(file_names)

    start = time.time()
    files_moved = 0
    # Keep trying until all files have been moved to destination
    for file in file_names:
        print(
            f"Waiting for file: {file} -- # Files Moved: {files_moved} -- Elapsed time: {round((time.time() - start) / 60.0, 4)} minutes.")
        moved = False
        # Wait for file to get to the download folder
        while not moved:
            # find file
            try:
                shutil.move(src=download_dir + file, dst=destination_dir + file)
                moved = True
            except (FileNotFoundError, PermissionError) as e:
                pass
        files_moved += 1

    end = time.time()
    print(f"Total Time: {round((end - start) / 60.0, 4)}")


if __name__ == '__main__':
    move_files()
