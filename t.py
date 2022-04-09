import json
import sys

j = json.load(open(sys.argv[1]))
uncovered_files = {}
for data in j["data"]:
    for file in data["files"]:
        filename = file["filename"]
        lines = {}
        if "segments" not in file:
            continue
        for segment in file["segments"]:
            # Line, Col, Count, HasCount, IsRegionEntry, IsGapRegion
            line = segment[0]
            count = segment[2]
            has_count = segment[3]
            if not has_count:
                continue
            covered = count > 0
            if line not in lines:
                lines[line] = False
            lines[line] |= covered
        uncovered_lines = []
        for (line, covered) in lines.items():
            if covered:
                continue
            uncovered_lines.append(line)
        if uncovered_lines:
            uncovered_files[filename] = uncovered_lines
if uncovered_files:
    print("Uncovered Lines:")
    for (file, lines) in uncovered_files.items():
        lines = [str(i) for i in lines]
        print("{}: {}".format(file, ", ".join(lines)))
