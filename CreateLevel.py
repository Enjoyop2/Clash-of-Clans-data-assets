import os
import json
import shutil

def print_error(message):
	print(f"\033[91m{message}\033[0m")

def restore_missing_levels():
	root_dir = os.getcwd()
	json_path = os.path.join(root_dir, "AL_LEVELS.json")
	al_levels_dir = os.path.join(root_dir, "AL_LEVELS")

	if not os.path.isfile(json_path):
		print_error("HATA: AL_LEVELS.json bulunamadı!")
		return

	if not os.path.isdir(al_levels_dir):
		print_error("HATA: AL_LEVELS klasörü bulunamadı!")
		return

	with open(json_path, "r", encoding="utf-8") as f:
		data = json.load(f)

	files = data.get("files", [])

	version_map = {}
	for entry in files:
		file_path = entry["file"]
		sha = entry["sha"]

		version = file_path.split("/")[0]
		version_map.setdefault(version, []).append((file_path, sha))

	for item in os.listdir(root_dir):
		item_path = os.path.join(root_dir, item)

		if os.path.isdir(item_path) and item.startswith("v"):
			if item not in version_map:
				print_error(f"{item} klasörü AL_LEVELS.json içinde tanımlı değil!")
				continue

			level_root = os.path.join(item_path, "level")
			os.makedirs(level_root, exist_ok=True)

			print(f"\nKontrol ediliyor: {item}")

			for file_path, sha in version_map[item]:

				relative_path = "/".join(file_path.split("/")[2:])
				destination_file = os.path.join(level_root, relative_path)

				if os.path.isfile(destination_file):
					print(f"Zaten var: {destination_file}")
					continue

				base_name = os.path.splitext(os.path.basename(relative_path))[0]
				source_filename = f"{base_name} - {sha}.json"

				source_file = os.path.join(
					al_levels_dir, os.path.dirname(relative_path), source_filename
				)

				if not os.path.isfile(source_file):
					print_error(f"Kaynak bulunamadı: {source_file}")
					continue

				os.makedirs(os.path.dirname(destination_file), exist_ok=True)

				shutil.copy2(source_file, destination_file)

				print(f"Oluşturuldu: {destination_file}")

	print("\nİşlem Bitti.")

restore_missing_levels()
