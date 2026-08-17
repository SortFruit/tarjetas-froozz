import os
import re
import json

EXCLUDE = {".git", ".github"}

def strip_tags(s):
    return re.sub(r"<[^<]+?>", "", s).strip()

def main():
    people = []
    for entry in sorted(os.listdir(".")):
        if entry in EXCLUDE or not os.path.isdir(entry):
            continue
        index_path = os.path.join(entry, "index.html")
        if not os.path.isfile(index_path):
            continue
        with open(index_path, encoding="utf-8") as f:
            html = f.read()

        name_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        role_match = re.search(r'<p class="role"[^>]*>(.*?)</p>', html, re.S)
        if not name_match:
            continue

        name = strip_tags(name_match.group(1))
        role = strip_tags(role_match.group(1)) if role_match else ""
        people.append({"name": name, "role": role, "slug": entry})

    with open("people.json", "w", encoding="utf-8") as f:
        json.dump(people, f, ensure_ascii=False, indent=2)

    print(f"Generadas {len(people)} entradas en people.json")

if __name__ == "__main__":
    main()
