#!/bin/bash
# 将全局 hooks 同步到指定项目的 .kiro/hooks/ 目录
# 用法: bash sync-hooks.sh /path/to/project1 /path/to/project2 ...

SOURCE_DIR="$HOME/.kiro/hooks"

if [ $# -eq 0 ]; then
  echo "用法: bash $0 <项目路径1> [项目路径2] ..."
  echo "示例: bash $0 ~/project/app1 ~/project/app2"
  exit 1
fi

for PROJECT in "$@"; do
  TARGET="$PROJECT/.kiro/hooks"
  mkdir -p "$TARGET"
  cp "$SOURCE_DIR"/*.kiro.hook "$TARGET/" 2>/dev/null
  echo "已同步到: $TARGET"
done
