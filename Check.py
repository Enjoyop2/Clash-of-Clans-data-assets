import os
import json

folder_path = "./"

def check_jsonformat_files(root_folder):
	log_entries = []

	for root, dirs, files in os.walk(root_folder):
		for file in files:
			if file.lower().endswith(".json"):
				file_path = os.path.join(root, file)

				try:
					with open(file_path, 'r', encoding='utf-8') as f:
						json.load(f)
				except Exception as e:
					log_entries.append(f"HATALI DOSYA: {file_path}\nHATA: {str(e)}\n")

	log_file_path = os.path.join(os.getcwd(), "jsonerrorlog.txt")

	with open(log_file_path, "w", encoding="utf-8") as log_file:
		if log_entries:
			log_file.write("\n".join(log_entries))
		else:
			log_file.write("Tüm JSON dosyaları doğru formatta.\n")

	print(f"Kontrol tamamlandı. Log dosyası: {log_file_path}")


def check_nullfolder_delete(root_folder):
	for root, dirs, files in os.walk(root_dir, topdown=False):
		for dir_name in dirs:
			full_path = os.path.join(root, dir_name)

			if not os.listdir(full_path):
				os.rmdir(full_path)
				print(f"Silindi: {full_path}")

	print("İşlem bitti")

def null_files_search(folder_path):
	null_files = []
	for root, dirs, files in os.walk(folder_path):
		for dosya in files:
			file_path = os.path.join(root, dosya)
			try:
				boyut = os.path.getsize(file_path)
				if boyut < 1:
					null_files.append(file_path)
			except OSError as e:
				print(f"Hata oluştu: {file_path} -> {e}")
	print(f"boş dosyalar: {null_files}")

check_jsonformat_files(folder_path)
