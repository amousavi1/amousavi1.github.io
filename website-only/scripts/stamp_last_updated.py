from pathlib import Path

old = 'datetime="2026-09-19T22:20:00-04:00">September 19, 2026, 10:20 PM EDT'
new = 'datetime="2026-09-20T18:55:00-04:00">September 20, 2026, 6:55 PM EDT'
root = Path(__file__).resolve().parents[2]
count = 0
for path in root.rglob("*.html"):
    if "node_modules" in path.parts:
        continue
    text = path.read_text(encoding="utf-8")
    if old in text:
        path.write_text(text.replace(old, new), encoding="utf-8", newline="\n")
        count += 1
print(f"updated {count} html files")
