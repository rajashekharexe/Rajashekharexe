import sys
import re
from pathlib import Path

def trim_snake(svg_path: Path):
    if not svg_path.exists():
        print(f"File not found: {svg_path}")
        return
    
    content = svg_path.read_text(encoding="utf-8")
    
    # Ensure snake is vibrant green #39d353 instead of dull purple
    content = content.replace("--cs:purple;", "--cs:#39d353;")
    content = content.replace("--cs: purple;", "--cs: #39d353;")
    
    # Tighten viewBox
    content = re.sub(
        r'<svg\s+viewBox="[^"]+"\s+width="[^"]+"\s+height="[^"]+"',
        '<svg viewBox="-16 -18 880 146" width="880" height="146"',
        content
    )
    
    # Hide unneeded progress bar line
    if ".u{" in content and "display:none;" not in content:
        content = content.replace(".u{", ".u{display:none;")
    elif ".u {" in content and "display: none;" not in content:
        content = content.replace(".u {", ".u { display: none;")
        
    svg_path.write_text(content, encoding="utf-8")
    print(f"Optimized {svg_path.name}")

if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else [
        "github-contribution-grid-snake-dark.svg",
        "github-contribution-grid-snake.svg"
    ]
    for f in files:
        trim_snake(Path(f))
