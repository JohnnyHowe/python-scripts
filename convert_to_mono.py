from pydub import AudioSegment
from pathlib import Path

# Folder containing audio files
folder = Path(r"C:\Users\Work\Documents\Projects\drifto\Assets\AssetsUnsorted\Sounds\Music\Myst3ry")

# Iterate over all wav and mp3 files
for file_path in folder.rglob("*"):
    if file_path.suffix.lower() in [".wav", ".mp3"]:
        audio = AudioSegment.from_file(file_path)
        if audio.channels > 1:  # Only convert if not already mono
            mono_audio = audio.set_channels(1)
            mono_audio.export(file_path, format=file_path.suffix[1:])
            print(f"Converted {file_path} to mono")
