import sys
import re
from pathlib import Path

def trim_snake(svg_path: Path):
    if not svg_path.exists():
        print(f"File not found: {svg_path}")
        return
    
    content = svg_path.read_text(encoding="utf-8")
    
    # 1. Ensure snake color is vibrant neon green #39d353 instead of dull purple
    content = content.replace("--cs:purple;", "--cs:#39d353;")
    content = content.replace("--cs: purple;", "--cs: #39d353;")
    
    # 2. Tighten viewBox:
    # - Top: starts at -16 (snake max upward reach is -16)
    # - Height: 144 (covers down to y=128, perfectly fitting snake at y=112 + 14.4px body)
    # - Width: 880 (covers all 53 weeks)
    content = re.sub(
        r'<svg\s+viewBox="[^"]+"\s+width="[^"]+"\s+height="[^"]+"',
        '<svg viewBox="-16 -16 880 144" width="880" height="144"',
        content
    )
    
    # 3. Hide the progress bar (.u) at y=144 to remove the ~45px gap
    if ".u{" in content and "display:none;" not in content:
        content = content.replace(".u{", ".u{display:none;")
    elif ".u {" in content and "display: none;" not in content:
        content = content.replace(".u {", ".u { display: none;")
        
    svg_path.write_text(content, encoding="utf-8")
    print(f"Optimized {svg_path.name}: trimmed dead space, green snake, viewBox [-16 -16 880 144]")

if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else [
        "github-contribution-grid-snake-dark.svg",
        "github-contribution-grid-snake.svg"
    ]
    for f in files:
        trim_snake(Path(f))
