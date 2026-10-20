import sys
import re
from pathlib import Path

def trim_snake(svg_path: Path):
    if not svg_path.exists():
        print(f"File not found: {svg_path}")
        return
    
    content = svg_path.read_text(encoding="utf-8")
    
    # 1. Vibrant neon green snake
    content = content.replace("--cs:purple;", "--cs:#39d353;")
    content = content.replace("--cs: purple;", "--cs: #39d353;")
    
    # 2. Completely delete all unneeded progress bar rects (<rect class="u...)
    content = re.sub(r'<rect class="u[^"]*"[^>]+>', '', content)
    
    # 3. Clean up unneeded .u CSS rules & keyframes
    content = re.sub(r'\.u\{[^}]*\}', '', content)
    content = re.sub(r'\.u\.[^{]+\{[^}]*\}', '', content)
    content = re.sub(r'@keyframes u\d+\{[^}]*\}', '', content)
    
    # 4. Ultra-tight viewBox:
    # Top is -16 (exact top snake reach), height 142 (exact bottom snake reach at y=112 + 14.4px body - no void)
    content = re.sub(
        r'<svg\s+viewBox="[^"]+"\s+width="[^"]+"\s+height="[^"]+"',
        '<svg viewBox="-16 -16 880 142" width="880" height="142"',
        content
    )
    
    svg_path.write_text(content, encoding="utf-8")
    print(f"Ultra-trimmed {svg_path.name}: eliminated all internal dead space")

if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else [
        "github-contribution-grid-snake-dark.svg",
        "github-contribution-grid-snake.svg"
    ]
    for f in files:
        trim_snake(Path(f))
