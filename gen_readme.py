import os
import glob
import urllib.parse

repo = os.environ.get("GITHUB_REPOSITORY", "OWNER/REPO")
server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")

pdfs = sorted(glob.glob("books/*.pdf"))

lines = [
    "# 📚 책 뷰어",
    "",
    "Google Drive에 올린 PDF가 자동으로 여기에 동기화됩니다.",
    "아래 제목을 클릭하면 로그인 없이 브라우저에서 바로 열립니다.",
    "",
]

if not pdfs:
    lines.append("_아직 동기화된 책이 없습니다._")
else:
    for p in pdfs:
        name = os.path.basename(p)
        title = os.path.splitext(name)[0]
        url = f"{server}/{repo}/blob/main/{urllib.parse.quote(p)}"
        lines.append(f"- [{title}]({url})")

lines.append("")

with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
