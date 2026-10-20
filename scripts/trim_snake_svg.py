import sys
import re
from pathlib import Path

def trim_snake(svg_path: Path):
    if not svg_path.exists():
        print(f"File not found: {svg_path}")
        return
    
    content = svg_path.read_text(encoding="utf-8")
    
    # 1. Update viewBox to tightly enclose snake movement and grid:
    # X spans -16 to 864 (width 880)
    # Y spans -18 to 128 (height 146) - perfectly fits snake (-16 to 112 + 14.4) and grid (0 to 110)
    # 2. Hide the bottom progress bar (.u) to save 50+ px of dead vertical void
    
    content = re.sub(
        r'<svg\s+viewBox="[^"]+"\s+width="[^"]+"\s+height="[^"]+"',
        '<svg viewBox="-16 -18 880 146" width="880" height="146"',
        content
    )
    
    # Ensure .u progress bar is hidden
    if ".u{" in content:
        content = content.replace(".u{", ".u{display:none;")
    elif ".u {" in content:
        content = content.replace(".u {", ".u { display: none;")
        
    svg_path.write_text(content, encoding="utf-8")
    print(f"Trimmed {svg_path.name}: new viewBox [-16 -18 880 146], height 146")

if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else [
        "github-contribution-grid-snake-dark.svg",
        "github-contribution-grid-snake.svg"
    ]
    for f in files:
        trim_snake(Path(f))
