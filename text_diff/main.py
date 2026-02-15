import difflib
import sys
from pathlib import Path

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def char_diff(text1, text2):
    matcher = difflib.SequenceMatcher(None, text1, text2)
    result = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            result.append(text1[i1:i2])
        elif tag == "delete":
            result.append(colored(text1[i1:i2], "91"))   # red
        elif tag == "insert":
            result.append(colored(text2[j1:j2], "92"))   # green
        elif tag == "replace":
            result.append(colored(text1[i1:i2], "91"))   # red
            result.append(colored(text2[j1:j2], "92"))   # green

    return "".join(result)

def main():
    if len(sys.argv) != 3:
        print("Usage: python char_diff.py file1.txt file2.txt")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    if not Path(file1).exists() or not Path(file2).exists():
        print("One of the files does not exist.")
        sys.exit(1)

    text1 = read_file(file1)
    text2 = read_file(file2)

    diff_result = char_diff(text1, text2)
    print(diff_result)

if __name__ == "__main__":
    main()
