import sys
import re
from pathlib import Path

def trim_snake(svg_path: Path):
    if not svg_path.exists():
        print(f"File not found: {svg_path}")
        return
    
    content = svg_path.read_text(encoding="utf-8")
    
    # 1. High-contrast electric cyan snake so it stands out against dark grid and green dots
    content = re.sub(r'--cs:[^;]+;', '--cs:#00f0ff;', content)
    
    # 2. Tighten viewBox: top starts at -16, height 144 (eliminates top/bottom dead margins)
    content = re.sub(
        r'<svg\s+viewBox="[^"]+"\s+width="[^"]+"\s+height="[^"]+"',
        '<svg viewBox="-16 -16 880 144" width="880" height="144"',
        content
    )
    
    # 3. Safely hide unneeded progress bar line without breaking any keyframes
    if ".u{" in content and "display:none;" not in content:
        content = content.replace(".u{", ".u{display:none;")
        
    svg_path.write_text(content, encoding="utf-8")
    print(f"Cleanly trimmed {svg_path.name}: high-contrast snake, zero dead margins")

if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else [
        "github-contribution-grid-snake-dark.svg",
        "github-contribution-grid-snake.svg"
    ]
    for f in files:
        trim_snake(Path(f))
