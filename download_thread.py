import requests
import os
from datetime import datetime
from urllib.parse import urlparse

default_url = "https://2ch.org"
# board = "b"
# thread = "337358784"

board = input("Enter board name: ")
thread = input("ID thread: ")

thread_dir = f"threads/{thread}"
src_dir = os.path.join(thread_dir, "src")
thumb_dir = os.path.join(thread_dir, "thumb")


def download_file(url: str, dest_path: str) -> bool:
    print(f"Downloading file {url}...")
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        return True
    try:
        resp = requests.get(url, stream=True, timeout=30)
        resp.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)
        return False



header_html = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>/b/ — Бред — Тред №337358784</title>
  <style>
    :root {
      --bg: #f0e0d6;
      --post-bg: #f0e0d6;
      --op-bg: #ffe6c7;
      --border: #d9bfb7;
      --header-bg: #ffe6a8;
      --link: #0000ee;
      --link-hover: #d00;
      --text: #262626;
      --name: #117743;
      --reply: #dd0000;
      --muted: #7f6b63;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Verdana, Geneva, "Segoe UI", sans-serif;
      font-size: 13px;
      line-height: 1.4;
    }

    a {
      color: var(--link);
      text-decoration: none;
    }

    a:hover {
      color: var(--link-hover);
      text-decoration: underline;
    }

    /* ---------- Header ---------- */

    .board-header {
      background: var(--header-bg);
      border-bottom: 2px solid var(--border);
      padding: 10px 16px;
      display: flex;
      align-items: baseline;
      gap: 12px;
      flex-wrap: wrap;
    }

    .board-header h1 {
      margin: 0;
      font-size: 24px;
      font-weight: 700;
      color: #800000;
      letter-spacing: 1px;
    }

    .board-header .board-title {
      color: var(--muted);
      font-size: 13px;
    }

    .board-nav {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      padding: 6px 16px;
      background: #f7d9b8;
      border-bottom: 1px solid var(--border);
    }

    .board-nav a {
      font-size: 12px;
      padding: 2px 6px;
      border: 1px solid transparent;
    }

    .board-nav a:hover {
      border-color: var(--border);
      background: #fff3e0;
      text-decoration: none;
    }

    /* ---------- Thread ---------- */

    .thread {
      max-width: 900px;
      margin: 12px auto;
      padding: 0 10px;
    }

    .thread-info {
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 8px;
    }

    .post {
      background: var(--op-bg);
      border: 1px solid var(--border);
      border-radius: 2px;
      padding: 8px 10px;
      margin-bottom: 6px;
      overflow: hidden;
    }

    .post.op {
      margin-bottom: 14px;
    }

    .post.oppost {
      background: var(--post-bg);
    }

    .post.closed {
      opacity: 0.7;
    }

    .post.highlight {
      outline: 2px solid #e6b800;
    }

    /* ---------- Post header ---------- */

    .post-header {
      display: flex;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 4px;
    }

    .post-name {
      color: var(--name);
      font-weight: 700;
    }

    .post-trip {
      color: #228854;
      font-weight: 400;
      font-size: 12px;
    }

    .post-subject {
      color: #cc1105;
      font-weight: 700;
    }

    .post-date {
      color: var(--muted);
      font-size: 12px;
    }

    .post-num {
      color: #800000;
      font-size: 12px;
    }

    .post-num a {
      color: #800000;
    }

    .post-num a:hover {
      color: var(--link-hover);
    }

    .post-reply-link {
      color: var(--reply);
      font-size: 12px;
    }

    .badge {
      display: inline-block;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      padding: 1px 5px;
      border-radius: 2px;
      vertical-align: middle;
    }

    .badge.op-badge {
      background: #c00;
      color: #fff;
    }

    .badge.sticky {
      background: #e6b800;
      color: #000;
    }

    .badge.closed {
      background: #555;
      color: #fff;
    }

    /* ---------- File block ---------- */

    .post-file {
      margin: 4px 0;
    }

    .post-file .file-info {
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 4px;
    }

    .post-file .file-info a {
      color: #34345c;
    }

    .post-file .file-info .file-name {
      color: #34345c;
      font-weight: 400;
    }

    .post-file .file-info .file-stats {
      color: var(--muted);
    }

    .post-file .thumbnail {
      display: block;
      border: 1px solid var(--border);
      background: #fff;
    }

    .post-file.op-file {
      float: left;
      margin: 4px 12px 4px 0;
    }

    /* ---------- Comment ---------- */

    .post-comment {
      margin-top: 4px;
      overflow-wrap: break-word;
      word-wrap: break-word;
      overflow: hidden;
    }

    .post-comment .quote {
      color: var(--reply);
    }

    .post-comment .spoiler {
      background: #000;
      color: #000;
    }

    .post-comment .spoiler:hover {
      color: #fff;
    }

    .post-comment br {
      line-height: 1.5;
    }

    .post-comment code {
      font-family: Consolas, monospace;
      background: #e8d4c4;
      padding: 0 2px;
    }

    /* ---------- Hover preview ---------- */

    .post-preview {
      position: absolute;
      z-index: 1000;
      display: none;
      max-width: 360px;
      padding: 8px 10px;
      background: #fff8ee;
      border: 1px solid var(--border);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
      font-size: 12px;
      color: var(--text);
    }

    .post-preview.visible {
      display: block;
    }

    .post-preview .preview-header {
      margin-bottom: 4px;
    }

    .post-preview .preview-body {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .post-preview .preview-thumb {
      flex: 0 0 auto;
    }

    .post-preview .preview-thumb img {
      display: block;
      max-width: 160px;
      max-height: 160px;
      border: 1px solid var(--border);
      background: #fff;
    }

    .post-preview .preview-file {
      width: 100%;
      color: var(--muted);
      margin-bottom: 4px;
    }

    .post-preview .preview-comment {
      flex: 1 1 140px;
      min-width: 120px;
      max-height: 170px;
      overflow: hidden;
      overflow-wrap: break-word;
      word-wrap: break-word;
    }

    .post-preview .preview-comment .quote {
      color: var(--reply);
    }

    .post-preview .preview-comment .spoiler {
      background: #000;
      color: #000;
    }

    .post-preview .preview-comment .spoiler:hover {
      color: #fff;
    }
  </style>
</head>"""


body_header_html = """
<body>
 <header class="board-header">
    <h1>/b/</h1>
    <span class="board-title">Бред</span>
  </header>
"""


info_thread = requests.get(default_url + f"/api/mobile/v2/info/{board}/{thread}")

# b'{"result":1,"thread":{"num":337358784,"posts":120,"timestamp":1791819784}}'
if info_thread.status_code == 200:
    print("Thread is exists")
    print(info_thread.content)

info_thr_json = info_thread.json()
info_thr_timestamps = datetime.fromtimestamp(
    info_thr_json["thread"]["timestamp"]
).strftime("%d/%m/%Y %H:%M:%S")

body_main_html = f"""
<main class="thread">
<div class="thread-info">
      Тред №{thread} &middot; {info_thr_json["thread"]["posts"]} постов &middot;  создан {info_thr_timestamps}
    </div>

"""
end_html = """
</main>
</body>
<script>
    (function () {
      var preview = document.createElement("div");
      preview.className = "post-preview";
      preview.setAttribute("aria-hidden", "true");
      document.body.appendChild(preview);

      var currentTarget = null;

      function buildPreview(post) {
        var name = post.querySelector(".post-name");
        var trip = post.querySelector(".post-trip");
        var date = post.querySelector(".post-date");
        var num = post.querySelector(".post-num");
        var fileInfo = post.querySelector(".post-file .file-info");
        var thumb = post.querySelector(".post-file .thumbnail");
        var comment = post.querySelector(".post-comment");

        var html = '<div class="preview-header">';
        html += '<span class="post-name">' + (name ? name.textContent : "Аноним") + "</span> ";
        if (trip) html += '<span class="post-trip">' + trip.textContent + "</span> ";
        if (date) html += '<span class="post-date">' + date.textContent + "</span> ";
        if (num) html += '<span class="post-num">' + num.textContent.trim() + "</span>";
        html += "</div>";

        html += '<div class="preview-body">';
        if (fileInfo) {
          html += '<div class="preview-file">' + fileInfo.innerHTML + "</div>";
        }
        if (thumb) {
          html +=
            '<a class="preview-thumb" href="#">' +
            '<img src="' + thumb.getAttribute("src") + '" alt="' + (thumb.getAttribute("alt") || "") + '">' +
            "</a>";
        }
        if (comment) {
          html += '<div class="preview-comment">' + comment.innerHTML + "</div>";
        }
        html += "</div>";

        preview.innerHTML = html;
      }

      function position(link) {
        var rect = link.getBoundingClientRect();
        var scrollX = window.pageXOffset;
        var scrollY = window.pageYOffset;
        var top = rect.bottom + scrollY + 6;
        var left = rect.left + scrollX;

        var pw = preview.offsetWidth;
        var viewport = document.documentElement.clientWidth;
        var maxLeft = scrollX + viewport - pw - 8;
        if (left > maxLeft) left = maxLeft;
        if (left < scrollX + 8) left = scrollX + 8;

        preview.style.top = top + "px";
        preview.style.left = left + "px";
      }

      function show(link) {
        var href = link.getAttribute("href") || "";
        if (href.charAt(0) !== "#") return;
        var post = document.getElementById(href.slice(1));
        if (!post) return;

        buildPreview(post);
        preview.classList.add("visible");
        post.classList.add("highlight");
        currentTarget = post;
        position(link);
      }

      function hide() {
        preview.classList.remove("visible");
        if (currentTarget) currentTarget.classList.remove("highlight");
        currentTarget = null;
      }

      document.addEventListener("mouseover", function (e) {
        var link = e.target.closest && e.target.closest(".post-num a");
        if (link) show(link);
      });

      document.addEventListener("mouseout", function (e) {
        var link = e.target.closest && e.target.closest(".post-num a");
        if (link) hide();
      });

      window.addEventListener("scroll", hide);
    })();
  </script>
</html>
"""


# {
#       "banned": 0,
#       "board": "b",
#       "closed": 0,
#       "comment": "\u003Ca href=\"/b/res/337358784.html#337358784\" class=\"post-reply-link\" data-thread=\"337358784\" data-num=\"337358784\"\u003E\u003E\u003E337358784 (OP)\u003C/a\u003E\u003Cbr\u003Eвид мени справка по шизе не могу",
#       "date": "12/10/26 Пнд 18:44:37",
#       "email": "",
#       "endless": 0,
#       "files": null,
#       "lasthit": 1791828757,
#       "name": "Аноним",
#       "num": 337358822,
#       "op": 0,
#       "parent": 337358784,
#       "sticky": 0,
#       "subject": "",
#       "timestamp": 1791819877,
#       "trip": "",
#       "views": 0
#     },

#   {
#       "banned": 0,
#       "board": "b",
#       "closed": 0,
#       "comment": "\u003Ca href=\"/b/res/337358784.html#337358918\" class=\"post-reply-link\" data-thread=\"337358784\" data-num=\"337358918\"\u003E\u003E\u003E337358918\u003C/a\u003E",
#       "date": "12/10/26 Пнд 18:51:11",
#       "email": "",
#       "endless": 0,
#       "files": [
#         {
#           "displayname": "image.png",
#           "fullname": "image.png",
#           "height": 480,
#           "md5": "d8b2e699c778350755308019a5d82199",
#           "name": "17918202712620863779.png",
#           "path": "/b/src/337358784/17918202712620863779.png",
#           "size": 583,
#           "thumbnail": "/b/thumb/337358784/17918202712620863779s.jpg",
#           "tn_height": 150,
#           "tn_width": 200,
#           "type": 2,
#           "width": 640
#         }
#       ],
#       "lasthit": 1791828757,
#       "name": "Аноним",
#       "num": 337358970,
#       "op": 0,
#       "parent": 337358784,
#       "sticky": 0,
#       "subject": "",
#       "timestamp": 1791820271,
#       "trip": "",
#       "views": 0
#     },
posts_from_thread = requests.get(
    default_url + f"/api/mobile/v2/after/{board}/{thread}/{thread}"
)

posts = posts_from_thread.json()["posts"]


def generate_post(
    op,
    num,
    name,
    date,
    comment,
    files: list | None,
) -> str:
    badges = ""
    if op:
        badges += '\n            <span class="badge op-badge">OP</span>'
    if comment:
        comment = comment.replace(f"/b/res/{thread}.html", "")

    header_post_html = f"""
    <article class="post{' op' if op else ''}" id="{num}">
        <div class="post-header">
            <span class="post-name">{name}</span>
            <span class="post-date">{date}</span>
            <span class="post-num"><a href="#{num}">№{num}</a></span>{badges}
        </div>
"""

    body_post_html = ""
    if type(files) is list and len(files) > 0:
        for file in files:
            file_name = file["name"]
            thumb_name = os.path.basename(urlparse(file["thumbnail"]).path)

            src_rel = os.path.join(src_dir, file_name).replace("\\", "/")
            thumb_rel = os.path.join(thumb_dir, thumb_name).replace("\\", "/")

            src_ok = download_file(default_url + file["path"], os.path.join(src_dir, file_name))
            thumb_ok = download_file(default_url + file["thumbnail"], os.path.join(thumb_dir, thumb_name))

            displayname = file.get("displayname") or file_name
            src_href = src_rel if src_ok else default_url + file["path"]
            thumb_src = thumb_rel if thumb_ok else default_url + file["thumbnail"]

            body_post_html += f"""
      <div class="post-file{' op-file' if op else ''}">
        <div class="file-info">
          Файл:
          <a href="{src_href}" target="_blank">{displayname}</a>
          <span class="file-stats">({file['size']} КБ, {file['width']}x{file['height']})</span>
        </div>
        <a href="{src_href}" target="_blank">
          <img class="thumbnail" src="{thumb_src}" width="{file['tn_width']}" height="{file['tn_height']}" alt="{displayname}">
        </a>
      </div>
"""

    end_post_html = f"""
     <div class="post-comment">
            {comment}
          </div>
    </article>
"""
    return header_post_html + body_post_html + end_post_html


op_html = """
 <article class="post op" id="337358784">
      <div class="post-header">
        <span class="post-name">Аноним</span>
        <span class="post-date">12/10/26 Пнд 18:44:37</span>
        <span class="post-num"><a href="#337358784">№337358784</a></span>
        <span class="badge op-badge">OP</span>
        <span class="badge sticky">Закреплён</span>
      </div>

      <div class="post-file op-file">
        <div class="file-info">
          Файл:
          <a href="#">shiza.png</a>
          <span class="file-stats">(124.5 КБ, 800x600)</span>
        </div>
        <a href="#">
          <img class="thumbnail"
               src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='250' height='188'%3E%3Crect width='250' height='188' fill='%23404040'/%3E%3Ctext x='125' y='100' font-family='sans-serif' font-size='20' fill='%23ffffff' text-anchor='middle'%3EОП-пост%3C/text%3E%3C/svg%3E"
               alt="shiza.png" width="250" height="188">
        </a>
      </div>

      <div class="post-comment">
        <a href="#337358784" class="quote">&gt;&gt;&gt;337358784</a> (OP)<br>
        вид мени справка по шизе не могу
      </div>
    </article>
    """


os.makedirs(thread_dir, exist_ok=True)
os.makedirs(src_dir, exist_ok=True)
os.makedirs(thumb_dir, exist_ok=True)

result_html = header_html + body_header_html + body_main_html
for post in posts:
    is_op = post["num"] == int(thread)
    result_html += generate_post(
        is_op,
        post["num"],
        post["name"],
        post["date"],
        post["comment"],
        post["files"],
    )

result_html += end_html


with open(os.path.join(thread_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(result_html)
