import json
import os

TARGET_FILES = {"calendar.json", "globals.json"}


def format_json(data, indent_char="\t"):
	"""
	JSON'u temiz şekilde formatlar:
	- Boş listeleri [] olarak yazar
	- Dict ve listeleri indent ile biçimlendirir
	- Key'leri alfabetik sıraya göre sıralar
	"""

	def sort_obj(obj):
		if isinstance(obj, dict):
			return {k: sort_obj(obj[k]) for k in sorted(obj)}
		elif isinstance(obj, list):
			return [sort_obj(i) for i in obj]
		return obj

	def render(obj, level=0):
		indent = indent_char * level
		next_indent = indent_char * (level + 1)

		if isinstance(obj, dict):
			if not obj:
				return "{}"
			items = []
			for k, v in obj.items():
				items.append(f'{next_indent}"{k}": {render(v, level + 1)}')
			return "{\n" + ",\n".join(items) + f"\n{indent}" + "}"

		elif isinstance(obj, list):
			if not obj:
				return "[]"

			# Tek satır yazılabilecek dict listesi
			if all(
				isinstance(i, dict) and
				all(not isinstance(v, (dict, list)) for v in i.values())
				for i in obj
			):
				items = [
					"{" + ", ".join(f'"{k}": {json.dumps(v, ensure_ascii=False)}' for k, v in i.items()) + "}"
					for i in obj
				]
				return "[\n" + ",\n".join(f"{next_indent}{item}" for item in items) + f"\n{indent}]"

			# Normal liste
			items = [f"{next_indent}{render(i, level + 1)}" for i in obj]
			return "[\n" + ",\n".join(items) + f"\n{indent}]"

		return json.dumps(obj, ensure_ascii=False)

	sorted_data = sort_obj(data)
	return render(sorted_data)


def process_file(path):
	try:
		with open(path, "r", encoding="utf-8") as f:
			data = json.load(f)

		formatted = format_json(data)

		with open(path, "w", encoding="utf-8") as f:
			f.write(formatted)

		print(f"✔ Formatted: {path}")

	except Exception as e:
		print(f"✖ Skipped (error): {path} -> {e}")


def main():
	root_dir = os.getcwd()

	for root, dirs, files in os.walk(root_dir):
		for file in files:
			if file in TARGET_FILES:
				full_path = os.path.join(root, file)
				process_file(full_path)


if __name__ == "__main__":
	main()
