import os
import shutil
import hashlib

root_dir = os.getcwd()

levels_dir = os.path.join(root_dir, "AL_LEVELS")
os.makedirs(levels_dir, exist_ok=True)

for item in os.listdir(root_dir):
	item_path = os.path.join(root_dir, item)

	if os.path.isdir(item_path) and item.startswith("v"):
		level_folder = os.path.join(item_path, "level")

		if os.path.isdir(level_folder):

			for root, dirs, files in os.walk(level_folder):
				for file in files:
					if file.endswith(".json"):
						source_file = os.path.join(root, file)

						with open(source_file, "rb") as f:
							file_hash = hashlib.sha1(f.read()).hexdigest()

						new_filename = f"{os.path.splitext(file)[0]} - {file_hash}.json"

						relative_path = os.path.relpath(root, level_folder)

						destination_folder = os.path.join(levels_dir, relative_path)
						os.makedirs(destination_folder, exist_ok=True)

						destination_file = os.path.join(destination_folder, new_filename)
						shutil.copy2(source_file, destination_file)

print("İşlem bitti")
