#!/usr/bin/env python3
"""Go 编码规范自动审计脚本

用法:
    python3 audit.py <file1.go> [file2.go ...]
    python3 audit.py --dir <directory>

输出:
    - 通过时: 编码规范审计 ✅ (N/N)
    - 失败时: 编码规范审计 ❌ (M/N) + 逐条失败明细
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class Violation:
    file: str
    line: int
    rule: str
    detail: str


@dataclass
class AuditResult:
    name: str
    passed: bool
    violations: List[Violation] = field(default_factory=list)


# ────────────────────────────────────────────────
# 解析工具
# ────────────────────────────────────────────────

def read_lines(filepath: str) -> List[str]:
    with open(filepath, encoding="utf-8") as f:
        return f.readlines()


def is_public_func(line: str) -> bool:
    """判断是否为公开函数声明（首字母大写）"""
    stripped = line.strip()
    if not stripped.startswith("func "):
        return False
    after_func = stripped[5:]
    # 方法: func (r *Repo) GetUser(...)
    if after_func.startswith("("):
        close = after_func.find(")")
        if close == -1:
            return False
        after_receiver = after_func[close + 1:].strip()
        return len(after_receiver) > 0 and after_receiver[0].isupper()
    # 普通函数: func GetUser(...)
    return len(after_func) > 0 and after_func[0].isupper()


def is_func_start(line: str) -> bool:
    return line.strip().startswith("func ")


def count_params(sig: str) -> int:
    """统计函数签名中的参数个数"""
    start = sig.find("(")
    if start == -1:
        return 0
    # 对于方法，跳过 receiver 括号
    stripped = sig.strip()
    if stripped.startswith("func ("):
        close_recv = stripped.find(")", 6)
        if close_recv == -1:
            return 0
        start = stripped.find("(", close_recv + 1)
        if start == -1:
            return 0

    depth = 0
    params_str = ""
    for ch in sig[start:]:
        if ch == "(":
            depth += 1
            if depth == 1:
                continue
        elif ch == ")":
            depth -= 1
            if depth == 0:
                break
        if depth == 1:
            params_str += ch

    if not params_str.strip():
        return 0
    return len([p for p in params_str.split(",") if p.strip()])


# ────────────────────────────────────────────────
# 检查项
# ────────────────────────────────────────────────

def check_public_func_doc(filepath: str, lines: List[str]) -> AuditResult:
    """检查所有公开函数是否有 Go doc 注释"""
    result = AuditResult(name="公开函数注释", passed=True)
    for i, line in enumerate(lines):
        if not is_public_func(line):
            continue
        j = i - 1
        while j >= 0 and lines[j].strip() == "":
            j -= 1
        if j < 0 or not lines[j].strip().startswith("//"):
            result.passed = False
            func_name = line.strip().split("(")[0].replace("func ", "")
            result.violations.append(Violation(
                file=filepath, line=i + 1,
                rule="公开函数注释",
                detail=f"函数 {func_name} 缺少 Go doc 注释",
            ))
    return result


def check_func_length(filepath: str, lines: List[str]) -> AuditResult:
    """检查函数长度不超过 50 行"""
    result = AuditResult(name="函数长度<=50行", passed=True)
    in_func = False
    func_start = 0
    func_name = ""
    brace_depth = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if is_func_start(line) and not in_func:
            in_func = True
            func_start = i
            brace_depth = 0
            func_name = stripped.split("(")[0].replace("func ", "").strip()

        if in_func:
            brace_depth += stripped.count("{") - stripped.count("}")
            if brace_depth <= 0 and i > func_start:
                func_len = i - func_start + 1
                if func_len > 50:
                    result.passed = False
                    result.violations.append(Violation(
                        file=filepath, line=func_start + 1,
                        rule="函数长度<=50行",
                        detail=f"函数 {func_name} 共 {func_len} 行，超过 50 行限制",
                    ))
                in_func = False
    return result


def check_param_count(filepath: str, lines: List[str]) -> AuditResult:
    """检查函数参数不超过 5 个"""
    result = AuditResult(name="函数参数<=5个", passed=True)
    for i, line in enumerate(lines):
        if not is_func_start(line):
            continue
        sig = line.strip()
        # 多行签名: 拼接直到找到 ) {
        j = i
        while "{" not in sig and j < len(lines) - 1:
            j += 1
            sig += " " + lines[j].strip()
        cnt = count_params(sig)
        if cnt > 5:
            func_name = line.strip().split("(")[0].replace("func ", "").strip()
            result.passed = False
            result.violations.append(Violation(
                file=filepath, line=i + 1,
                rule="函数参数<=5个",
                detail=f"函数 {func_name} 有 {cnt} 个参数，超过 5 个限制",
            ))
    return result


def check_nesting_depth(filepath: str, lines: List[str]) -> AuditResult:
    """检查 if 嵌套不超过 2 层（忽略 Gin 中间件的外层 return func 模式）"""
    result = AuditResult(name="if嵌套<=2层", passed=True)
    in_func = False
    func_start = 0
    func_name = ""
    brace_depth = 0
    func_brace_start = 0
    if_depth = 0
    max_if_depth = 0

    # Gin 中间件模式: return func(c *gin.Context) 会多一层，需要抵消
    is_middleware = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        if is_func_start(line) and not in_func:
            in_func = True
            func_start = i
            brace_depth = 0
            if_depth = 0
            max_if_depth = 0
            func_name = stripped.split("(")[0].replace("func ", "").strip()
            is_middleware = "gin.HandlerFunc" in stripped

        if not in_func:
            continue

        # 检测 return func 模式（中间件内层闭包）
        if "return func(" in stripped and "gin.Context" in stripped:
            is_middleware = True

        open_braces = stripped.count("{")
        close_braces = stripped.count("}")

        # 在开括号前检测是否有 if/else if/for/switch
        is_control = bool(re.match(r"^(if|else if|for|switch)\b", stripped))
        if is_control:
            if_depth += 1
            max_if_depth = max(max_if_depth, if_depth)

        brace_depth += open_braces - close_braces

        if close_braces > 0:
            # 闭括号时回退 if 深度（只有 control flow 产生的）
            for _ in range(close_braces):
                if if_depth > 0:
                    if_depth -= 1

        if brace_depth <= 0 and i > func_start:
            threshold = 3 if is_middleware else 2
            if max_if_depth > threshold:
                result.passed = False
                result.violations.append(Violation(
                    file=filepath, line=func_start + 1,
                    rule="if嵌套<=2层",
                    detail=f"函数 {func_name} 最大嵌套深度 {max_if_depth}，超过 {threshold} 层限制",
                ))
            in_func = False

    return result


def check_error_handling(filepath: str, lines: List[str]) -> AuditResult:
    """检查 _ = / _ , 是否有注释说明"""
    result = AuditResult(name="错误处理", passed=True)
    for i, line in enumerate(lines):
        stripped = line.strip()
        # 忽略 import 块和注释行
        if stripped.startswith("//") or stripped.startswith("/*"):
            continue
        # 检测 _ = 或 _ , 模式（忽略 range 中的 _ 和 for _ 形式）
        if ("_ =" in stripped or "_ ," in stripped) and "range" not in stripped:
            if "//" not in stripped:
                result.passed = False
                result.violations.append(Violation(
                    file=filepath, line=i + 1,
                    rule="错误处理",
                    detail=f"忽略错误未添加注释: {stripped[:80]}",
                ))
    return result


def check_error_branch_logging(filepath: str, lines: List[str]) -> AuditResult:
    """检查错误分支是否记录日志（允许通过注释标记跳过）"""
    result = AuditResult(name="错误分支日志", passed=True)
    err_if_pattern = re.compile(r"\bif\b.*\berr\s*!=\s*nil\b.*\{")
    log_pattern = re.compile(r"\b\w+\.(Error|Warn|Info)\(")
    exit_pattern = re.compile(r"\b(return|continue|break)\b")
    skip_marker = "audit:allow-no-log"

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not err_if_pattern.search(stripped):
            continue
        if skip_marker in stripped:
            continue

        brace_depth = line.count("{") - line.count("}")
        has_log = bool(log_pattern.search(stripped))
        has_exit = bool(exit_pattern.search(stripped))
        allow_skip = False

        j = i + 1
        while j < len(lines):
            current = lines[j].strip()
            if skip_marker in current:
                allow_skip = True
            if log_pattern.search(current):
                has_log = True
            if exit_pattern.search(current):
                has_exit = True

            brace_depth += lines[j].count("{") - lines[j].count("}")
            if brace_depth <= 0:
                break
            j += 1

        if allow_skip:
            continue
        if has_exit and not has_log:
            result.passed = False
            result.violations.append(Violation(
                file=filepath,
                line=i + 1,
                rule="错误分支日志",
                detail="错误分支直接退出但未记录日志（可用 audit:allow-no-log 注释豁免高频场景）",
            ))
    return result


def check_reflect_usage(filepath: str, lines: List[str]) -> AuditResult:
    """检查是否使用了 reflect 包"""
    result = AuditResult(name="无反射使用", passed=True)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if '"reflect"' in stripped:
            result.passed = False
            result.violations.append(Violation(
                file=filepath, line=i + 1,
                rule="无反射使用",
                detail="导入了 reflect 包，请确认是否必要",
            ))
    return result


def check_context_in_blocking(filepath: str, lines: List[str]) -> AuditResult:
    """检查涉及 DB/HTTP/RPC 操作的公开函数是否接受 context.Context

    排除仅构建查询但不执行的 scope/builder 函数（返回 *gorm.DB 等）。
    """
    result = AuditResult(name="context传递", passed=True)
    # 实际执行 I/O 的调用关键词（排除链式构建如 .Where/.Model）
    exec_keywords = [
        ".Create(", ".Save(", ".Delete(", ".Find(", ".First(",
        ".Take(", ".Last(", ".Scan(", ".Exec(", ".Raw(",
        ".Count(", ".Pluck(", ".Updates(", ".Update(",
        "http.Do(", "http.Get(", "http.Post(",
        "grpc.", "redis.",
    ]
    # 返回值为 builder/scope 的函数不算阻塞
    scope_return_patterns = ["*gorm.DB", "gorm.DB"]

    for i, line in enumerate(lines):
        if not is_public_func(line):
            continue
        sig = line.strip()
        j = i
        while "{" not in sig and j < len(lines) - 1:
            j += 1
            sig += " " + lines[j].strip()

        # 已接受 context 则跳过
        if "context.Context" in sig or "ctx " in sig or "ctx," in sig:
            continue

        # 返回 *gorm.DB 的 scope 函数跳过
        if any(pat in sig for pat in scope_return_patterns):
            continue

        # 构造函数（New...）通常初始化而非执行阻塞 I/O，跳过
        func_name_match = re.search(r"func\s+(?:\([^)]+\)\s+)?(\w+)\(", sig)
        if func_name_match and func_name_match.group(1).startswith("New"):
            continue

        # Gin handler/middleware 通过 *gin.Context 间接获取 context，跳过
        if "*gin.Context" in sig or "gin.HandlerFunc" in sig:
            continue

        # 扫描函数体，查找实际执行 I/O 的调用
        brace_depth = 0
        found_blocking = False
        for k in range(i, min(i + 60, len(lines))):
            brace_depth += lines[k].count("{") - lines[k].count("}")
            for kw in exec_keywords:
                if kw in lines[k]:
                    found_blocking = True
                    break
            if found_blocking:
                break
            if brace_depth <= 0 and k > i:
                break

        if found_blocking:
            func_name = line.strip().split("(")[0].replace("func ", "").strip()
            result.passed = False
            result.violations.append(Violation(
                file=filepath, line=i + 1,
                rule="context传递",
                detail=f"函数 {func_name} 涉及阻塞操作但未接受 context.Context",
            ))
    return result


def check_interface_size(filepath: str, lines: List[str]) -> AuditResult:
    """检查接口方法数不超过 10 个"""
    result = AuditResult(name="接口最小化", passed=True)
    in_interface = False
    iface_name = ""
    iface_start = 0
    method_count = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        match = re.match(r"^type\s+(\w+)\s+interface\s*\{", stripped)
        if match:
            in_interface = True
            iface_name = match.group(1)
            iface_start = i
            method_count = 0
            continue

        if in_interface:
            if stripped == "}":
                if method_count > 10:
                    result.passed = False
                    result.violations.append(Violation(
                        file=filepath, line=iface_start + 1,
                        rule="接口最小化",
                        detail=f"接口 {iface_name} 有 {method_count} 个方法，超过 10 个",
                    ))
                in_interface = False
            elif stripped and not stripped.startswith("//"):
                method_count += 1

    return result


# ────────────────────────────────────────────────
# 主流程
# ────────────────────────────────────────────────

ALL_CHECKS = [
    check_public_func_doc,
    check_func_length,
    check_param_count,
    check_nesting_depth,
    check_error_handling,
    check_error_branch_logging,
    check_reflect_usage,
    check_context_in_blocking,
    check_interface_size,
]


def audit_file(filepath: str) -> List[AuditResult]:
    lines = read_lines(filepath)
    return [check(filepath, lines) for check in ALL_CHECKS]


def collect_files(paths: List[str]) -> List[str]:
    """从路径列表中收集 .go 文件（支持文件和目录）"""
    files = []
    for p in paths:
        path = Path(p)
        if path.is_file() and path.suffix == ".go":
            files.append(str(path))
        elif path.is_dir():
            files.extend(str(f) for f in path.rglob("*.go")
                         if "_test.go" not in f.name and "vendor" not in f.parts)
    return sorted(set(files))


def main():
    parser = argparse.ArgumentParser(description="Go 编码规范审计")
    parser.add_argument("targets", nargs="*", help="Go 文件或目录路径")
    parser.add_argument("--dir", help="扫描整个目录")
    parser.add_argument("--verbose", "-v", action="store_true", help="输出详细违规信息")
    args = parser.parse_args()

    targets = args.targets or []
    if args.dir:
        targets.append(args.dir)

    if not targets:
        print("用法: audit.py <file1.go> [file2.go ...] 或 --dir <directory>", file=sys.stderr)
        sys.exit(1)

    files = collect_files(targets)
    if not files:
        print("未找到 .go 文件", file=sys.stderr)
        sys.exit(1)

    # 按检查项名汇总: 任何文件不通过则该项不通过
    summary: dict[str, bool] = {}
    all_violations: List[Violation] = []

    for filepath in files:
        for result in audit_file(filepath):
            prev = summary.get(result.name, True)
            summary[result.name] = prev and result.passed
            all_violations.extend(result.violations)

    total = len(ALL_CHECKS)
    passed = sum(1 for v in summary.values() if v)

    if passed == total:
        print(f"编码规范审计 ✅ ({passed}/{total})")
    else:
        print(f"编码规范审计 ❌ ({passed}/{total})")
        for v in all_violations:
            print(f"  ❌ {v.file}:{v.line} [{v.rule}] {v.detail}")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
