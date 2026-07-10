import os
import glob
import html
import urllib.parse
from datetime import datetime, timezone, timedelta

repo = os.environ.get("GITHUB_REPOSITORY", "OWNER/REPO")
server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
owner = repo.split("/")[0]
name_only = repo.split("/")[-1]
pages_url = f"https://{owner.lower()}.github.io/{name_only}/"

pdfs = sorted(glob.glob("books/*.pdf"))


def human_size(n):
    mb = n / (1024 * 1024)
    if mb >= 1:
        return f"{mb:.1f} MB"
    return f"{n / 1024:.0f} KB"


books = []
for p in pdfs:
    base = os.path.basename(p)
    books.append({
        "title": os.path.splitext(base)[0],
        "href": urllib.parse.quote(p),
        "size": human_size(os.path.getsize(p)),
    })

kst = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=9)))
updated = kst.strftime("%Y-%m-%d %H:%M KST")

# ---------- README.md ----------
md = [
    "# 📚 책장",
    "",
    f"**웹 목차 → {pages_url}**",
    "",
    "Google Drive에 올린 PDF가 자동으로 여기에 동기화됩니다. 아래 제목을 클릭하면 로그인 없이 브라우저에서 바로 열립니다.",
    "",
]
if not books:
    md.append("_아직 동기화된 책이 없습니다._")
else:
    for b in books:
        md.append(f"- [{b['title']}]({server}/{repo}/blob/main/{b['href']})")
md.append("")
with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md))

# ---------- index.html (GitHub Pages) ----------
SPINES = ["#c0472b", "#3d6b5a", "#b5852a", "#4a5a8c", "#8a4a6b", "#5a6b3d", "#2f6d78", "#a35a2a"]

if books:
    cards = []
    for i, b in enumerate(books):
        spine = SPINES[i % len(SPINES)]
        t = html.escape(b["title"])
        initial = html.escape(b["title"].strip()[:1]) or "•"
        viewer_href = f"viewer.html?f={b['href']}&t={urllib.parse.quote(b['title'])}"
        cards.append(
            f'''      <a class="card" href="{viewer_href}">
        <span class="spine" style="background:{spine}"><span class="initial">{initial}</span></span>
        <span class="body">
          <span class="idx">{i + 1:02d}</span>
          <span class="title">{t}</span>
          <span class="meta">PDF · {b['size']}</span>
        </span>
      </a>'''
        )
    grid = '<div class="grid">\n' + "\n".join(cards) + "\n    </div>"
else:
    grid = '<p class="empty">아직 동기화된 책이 없습니다. Google Drive 폴더에 PDF를 올려 주세요.</p>'

count = len(books)

HEAD = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>책장</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@700&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#f5f2ec; --card:#fffdf9; --ink:#211e19; --muted:#8c8577;
    --line:#e8e2d6; --accent:#c0472b;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{
    font-family:"Pretendard",system-ui,sans-serif;
    background:
      radial-gradient(120% 80% at 100% 0%, #efe9dd 0%, transparent 55%),
      var(--bg);
    color:var(--ink); line-height:1.5;
    -webkit-font-smoothing:antialiased;
    min-height:100vh;
  }
  .wrap{max-width:960px;margin:0 auto;padding:clamp(2.5rem,6vw,5rem) clamp(1.2rem,4vw,2rem) 4rem}
  header{margin-bottom:clamp(2rem,5vw,3.2rem)}
  .kicker{
    font-size:.78rem;letter-spacing:.22em;text-transform:uppercase;
    color:var(--accent);font-weight:700;margin-bottom:.9rem;
  }
  h1{
    font-family:"Gowun Batang",serif;font-weight:700;
    font-size:clamp(2.4rem,7vw,3.6rem);line-height:1.04;letter-spacing:-.01em;
  }
  .sub{margin-top:1rem;color:var(--muted);max-width:34rem;font-size:1rem}
  .count{
    display:inline-flex;align-items:center;gap:.5rem;margin-top:1.4rem;
    font-size:.82rem;color:var(--muted);
    border:1px solid var(--line);border-radius:999px;padding:.4rem .9rem;background:var(--card);
  }
  .dot{width:7px;height:7px;border-radius:50%;background:#3d9b6b;box-shadow:0 0 0 3px rgba(61,155,107,.15)}
  .grid{
    display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
    gap:1rem;
  }
  .card{
    display:flex;text-decoration:none;color:inherit;
    background:var(--card);border:1px solid var(--line);border-radius:14px;
    overflow:hidden;transition:transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    box-shadow:0 1px 2px rgba(40,30,20,.03);
  }
  .card:hover{
    transform:translateY(-4px);
    box-shadow:0 14px 30px -12px rgba(40,30,20,.28);
    border-color:#d9d1c2;
  }
  .spine{
    flex:0 0 58px;display:flex;align-items:center;justify-content:center;position:relative;
  }
  .spine:after{content:"";position:absolute;right:0;top:12%;bottom:12%;width:1px;background:rgba(255,255,255,.35)}
  .initial{
    font-family:"Gowun Batang",serif;color:#fff;font-size:1.5rem;font-weight:700;
    text-shadow:0 1px 2px rgba(0,0,0,.2);
  }
  .body{padding:1.05rem 1.15rem;display:flex;flex-direction:column;min-width:0;flex:1}
  .idx{font-size:.72rem;color:var(--muted);letter-spacing:.15em;font-variant-numeric:tabular-nums}
  .title{
    font-family:"Gowun Batang",serif;font-weight:700;font-size:1.08rem;margin:.35rem 0 .55rem;
    line-height:1.28;color:var(--ink);
    display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
  }
  .meta{margin-top:auto;font-size:.78rem;color:var(--muted);letter-spacing:.02em}
  .empty{color:var(--muted);padding:2rem 0}
  footer{margin-top:3rem;padding-top:1.6rem;border-top:1px solid var(--line);
    font-size:.82rem;color:var(--muted);display:flex;flex-wrap:wrap;gap:.4rem 1.2rem}
  footer a{color:var(--accent);text-decoration:none}
  footer a:hover{text-decoration:underline}
</style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="kicker">Library</div>
      <h1>책장</h1>
      <p class="sub">Google Drive에 올린 책이 자동으로 여기에 모입니다. 제목을 누르면 로그인 없이 바로 열립니다.</p>
      <div class="count"><span class="dot"></span>__COUNT__권 · 자동 동기화</div>
    </header>
    __GRID__
    <footer>
      <span>마지막 갱신 __UPDATED__</span>
      <span>Google Drive 폴더에 올리면 30분 내 자동 반영</span>
    </footer>
  </div>
</body>
</html>
"""

page = (HEAD
        .replace("__COUNT__", str(count))
        .replace("__GRID__", grid)
        .replace("__UPDATED__", updated))

with open("index.html", "w", encoding="utf-8") as f:
    f.write(page)
