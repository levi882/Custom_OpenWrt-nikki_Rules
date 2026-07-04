#!/usr/bin/env python3
"""
将 MkDocs 文档转换为 GitHub Wiki 格式。

转换内容：
  - !!! tip/note/warning  →  > [!TIP]/[!NOTE]/[!WARNING]
  - GitHub Pages 绝对链接  →  wiki 相对链接
  - 从 mkdocs.yml 自动生成 _Sidebar.md
  - 从 mkdocs.yml 自动生成 _Footer.md

用法：
  python convert_to_wiki.py [项目根目录] [wiki输出目录]
"""

import re
import sys
import shutil
from pathlib import Path

import yaml

# MkDocs admonition 类型 → GitHub Wiki blockquote 类型
ADMONITION_MAP = {
    "tip": "TIP",
    "note": "NOTE",
    "warning": "WARNING",
    "danger": "DANGER",
    "caution": "CAUTION",
    "important": "IMPORTANT",
    "info": "INFO",
    "example": "EXAMPLE",
    "quote": "QUOTE",
    "abstract": "ABSTRACT",
    "summary": "ABSTRACT",
    "success": "SUCCESS",
    "failure": "FAILURE",
    "bug": "BUG",
    "question": "QUESTION",
}


def convert_admonitions(content: str) -> str:
    """
    转换 MkDocs !!! admonition → GitHub Wiki > [!TYPE] 格式。

    支持多段落（中间有空行的缩进内容）。
    """
    lines = content.split("\n")
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # 匹配: !!! type 或 !!! type "标题"
        m = re.match(r'^!!!\s+(\w+)(?:\s+"([^"]*)")?\s*$', line)
        if m:
            admon_type = m.group(1).lower()
            title = m.group(2)
            gh_type = ADMONITION_MAP.get(admon_type, admon_type.upper())

            if title:
                result.append(f"> [!{gh_type}] {title}")
            else:
                result.append(f"> [!{gh_type}]")

            i += 1
            # 收集缩进内容
            while i < len(lines):
                cl = lines[i]
                if cl == "":
                    # 完全空行（无缩进）→ 结束当前 admonition
                    break
                if cl.isspace():
                    # 仅缩进空格 → admonition 中的空行
                    result.append("> ")
                    i += 1
                elif cl.startswith("    "):
                    # 缩进内容 → 去掉前 4 个空格，加上 >  前缀
                    result.append(f"> {cl[4:]}")
                    i += 1
                else:
                    # 非缩进非空行 → 结束当前 admonition
                    break
        else:
            result.append(line)
            i += 1

    return "\n".join(result)


def convert_links(content: str) -> str:
    """将 GitHub Pages 绝对链接转换为 wiki 相对链接。"""
    # https://levi882.github.io/Custom_OpenWrt-nikki_Rules/XXX/ → ./XXX
    content = re.sub(
        r"https?://levi882\.github\.io/Custom_OpenWrt-nikki_Rules/([^\s<>\"\')\]\)]+)",
        lambda m: "./" + m.group(1).rstrip("/"),
        content,
    )
    return content


def build_sidebar(nav: list) -> str:
    """从 mkdocs.yml 的 nav 配置生成 _Sidebar.md 内容。"""
    def wiki_name(filename: str) -> str:
        """index.md → Home, 其他去掉 .md 后缀"""
        name = filename.replace(".md", "")
        return "Home" if name == "index" else name

    lines = []
    for item in nav:
        if isinstance(item, dict):
            for section, subitems in item.items():
                lines.append(f"## {section}")
                if isinstance(subitems, str):
                    # 单页面: 首页: index.md
                    lines.append(f"- [{section}](./{wiki_name(subitems)})")
                elif isinstance(subitems, list):
                    # 子页面列表
                    for sub in subitems:
                        if isinstance(sub, dict):
                            for title, file in sub.items():
                                lines.append(f"- [{title}](./{wiki_name(file)})")
                        elif isinstance(sub, str):
                            lines.append(f"- [{sub}](./{wiki_name(sub)})")
                lines.append("")  # 段落间空行
    return "\n".join(lines)


def main():
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    doc_dir = repo_root / "doc"
    wiki_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else repo_root / "wiki"

    if not doc_dir.exists():
        print(f"Error: doc dir not found: {doc_dir}")
        sys.exit(1)

    # 清理并重建输出目录
    if wiki_dir.exists():
        shutil.rmtree(wiki_dir)
    wiki_dir.mkdir()

    # 读取 mkdocs.yml
    mkdocs_yml = repo_root / "mkdocs.yml"
    if not mkdocs_yml.exists():
        print(f"Error: mkdocs.yml not found: {mkdocs_yml}")
        sys.exit(1)

    with open(mkdocs_yml, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # ---- _Sidebar.md ----
    nav = cfg.get("nav", [])
    sidebar = build_sidebar(nav)
    (wiki_dir / "_Sidebar.md").write_text(sidebar + "\n", encoding="utf-8")
    print("[OK] _Sidebar.md")

    # ---- _Footer.md ----
    site_url = cfg.get("site_url", "")
    if site_url:
        footer = f"---\n\n:pencil: 基于 [{cfg.get('site_name', 'MkDocs')}]({site_url}) 生成"
        (wiki_dir / "_Footer.md").write_text(footer + "\n", encoding="utf-8")
        print("[OK] _Footer.md")

    # ---- 转换 Markdown 文件 ----
    # index.md → Home.md (GitHub Wiki 默认首页)
    RENAME_MAP = {"index.md": "Home.md"}

    md_files = sorted(doc_dir.glob("*.md"))
    if not md_files:
        print("Warning: no .md files found")
        return

    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        content = convert_admonitions(content)
        content = convert_links(content)

        # 确定输出文件名
        out_name = RENAME_MAP.get(md_file.name, md_file.name)
        out = wiki_dir / out_name
        out.write_text(content, encoding="utf-8")
        if out_name != md_file.name:
            print(f"[OK] {md_file.name} -> {out_name}")
        else:
            print(f"[OK] {md_file.name}")

    print(f"\nDone! {len(md_files)} files -> {wiki_dir}")


if __name__ == "__main__":
    main()
