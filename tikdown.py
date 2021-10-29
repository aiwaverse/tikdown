from genericpath import exists
from lib2to3.pytree import Base
from TikTokApi import TikTokApi
from TikTokApi import exceptions
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
    return f"https://www.tiktok.com/@{user}/video/{video_id}"


def get_pager(api: TikTokApi, user: str) -> Generator:
    if exists(f"{user}-gen.pickle"):
        return load_generator(user)
    return api.get_user_pager(user, page_size=1, cursor=0)


def main():
    print("Creating TikTokApi instance...")
    api: TikTokApi = TikTokApi.get_instance()
    user: str = "apoki.vv"
    path_prefix = "./apoki.vv"
    if api:
        print("Api instance succefully created.")
        # user = api.get_user(user)
        # user_fed_config = user[]
        # feed_config = user["feedConfig"]
        # user_id = feed_config["id"]
        # sec_uid = feed_config["secUid"]
        # page = api.user_page(user_id, sec_uid, 10, cursor)
        # print(page)
        print(f"Creating pager for @{user}")
        user_pager = get_pager(api, user)
        print("Pager created")
        try:
            for item in user_pager:
                video_id = item[0]["id"]
                print(f"Extracting video {video_id} data...")
                video_download_addr = item[0]["video"]["downloadAddr"]
                video = api.get_video_by_download_url(video_download_addr)
                print(f"Video {video_id} data extracted...")
                print(f"Saving video {video_id}...")
                save_video(video, f"{path_prefix}/{video_id}.mp4")
                print(f"Video saved to {path_prefix}/{video_id}.mp4")
        except TikTokApi.exceptions.TikTokCaptchaError:
            print("Error with the pager, run this again.")
        except BaseException:
            save_generator(user, user_pager)
    else:
        print("Error creating the Api instance.")


if __name__ == "__main__":
    main()
