import argparse
import getpass
import os
import time

# Nonlocal imports
from progress.bar import IncrementalBar
import vk_api


# Parser
PARSER = argparse.ArgumentParser(description="Parse user gifts")


# add python3 gifts.py [user_id_1] [user_id_2]
PARSER.add_argument("users",
                    nargs   = "*",
                    type    = int,
                    help    = "python3 gifts.py [user_id_1] [user_id_2] [...]")


# add python3 gifts.py -m [min]
PARSER.add_argument("-m",
                    "--min",
                    type    = int,
                    dest    = "min",
                    default = 0,
                    help    = "python3 gifts.py -x [max]")


args = PARSER.parse_args()


class Colors():
    HEADER = '\033[95m'
    MAINCOLOR = '\033[33m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def color_string(string: str) -> str:
    new_string = f"{Colors.MAINCOLOR}{Colors.BOLD}{string}{Colors.ENDC}"
    return new_string


def nice_output(output: str) -> None:
    new_output = f"{Colors.MAINCOLOR}{Colors.BOLD}{output}{Colors.ENDC}"
    print(new_output)


def nice_output_with_content(output: str, content) -> None:
    new_output = f"{Colors.MAINCOLOR}{Colors.BOLD}\t{output}\t{Colors.ENDC}"
    print(new_output, content)


def authorize():
    try:
        login = input(color_string("[?] LOGIN: "))
        try:
            passwd = getpass.getpass(color_string("[?] PASSWORD: "))
        except:
            print("[!] Error")
            passwd = getpass.getpass(color_string("[?] PASSWORD: "))
        api = vk_api.VkApi( login = login,
                            password = passwd,
                            session = None )
        api.auth()
        api = api.get_api()
        return api

    except vk_api.BadPassword:
        print("[!] Bad password")


def delete_vk_config():
    if os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")
    os.walk("..")
    if os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")


def get_gifts(account: vk_api.vk_api.VkApiMethod, user: int):
    try:
        print()
        gifts_list   = account.gifts.get(user_id  = user)
        account_info = account.users.get(user_ids = user)

        # Create status bar
        bar_name = str(account_info[0].get("first_name") + " " + account_info[0].get("last_name"))

        bar = IncrementalBar(
                color_string(bar_name),
                max = len(gifts_list.get("items"))
        )

        usrs = []
        for i in gifts_list.get("items"):
            if not i.get("from_id") in usrs:
                usrs.append(i.get("from_id"))
            bar.next()
            time.sleep(0.005)
        bar.finish()
        print()

        res = []
        for usr in usrs:
            tmp = 0

            for i in gifts_list.get("items"):
                if i.get("from_id") == usr:
                    tmp += 1

            if usr < 0 and tmp >= args.min:

                usr              = str(abs(usr))
                public           = "https://vk.com/public"
                public_plus_user = f"{public}{usr}"
                output           = color_string(f"\t\e]8;;{public_plus_user}\\a{public_plus_user}\e]8;;\\a\t")
                out              = f"echo '{output} {tmp}'"

                os.system(out)

            elif usr > 0 and tmp >= args.min:

                usr              = str(usr)
                vkid             = "https://vk.com/id"
                vkid_plus_usr    = f"{vkid}{usr}"
                output           = color_string(f"\t\e]8;;{vkid_plus_usr}\\a{vkid_plus_usr}\e]8;;\\a\t")
                out              = f"echo '{output} {tmp}'"

                os.system(out)
        print()

        groups_gifts = 0
        users_gifts = 0

        for i in gifts_list.get("items"):
            if i.get("from_id") < 0:
                groups_gifts += 1
            elif i.get("from_id") > 0:
                users_gifts += 1

        unidentified = gifts_list.get("count") - (groups_gifts + users_gifts)

        nice_output_with_content("Count:                  ", gifts_list.get("count"))
        nice_output_with_content("Gifts from groups:      ", groups_gifts)
        nice_output_with_content("Gifts from users:       ", users_gifts)
        nice_output_with_content("Unidentified gifts:     ", unidentified)
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
    BANNER = color_string(BANNER)
    print(BANNER)
    account = authorize()
    [get_gifts(account, usr) for usr in args.users]


if __name__ == "__main__":
    main()
    delete_vk_config()
