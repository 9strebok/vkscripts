import os
import argparse

import vk_api
import getpass


PARSER = argparse.ArgumentParser(description="")
PARSER.add_argument("users", nargs="*", type=int, help="python3 gifts.py [user_id_1] [user_id_2] [user_id_3]")
args = PARSER.parse_args()


BANNER = """
   _____                            ___________      .__                   .___
  /     \   ___________  ____   ____\_   _____/______|__| ____   ____    __| _/______
 /  \ /  \_/ __ \_  __ \/ ___\_/ __ \|    __) \_  __ \  |/ __ \ /    \  / __ |/  ___/
/    Y    \  ___/|  | \/ /_/  >  ___/|     \   |  | \/  \  ___/|   |  \/ /_/ |\___ \
\____|__  /\___  >__|  \___  / \___  >___  /   |__|  |__|\___  >___|  /\____ /____  >
        \/     \/     /_____/      \/    \/                  \/     \/      \/    \/
"""


def delete_vk_config():
    if os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")
    os.walk("..")
    if os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")


def authorize():
    try:
        login = input("[?] LOGIN: ")
        try:
            passwd = getpass.getpass("[?] PASSWORD: ")
        except:
            print("[!] Error")
            passwd = getpass.getpass("[?] PASSWORD: ")
        api = vk_api.VkApi(login=login, password=passwd, session=None)
        api.auth()
        api = api.get_api()
        return api
    except vk_api.BadPassword as e:
        print("[!] Bad password")


def get_unique(l: list):
    res = []
    for i in l:
        c = l.count(i)
        if c > 1:
            res.append(i)
            l.remove(i)
    return res


def main():
    print(BANNER)
    account = authorize()

    merged_friends = []

    for usr in args.users:
        friends = account.friends.get(user_id=usr).get("items")
        merged_friends.extend(friends)

    res = get_unique(merged_friends)

    vkid = "https://vk.com/id"
    for r in res:
        s = f"echo '\e]8;;{vkid}{r}\\a{vkid}{r}\e]8;;\\a\t'"
        os.system(s)


if __name__ == "__main__":
    main()
    delete_vk_config()
