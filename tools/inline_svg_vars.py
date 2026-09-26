#!/usr/bin/env python3
"""把 SVG 里的 CSS 变量写死成色值。

snk 生成的蛇把颜色表达成 CSS 变量（fill:var(--ce)）。遇到不认变量的渲染器
（部分浏览器、图片预览器、某些客户端）变量不生效，fill 会退回黑色，整张图就是黑的。
这个脚本把 var(--xx) 全部替换成它对应的色值，之后谁渲染都一样。

用法：
    python3 tools/inline_svg_vars.py dist
"""

import pathlib
import re
import sys

# 只输出 ASCII，避免某些环境 stdout 编码不是 UTF-8 时 print 直接报错退出
def main(paths):
    changed = 0
    for folder in paths:
        for path in sorted(pathlib.Path(folder).glob("*.svg")):
            text = path.read_text(encoding="utf-8")
            colors = re.findall(r"--([a-zA-Z0-9]+)\s*:\s*([^;}]+)", text)
            for key, value in colors:
                text = text.replace(f"var(--{key})", value.strip())
            path.write_text(text, encoding="utf-8")
            print(f"inlined {len(colors)} vars -> {path.name}")
            changed += 1
    print(f"done, {changed} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["dist"]))
