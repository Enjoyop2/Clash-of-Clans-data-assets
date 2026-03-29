import os

CRC64_TABLE = [0] * 256
for i in range(256):
	res = i
	for j in range(8):
		if res & 1:
			res = (res >> 1) ^ 0xD800000000000000
		else:
			res >>= 1
	CRC64_TABLE[i] = res

def calculate_crc64(text):
	crc = 0xFFFFFFFFFFFFFFFF
	for byte in text.encode("utf-8"):
		crc = (crc >> 8) ^ CRC64_TABLE[(crc ^ byte) & 0xFF]
	return format(crc ^ 0xFFFFFFFFFFFFFFFF, "016x")

def process_localization():
	root_dir = os.getcwd()
	common_dir = os.path.join(root_dir, "ALL_LOCALIZATION")

	if not os.path.exists(common_dir):
		os.makedirs(common_dir)

	total_files_processed = 0

	localization_dirs = []
	for root, dirs, files in os.walk(root_dir):
		if "localization" in root.lower() and "ALL_LOCALIZATION" not in root:
			localization_dirs.append(root)

	for loc_dir in localization_dirs:
		print(f"\n📂 Folder: {loc_dir}")

		csv_files = [
			os.path.join(loc_dir, f)
			for f in os.listdir(loc_dir)
			if f.endswith(".csv")
		]

		for file_path in csv_files:
			fname = os.path.basename(file_path)
			updated_lines = []
			mapping_content = set()

			try:
				with open(file_path, "r", encoding="utf-8") as f:
					lines = f.readlines()

				for line in lines:
					clean_line = line.strip()

					if not clean_line:
						updated_lines.append("\n")
						continue

					h = calculate_crc64(clean_line)
					updated_lines.append(h + "\n")
					mapping_content.add(f"{h},{clean_line}")

				with open(file_path, "w", encoding="utf-8") as f:
					f.writelines(updated_lines)

				if mapping_content:
					common_file_path = os.path.join(common_dir, fname)

					existing_hashes = set()

					if os.path.exists(common_file_path):
						with open(common_file_path, "r", encoding="utf-8") as f:
							for line in f:
								existing_hashes.add(line.split(",")[0])

					new_lines = [
						item for item in mapping_content
						if item.split(",")[0] not in existing_hashes
					]

					if new_lines:
						with open(common_file_path, "a", encoding="utf-8") as f:
							f.write("\n".join(new_lines) + "\n")

				total_files_processed += 1
				print(f"	✔ {fname}")

			except Exception as e:
				print(f"	❌ Error: {file_path} -> {e}")

	print(f"\n🎉 Total number of files processed: {total_files_processed}")

def restore_localization_from_hashes():
	root_dir = os.getcwd()
	common_dir = os.path.join(root_dir, "ALL_LOCALIZATION")

	if not os.path.exists(common_dir):
		print(f"Error: '{common_dir}' folder not found!")
		return

	hash_map = {}
	for root, dirs, files in os.walk(common_dir):
		for file in files:
			if file.endswith(".csv"):
				try:
					with open(os.path.join(root, file), "r", encoding="utf-8") as f:
						for line in f:
							parts = line.strip().split(",", 1)
							if len(parts) == 2:
								h_code, original_text = parts
								hash_map[h_code.strip()] = original_text
				except Exception as e:
					print(f"Dictionary reading error ({file}): {e}")

	if not hash_map:
		print("No matching hash data was found.")
		return

	files_updated = 0
	for root, dirs, files in os.walk(root_dir):
		if "localization" in root.lower() and "ALL_LOCALIZATION" not in root:
			for file in files:
				if file.endswith(".csv"):
					file_path = os.path.join(root, file)
					updated_content = []
					is_modified = False

					try:
						with open(file_path, "r", encoding="utf-8") as f:
							for line in f:
								clean_line = line.strip()

								if clean_line in hash_map:
									updated_content.append(hash_map[clean_line] + "\n")
									is_modified = True
								else:
									updated_content.append(line)

						if is_modified:
							with open(file_path, "w", encoding="utf-8") as f:
								f.writelines(updated_content)
							files_updated += 1

					except Exception as e:
						print(f"File processing error ({file}): {e}")

	print(f"Done. {files_updated} The hashes in the file were replaced with the original text.")

if __name__ == "__main__":
	#process_localization()
	#
	restore_localization_from_hashes()