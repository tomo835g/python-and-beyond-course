"""contents.py の目次から、各教材のページ（<folder>/README.md）と、
トップの README.md の教材の表を作る。書いたノートブックには Colab で開くボタンを付け、
まだのものは「準備中」と書く。"""
import re
from pathlib import Path

from contents import BOOKS

ROOT = Path(__file__).resolve().parent.parent
REPO = "tomo835g/python-and-beyond-course"
BADGE = "https://colab.research.google.com/assets/colab-badge.svg"
BEGIN, END = "<!-- 教材の表ここから（tools/make_pages.py が作る） -->", "<!-- 教材の表ここまで -->"


def find_notebook(folder, part_dir, n):
    d = ROOT / folder / part_dir
    hits = sorted(d.glob(f"{n:02d}_*.ipynb")) if d.is_dir() else []
    return hits[0].relative_to(ROOT).as_posix() if hits else None



def book_page(book):
    out = [f"# 教材{book['no']}「{book['name']}」", "",
           book["summary"] + "。", "",
           f"前提：{book['prereq']}", "",
           "表の「Colab で開く」を押すと、そのまま Colab で開けます。"
           "開いたら、最初に自分のドライブにコピーを保存してください（やり方は教材1 第1部 第1回）。", "",
           "分からないところは AI に聞いてみよう（やり方は教材1 第1部 第2回「分からないときは AI に聞く」）。", ""]
    done = total = 0
    for part in book["parts"]:
        if part["title"]:
            out += [f"## {part['title']}", ""]
        if part.get("note"):
            out += [part["note"], ""]
        out += ["| 回 | 内容 | ノートブック |", "|---|---|---|"]
        for k, title in enumerate(part["items"]):
            n = part.get("start", 1) + k
            total += 1
            nb = find_notebook(book["folder"], part["dir"], n)
            if nb:
                done += 1
                link = f"[![Colab で開く]({BADGE})](https://colab.research.google.com/github/{REPO}/blob/main/{nb})"
                out.append(f"| 第{n}回 | {title} | {link} |")
            else:
                out.append(f"| 第{n}回 | {title} | 準備中 |")
        out.append("")
    out += ["---", "", "[トップページへ戻る](../README.md)", ""]
    return "\n".join(out), done, total


def main():
    rows = ["| 教材 | 内容 | 前提 | できている回 |", "|---|---|---|---|"]
    for book in BOOKS:
        text, done, total = book_page(book)
        page = ROOT / book["folder"] / "README.md"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(text, encoding="utf-8")
        rows.append(f"| [教材{book['no']}「{book['name']}」]({book['folder']}/README.md) "
                    f"| {book['summary']} | {book['prereq']} | {done} / {total} |")
    top = ROOT / "README.md"
    t = top.read_text(encoding="utf-8")
    table = BEGIN + "\n\n" + "\n".join(rows) + "\n\n" + END
    t = re.sub(re.escape(BEGIN) + ".*?" + re.escape(END), lambda m: table, t, flags=re.S)
    top.write_text(t, encoding="utf-8")


if __name__ == "__main__":
    main()
