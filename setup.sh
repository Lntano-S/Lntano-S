#!/usr/bin/env bash
# 照搬 living-scene 模板：拉横幅 + 小院页脚，把名字和坐标改成你的。
# 用法：bash setup.sh
# 先试 api.github.com（多数网络能通），不行再走本地代理常见端口。
set -u

cd "$(dirname "$0")"
NAME=Lntano-S
LAT=30.49
LON=114.39
TZ=Asia/Shanghai

MODES=("" "http://127.0.0.1:10808" "http://127.0.0.1:10809" "socks5h://127.0.0.1:10808" "socks5h://127.0.0.1:1080" "http://127.0.0.1:7890")

get() { # $1 仓库内路径  $2 落盘文件名
  local path="$1" out="$2" m
  for m in "${MODES[@]}"; do
    for u in \
      "https://api.github.com/repos/yuki4266/living-scene-template/contents/$path" \
      "https://raw.githubusercontent.com/yuki4266/living-scene-template/HEAD/$path"
    do
      local -a cmd=(curl -fsSL --max-time 30)
      [ -n "$m" ] && cmd+=(-x "$m")
      [ "${u#*api.github}" != "$u" ] && cmd+=(-H "Accept: application/vnd.github.raw")
      if env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u all_proxy \
          "${cmd[@]}" -o "$out" "$u" && [ -s "$out" ]; then
        echo "  拉到 $out  ($(stat -c%s "$out") 字节)"
        return 0
      fi
    done
  done
  echo "  !! $out 没拉到"
  return 1
}

mkdir -p .github/workflows
for f in header.svg header-night.svg garden-footer.svg garden-footer-night.svg; do
  get "$f" "$f"
done
get ".github/workflows/scene.yml" ".github/workflows/scene.yml"
get ".github/scene-state" ".github/scene-state"

# 名字：模板里叫 yourname，在 <text> 和 <title> 各一处
for f in header.svg header-night.svg; do
  if [ -f "$f" ]; then
    sed -i "s/yourname/$NAME/g" "$f"
    echo "$f 里 $NAME 出现 $(grep -c "$NAME" "$f") 处"
  fi
done

# 坐标：武汉
if [ -f .github/workflows/scene.yml ]; then
  sed -i -E "s|^([[:space:]]*lat:[[:space:]]*).*|\1\"$LAT\"|; s|^([[:space:]]*lon:[[:space:]]*).*|\1\"$LON\"|; s|^([[:space:]]*tz:[[:space:]]*).*|\1$TZ|" .github/workflows/scene.yml
  grep -E "lat:|lon:|tz:" .github/workflows/scene.yml
fi

echo
echo "剩下的："
echo "  git add -A && git commit -m '照搬 living-scene 主页' && git push"
