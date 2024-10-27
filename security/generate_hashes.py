"""
 This module is essential for file integrity and security
 Beware it overrides the last file
"""
from pathlib import Path
import json
from config.cfg import enc_module, hash_algo

OUT_PATH = str(Path(__file__).parent.joinpath('hashes.json'))
FILES_TO_HASH = [
    str(Path(__file__).parent.parent.joinpath('convert_mp4_to_mp3.ps1'))
]

hashes = []
if __name__ == '__main__':
    for file_to_hash in FILES_TO_HASH:
        with open(file_to_hash) as r_file:
            content = r_file.read()
            hashes.append(hash_algo(enc_module.encode(content).hexdigest()))
    with open(OUT_PATH,"w") as w_file:
        json.dump(hashes, w_file)
