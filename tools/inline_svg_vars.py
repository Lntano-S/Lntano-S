#!/usr/bin/env python3
"""把 SVG 里的 CSS 变量写死成色值。

snk 生成的蛇把颜色表达成 CSS 变量（fill:var(--ce)）。遇到不认变量的渲染器
（部分浏览器、图片预览器、某些客户端）变量不生效，fill 会退回黑色，整张图就是黑的。
把 var(--xx) 替换成对应色值，之后谁渲染都一样。

用法：
    python3 tools/inline_svg_vars.py dist out    # 从 dist 读，写进 out（推荐）
    python3 tools/inline_svg_vars.py dist        # 就地改写

为什么要能换目录：snk 是 Docker action，容器里以 root 写出 dist/*.svg，
runner 用户没权限覆盖它们，换个目录写就不用 sudo 了。
"""

import pathlib
import re
import sys


def inline(text: str) -> str:
    for key, value in re.findall(r"--([a-zA-Z0-9]+)\s*:\s*([^;}]+)", text):
        text = text.replace(f"var(--{key})", value.strip())
    return text


def main(args) -> int:
    src = pathlib.Path(args[0])
    dest = pathlib.Path(args[1]) if len(args) > 1 else src
    if dest != src:
        dest.mkdir(parents=True, exist_ok=True)

    count = 0
    for path in sorted(src.glob("*.svg")):
        out = dest / path.name
        out.write_text(inline(path.read_text(encoding="utf-8")), encoding="utf-8")
        print(f"inlined -> {out}")
        count += 1
    print(f"done, {count} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["dist"]))
