import requests
import os
from datetime import datetime
from urllib.parse import urlparse
import page_maker
import argparse
from file_downloader import download_file


def main():
    default_url = "https://2ch.org"
    # board = "b"
    # thread = "337358784"

    board = input("Enter board name: ")
    thread = input("ID thread: ")
    thread_dir = f"threads/{thread}"
    src_dir = os.path.join(thread_dir, "src")
    thumb_dir = os.path.join(thread_dir, "thumb")
    info_thread = requests.get(default_url + f"/api/mobile/v2/info/{board}/{thread}")

    # b'{"result":1,"thread":{"num":337358784,"posts":120,"timestamp":1791819784}}'
    if info_thread.status_code == 200:
        print("Thread is exists")
        print(info_thread.content)

    info_thr_json = info_thread.json()
    info_thr_timestamps = datetime.fromtimestamp(
        info_thr_json["thread"]["timestamp"]
    ).strftime("%d/%m/%Y %H:%M:%S")

   
    posts_from_thread = requests.get(
        default_url + f"/api/mobile/v2/after/{board}/{thread}/{thread}"
    )

    posts = posts_from_thread.json()["posts"]

    os.makedirs(thread_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(thumb_dir, exist_ok=True)

    # with open(os.path.join(thread_dir, "index.html"), "w", encoding="utf-8") as f:
    #     html_page = page_maker.get_result_html(
    #         thread=thread,
    #         default_url=default_url,
    #         posts=posts,
    #         src_dir=src_dir,
    #         thumb_dir=thumb_dir,
    #         info_thr_json=info_thr_json,
    #         info_thr_timestamps=info_thr_timestamps,
    #         is_op=0,
    #     )
    #     if html_page is str:
    #         f.write(html_page)
    with open(os.path.join(thread_dir, f"{thread}.json"), "w") as json_file:
        json_file.write(str(posts))

if __name__ == "__main__":
    main()
