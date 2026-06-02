import requests

# Example URL for a specific DCU version (replace with the latest from Dell)
dcu_url = "https://dl.dell.com/FOLDER14424601M/1/Dell-Command-Update-Windows-Universal-Application_FGK9X_WIN64_5.7.0_A00.EXE"
local_filename = "DellCommandUpdate.exe"

def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Download complete: {filename}")
    else:
        print(f"Failed to download. Status code: {response.status_code}")

download_file(dcu_url, local_filename)
