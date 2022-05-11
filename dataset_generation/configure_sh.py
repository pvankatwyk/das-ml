import pandas as pd


def configure_sh(write_file=True):
    """
    Function for joining the CSV of files needed for the study and the wget commands from the full .sh file (downloaded
    from FORGE website).

    :param write_file: True if you want the file written to a base script
    :return: joined [pd.DataFrame]: dataframe of all files needed and wget commands
    """
    all_paths = pd.read_csv(r'../src/all_paths.csv')
    files_needed = pd.read_csv(r'../src/files_needed.csv')
    joined = all_paths.merge(files_needed, on="name", how="inner")

    # Concatenate to get full bash command for each file
    url_path = r"wget https://pando-rgw01.chpc.utah.edu/"
    joined['bash'] = url_path + joined['day'] + "/" + joined["name"]

    # Create multi-line string with command
    bash_string = "\n".join(list(joined['bash']))

    # Create bash script
    if write_file:
        with open('../src/get_cataloged.sh', 'w') as sh:
            sh.write(f"""#!/bin/bash
        {bash_string}""")

    return joined


if __name__ == '__main__':
    joined = configure_sh(write_file=True)
