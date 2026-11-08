from pathlib import Path

file = Path(__file__).with_name("file.txt")

def main():
    with open(file, "r", encoding="utf-8") as f:
        s = f.read()
        print(type(bytes(s, encoding="utf-8")))
        print(s)

if __name__ == "__main__":
    main()
