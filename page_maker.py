import os
from file_downloader import download_file
from urllib.parse import urlparse


def get_header_html() -> str:
    return """<!DOCTYPE html>
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


def get_body_header_html() -> str:
    return """
<body>
 <header class="board-header">
    <h1>/b/</h1>
    <span class="board-title">Бред</span>
  </header>
"""


def get_body_main_html(thread, info_thr_json, info_thr_timestamps) -> str:
    return f"""
  <main class="thread">
  <div class="thread-info">
        Тред №{thread} &middot; {info_thr_json["thread"]["posts"]} постов &middot;  создан {info_thr_timestamps}
      </div>

  """


def get_end_html() -> str:
    return """
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


def get_op_html() -> str:
    return """
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


def generate_post(
    op,
    num,
    name,
    date,
    comment,
    files: list | None,
    thread,
    src_dir,
    thumb_dir,
    default_url,
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

            src_ok = download_file(
                default_url + file["path"], os.path.join(src_dir, file_name)
            )
            thumb_ok = download_file(
                default_url + file["thumbnail"], os.path.join(thumb_dir, thumb_name)
            )

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


def get_result_html(
    thread,
    src_dir,
    thumb_dir,
    posts,
    default_url,
    info_thr_json,
    info_thr_timestamps,
    is_op,
) -> str | None:
    result_html = (
        get_header_html()
        + get_body_header_html()
        + get_body_main_html(thread, info_thr_json, info_thr_timestamps)
    )
    for post in posts:
        is_op = post["num"] == int(thread)
        result_html += generate_post(
            is_op,
            post["num"],
            post["name"],
            post["date"],
            post["comment"],
            post["files"],
            thread=thread,
            src_dir=src_dir,
            thumb_dir=thumb_dir,
            default_url=default_url,
        )

    result_html += get_end_html()
    return result_html
