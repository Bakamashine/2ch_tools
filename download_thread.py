import requests
import os
from datetime import datetime
from urllib.parse import urlparse
import page_maker
import argparse
import json
from file_downloader import download_file


def main():
    parse = argparse.ArgumentParser(prog="download_thread")
    parse.add_argument("--url", "-u", help="thread url")
    args = vars(parse.parse_args())

    base_url = "https://2ch.org"
    # board = "b"
    # thread = "337358784"

    board = input("Enter board name: ")
    thread = input("ID thread: ")
    thread_dir = f"threads/{thread}"
    src_dir = os.path.join(thread_dir, "src")
    thumb_dir = os.path.join(thread_dir, "thumb")
    info_thread = requests.get(base_url + f"/api/mobile/v2/info/{board}/{thread}")

    # b'{"result":1,"thread":{"num":337358784,"posts":120,"timestamp":1791819784}}'
    if info_thread.status_code != 200:
        print(f"Failed to get thread info: HTTP {info_thread.status_code}")
        return

    print("Thread is exists")

    info_thr_json = info_thread.json()
    info_thr_timestamps = datetime.fromtimestamp(
        info_thr_json["thread"]["timestamp"]
    ).strftime("%d/%m/%Y %H:%M:%S")

    posts_from_thread = requests.get(
        base_url + f"/api/mobile/v2/after/{board}/{thread}/{thread}"
    )

    if posts_from_thread.status_code != 200:
        print(f"Failed to get posts: HTTP {posts_from_thread.status_code}")
        return

    posts = posts_from_thread.json()["posts"]

    os.makedirs(thread_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(thumb_dir, exist_ok=True)

    if isinstance(args["url"], str) and len(str(args["url"])) > 0:
        with open(os.path.join(thread_dir, "index.html"), "w", encoding="utf-8") as f:
            html_page = page_maker.get_result_html(
                thread=thread,
                default_url=base_url,
                posts=posts,
                src_dir=src_dir,
                thumb_dir=thumb_dir,
                info_thr_json=info_thr_json,
                info_thr_timestamps=info_thr_timestamps,
                is_op=0,
            )
            if isinstance(html_page, str):
                f.write(html_page)

    # downloading files
    for post in posts:
        files = post.get("files") or []
        for file in files:
            if file is None:
                continue
            file_name = file.get("name") or os.path.basename(urlparse(file["path"]).path)
            src_url = base_url + file["path"]
            thumb_url = base_url + file["thumbnail"]
            download_file(src_url, os.path.join(src_dir, file_name))
            download_file(
                thumb_url,
                os.path.join(thumb_dir, os.path.basename(urlparse(file["thumbnail"]).path)),
            )
    with open(
        os.path.join(thread_dir, f"{thread}.json"), "w", encoding="utf-8"
    ) as json_file:
        json.dump(posts, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
