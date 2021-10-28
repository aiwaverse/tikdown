from genericpath import exists
from TikTokApi import TikTokApi
from typing import *
from os import path
import pickle


def save_generator(user: str, gen: Generator) -> None:
    with open(f"{user}-gen.pickle", "wb") as f:
        pickle.dump(gen, f)


def load_generator(user: str) -> Generator:
    with open(f"{user}-gen.pickle", "rb") as f:
        data = pickle.load(f)
    return data


def save_video(bin, path: str) -> None:
    if not exists(path):
        with open(path, "wb") as f:
            f.write(bin)


def create_video_url(user: str, video_id: str):
    return f"https://www.tiktok.com/{user}/video/{video_id}"


def get_pager(api: TikTokApi, user: str) -> Generator:
    if exists(f"{user}-gen.pickle"):
        return load_generator(user)
    return api.get_user_pager(user, page_size=1, cursor=0)


def main():
    api: TikTokApi = TikTokApi.get_instance()
    user: str = "apoki.vv"
    path_prefix = "."
    if api:
        # user = api.get_user(user)
        # user_fed_config = user[]
        # feed_config = user["feedConfig"]
        # user_id = feed_config["id"]
        # sec_uid = feed_config["secUid"]
        # page = api.user_page(user_id, sec_uid, 10, cursor)
        # print(page)
        user_pager = get_pager(api, user)
        for item in user_pager:
            try:
                video_id = item[0]["id"]
                video = api.get_video_by_download_url(create_video_url(user, video_id))
                save_video(video, f"{path_prefix}/{video_id}.mp4")
            except BaseException:
                save_generator(user_pager)
                break


if __name__ == "__main__":
    main()
