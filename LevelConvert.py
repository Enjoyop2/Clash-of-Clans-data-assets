import os
import json
import json5

class JsonConverter:
	def __init__(self, root_dir: str = None, overwrite: bool = False):
		if root_dir is None:
			self.root_dir = os.path.dirname(os.path.abspath(__file__))
		else:
			self.root_dir = root_dir

		self.overwrite = overwrite

	def get_all_files(self):
		file_list = []
		for root, dirs, files in os.walk(self.root_dir):
			for file in files:
				file_list.append(os.path.join(root, file))
		return file_list

	def get_all_level_files(self):
		file_list = []
		for root, dirs, files in os.walk(self.root_dir):
			path_parts = root.split(os.sep)
			if "level" in path_parts:
				for file in files:
					file_list.append(os.path.join(root, file))
			else:
				continue
		return file_list


	def convert_json_to_json5(self, file_path: str):
		try:
			with open(file_path, "r", encoding="utf-8") as f:
				data = json.load(f)

			minified = json5.dumps(data, separators=(",", ":"), ensure_ascii=False)
			new_path = file_path.replace(".json", ".json5")

			with open(new_path, "w", encoding="utf-8") as f:
				f.write(minified)

			print(f"Converted JSON → JSON5: {new_path}")
			return True

		except Exception as e:
			print(f"Error converting JSON {file_path}: {e}")
			return False

	def convert_json5_to_json(self, file_path: str):
		try:
			with open(file_path, "r", encoding="utf-8") as f:
				data = json5.load(f)

			minified = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
			new_path = file_path.replace(".json5", ".json")

			with open(new_path, "w", encoding="utf-8") as f:
				f.write(minified)

			print(f"Converted JSON5 → JSON: {new_path}")
			return True

		except Exception as e:
			print(f"Error converting JSON5 {file_path}: {e}")
			return False

	def convert_all_json_to_json5(self):
		success_files = []

		for file in self.get_all_level_files():
			if file.endswith(".json"):
				if self.convert_json_to_json5(file):
					success_files.append(file)

		for file in success_files:
			try:
				os.remove(file)
				print(f"Deleted original JSON: {file}")
			except Exception as e:
				print(f"Error deleting JSON {file}: {e}")

	def convert_all_json5_to_json(self):
		success_files = []

		for file in self.get_all_level_files():
			if file.endswith(".json5"):
				if self.convert_json5_to_json(file):
					success_files.append(file)

		for file in success_files:
			try:
				os.remove(file)
				print(f"Deleted original JSON5: {file}")
			except Exception as e:
				print(f"Error deleting JSON5 {file}: {e}")


if __name__ == "__main__":
	converter = JsonConverter()
	converter.convert_all_json_to_json5()
	#converter.convert_all_json5_to_json()
