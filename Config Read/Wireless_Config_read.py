import sys

def section_with_bounds(file_name):
    start_patterns = ('config wireless-controller',)
    end_patterns = ('end',)

    with open(file_name) as f:
        section_in_play = False
        for line in f:
            if any(line.startswith(pattern) for pattern in start_patterns):
                section_in_play = True
            if section_in_play:
                print(line, end='')
            if any(line.startswith(pattern) for pattern in end_patterns):
                section_in_play = False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <file_name>")
        sys.exit(1)
    file_name = sys.argv[1]
    section_with_bounds(file_name)



