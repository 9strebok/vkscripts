import argparse
import getpass
import os
import time

from progress.bar import IncrementalBar
import vk_api

PARSER = argparse.ArgumentParser(description="Parse user gifts")

# add python3 gifts.py -u [id]

PARSER.add_argument("users",
                    nargs = "*",
                    type  = int,
                    help  = "python3 gifts.py [user_id_1] [user_id_2] [...]")

# add python3 gifts.py -x [max]

PARSER.add_argument("-m",
                    "--min",
                    type    = int,
                    dest    = "min",
                    default = 0,
                    help    = "python3 gifts.py -x [max]")



args = PARSER.parse_args()

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


def delete_vk_config():
    if os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")
    os.walk("..")
    if os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")


def get_gifts(account: vk_api.vk_api.VkApiMethod,user: int):
    try:
        print()
        gifts_list = account.gifts.get(user_id=user)
        bar = IncrementalBar(str(user), max = len(gifts_list.get("items")))
        usrs = []
        for i in gifts_list.get("items"):
            if not i.get("from_id") in usrs:
                usrs.append(i.get("from_id"))
            bar.next()
            time.sleep(0.01)
        bar.finish()
        print()

        res = []
        for usr in usrs:
            tmp = 0
            for i in gifts_list.get("items"):
                if i.get("from_id") == usr:
                    tmp += 1
            if usr < 0 and tmp >= args.min:
                usr = str(abs(usr))
                public = "https://vk.com/public"
                s = f"echo '\e]8;;{public}{usr}\\a{public}{usr}\e]8;;\\a\t' {tmp}"
                os.system(s)
            elif usr > 0 and tmp >= args.min:
                usr = str(usr)
                vkid = "https://vk.com/id"
                s = f"echo '\e]8;;{vkid}{usr}\\a{vkid}{usr}\e]8;;\\a\t' {tmp}"
                os.system(s)
        print()

        groups_gifts = 0
        users_gifts = 0
        for i in gifts_list.get("items"):
            if i.get("from_id") < 0:
                groups_gifts += 1
            elif i.get("from_id") > 0:
                users_gifts += 1
        unidentified = gifts_list.get("count") - (groups_gifts + users_gifts)
        print("Count:                  \t", gifts_list.get("count"))
        print("Gifts from groups:      \t", groups_gifts)
        print("Gifts from users:       \t", users_gifts)
        print("Unidentified gifts:     \t", unidentified)
        print()
    except:
        print("Error, maybe you can't to get gifts list")
        print()

def main():
    BANNER = """
        .__  _____  __
   ____ |__|/ ____\/  |_  ______
  / ___\|  \   __\\\\   __\/  ___/
 / /_/  >  ||  |   |  |  \___ \\
 \___  /|__||__|   |__| /____  >
/_____/                      \/

"""

    print(BANNER)
    account = authorize()
    for usr in args.users:
        get_gifts(account, usr)
    print()


if __name__ == "__main__":
    main()
    delete_vk_config()
