#!/usr/bin/env bash
# setup.sh — 在新机器上一键建立所有 symlink
# 使用方式：git clone <repo> && cd skills && bash setup.sh
set -e

REPO="$(cd "$(dirname "$0")" && pwd)"

link_dir() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  ln -sfn "$src" "$dst"
  echo "  linked: $dst -> $src"
}

link_file() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  ln -sfn "$src" "$dst"
  echo "  linked: $dst -> $src"
}

echo ""
echo "=== Cursor ==="
for d in "$REPO/cursor/skills"/*/; do
  link_dir "$d" "$HOME/.cursor/skills/$(basename "$d")"
done
for d in "$REPO/cursor/skills-cursor"/*/; do
  link_dir "$d" "$HOME/.cursor/skills-cursor/$(basename "$d")"
done
for f in "$REPO/cursor/rules"/*.mdc; do
  link_file "$f" "$HOME/.cursor/rules/$(basename "$f")"
done

echo ""
echo "=== Codex ==="
for d in "$REPO/codex/skills"/*/; do
  link_dir "$d" "$HOME/.codex/skills/$(basename "$d")"
done

echo ""
echo "=== Kiro ==="
for d in "$REPO/kiro/skills"/*/; do
  link_dir "$d" "$HOME/.kiro/skills/$(basename "$d")"
done
# pretty-mermaid 共用 cursor 版本
link_dir "$REPO/cursor/skills/pretty-mermaid" "$HOME/.kiro/skills/pretty-mermaid"
for f in "$REPO/kiro/hooks"/*.kiro.hook; do
  link_file "$f" "$HOME/.kiro/hooks/$(basename "$f")"
done
for f in "$REPO/kiro/steering"/*.md; do
  link_file "$f" "$HOME/.kiro/steering/$(basename "$f")"
done

echo ""
echo "=== Claude ==="
# pretty-mermaid 共用 cursor 版本
link_dir "$REPO/cursor/skills/pretty-mermaid" "$HOME/.claude/skills/pretty-mermaid"

echo ""
echo "Done. 请重启 Cursor / Kiro / Claude 让 skills 生效。"
