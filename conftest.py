"""pytest 根配置：将 src/ 加入 sys.path，使 `import scheduler_lab` 无需安装。"""
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
