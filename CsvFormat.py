import os
import csv

folder_path = "./"

def soort_arraycsv_files(root_folder):
	target_files = [ "particle_emitters.csv", "effects.csv" ]

	for root, dirs, files in os.walk(root_folder):
		for file_name in files:
			if file_name.lower() in [d.lower() for d in target_files]:
				file_path = os.path.join(root, file_name)

				with open(file_path, "r", encoding="UTF-8") as f:
					satirlar = f.readlines()

				if len(satirlar) <= 2:
					continue

				basliklar = satirlar[:2]
				veri_satirlari = satirlar[2:]

				gruplar = []
				grup = []

				for satir in veri_satirlari:
					if not satir.startswith(","):
						if grup:
							gruplar.append(grup)
						grup = [satir]
					else:
						grup.append(satir)

				if grup:
					gruplar.append(grup)

				gruplar.sort(key=lambda g: g[0].split(",")[0].strip().lower())

				with open(file_path, "w", encoding="UTF-8") as f:
					f.writelines(basliklar)
					for grup in gruplar:
						f.writelines(grup)

				print(f"{file_path} sıralandı.")

def sort_localization_csv_files(root_folder):
	for root, dirs, files in os.walk(root_folder):
		if "localization" in dirs:
			localization_path = os.path.join(root, "localization")
			csv_files = [f for f in os.listdir(localization_path) if f.endswith(".csv")]
		else:
			csv_path = os.path.join(root, "csv")
			csv_files = []
			if os.path.exists(csv_path):
				for f in ["texts.csv", "texts_patch.csv"]:
					if f in os.listdir(csv_path):
						csv_files.append(f)
				localization_path = csv_path

		for file_name in csv_files:
			file_path = os.path.join(localization_path, file_name)
			with open(file_path, "r", encoding="UTF-8") as f:
				lines = f.readlines()

			if len(lines) <= 2:
				continue

			header = lines[0]
			data_lines = lines[1:]

			data_lines.sort()

			with open(file_path, "w", encoding="UTF-8") as f:
				f.writelines([header] + data_lines)

			print(f"{file_path} sıralandı.")


def fix_boolean_columns(root_folder):
	for root, dirs, files in os.walk(root_folder):
		for file_name in files:
			if file_name.lower().endswith(".csv"):
				file_path = os.path.join(root, file_name)

				with open(file_path, mode="r", newline="", encoding="UTF-8") as f:
					reader = list(csv.reader(f))

				if len(reader) < 2:
					continue

				baslik = reader[0]
				kolon_tipleri = reader[1]

				boolean_indexler = [i for i, tip in enumerate(kolon_tipleri) if tip.lower() == "boolean"]

				updated = False

				for row in reader[2:]:
					for i in boolean_indexler:
						if i < len(row) and row[i].strip() != "":

							if row[i].strip().lower() == "true":
								row[i] = "TRUE"
								updated = True

							elif row[i].strip().lower() == "false":
								row[i] = "FALSE"
								updated = True

						else:
							updated = False
				if updated:
					with open(file_path, mode="w", newline="", encoding="UTF-8") as f:
						writer = csv.writer(f, lineterminator="\n")
						writer.writerows(reader)

					print(f"{file_path} güncellendi (Boolean kolonlar).")

				else:
					print(f"\033[91m{file_path} güncellenemedi (Boolean kolonlar).\033[0m")
	print("İşlem Bitti")

def check_csv_files(root_folder):
	for root, dirs, files in os.walk(root_folder):
		for file_name in files:
			if file_name.endswith(".csv"):
				file_path = os.path.join(root, file_name)
				with open(file_path, mode="r", newline="", encoding="UTF-8") as infile:
					reader = csv.reader(infile)
					rows = list(reader)

				updated = False

				if len(rows) > 1:
					for i in range(len(rows[1])):

						if rows[1][i] == "string":
							rows[1][i] = "String"
							updated = True

						elif rows[1][i] == "String":
							rows[1][i] = "String"
							updated = True

						elif rows[1][i] == "Int":
							rows[1][i] = "int"
							updated = True

						elif rows[1][i] == "Boolean":
							rows[1][i] = "boolean"
							updated = True
				else:
					updated = False

				if updated:
					with open(file_path, mode="w", newline="", encoding="UTF-8") as outfile:
						writer = csv.writer(outfile, lineterminator="\n")
						writer.writerows(rows)
					print(f"{file_path} güncellendi.")

				else:
					print(f"\033[91m{file_path} güncellenemedi.\033[0m")

	print("İşlem Bitti")

soort_arraycsv_files(folder_path)
sort_localization_csv_files(folder_path)
#check_csv_files(folder_path)
#fix_boolean_columns(folder_path)
