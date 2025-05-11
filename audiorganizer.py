"""
Simple Python script for sorting MP3 files based on ID3 tag information
Sorts by Artist/Album with options for destination directory and copy/move mode
"""

import os
import shutil
import argparse
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

"""
Sanitize paths since artists' and albums' titles can contain invalid filename characters
@param path: path to sanitize

"""
def sanitize_path(path):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        path = path.replace(char, '-')
    path = path.strip('. ')
    return path


"""
Organize MP3 files into artist/album dirs based on ID3 tags.

@param source_dir: Dir containing the original MP3 files
@param dest_dir: Dir we want to copy to (if not supplied, defaults to source_dir)
@param mode: 'copy' or 'move' to state whether we want to move files directly or to copy them (nondestructive) (defaults to move)

"""
def audiorganizer(source_dir, dest_dir=None, mode='move'):

    dest_dir = dest_dir or source_dir
    file_op = shutil.copy2 if mode == 'copy' else shutil.move

    for filename in os.listdir(source_dir):
        if not filename.lower().endswith('.mp3'):
            continue

        filepath = os.path.join(source_dir, filename)

        try:
            audio = MP3(filepath, ID3=EasyID3)
            artist = audio.get('artist', ['Unknown Artist'])[0]
            album = audio.get('album', ['Unknown Album'])[0]

            # Create directory names with Unicode support
            artist_dir = os.path.join(dest_dir, sanitize_path(artist))
            album_dir = os.path.join(artist_dir, sanitize_path(album))

            os.makedirs(album_dir, exist_ok=True)

            # Move or copy file to new location
            dest_path = os.path.join(album_dir, filename)
            file_op(filepath, dest_path)
            action = "Copied" if mode == 'copy' else "Moved"
            print(f"{action}: {filename} -> {dest_path}")

        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Organize MP3 files by artist/album')
    parser.add_argument('source_dir', help='Directory containing MP3 files')
    parser.add_argument('--dest', dest='dest_dir',
                       help='Destination directory (defaults to source directory)')
    parser.add_argument('--mode', choices=['copy', 'move'], default='move',
                       help='Copy or move files (default: move)')

    args = parser.parse_args()
    audiorganizer(args.source_dir, args.dest_dir, args.mode)
