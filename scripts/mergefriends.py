import os
import argparse

import vk_api
import getpass


PARSER = argparse.ArgumentParser(description="")
PARSER.add_argument("-u1", "--user1", action="store", type=int, dest="user1", help="python3 gifts.py -u1 [user_id] -u2 [user_id]")
PARSER.add_argument("-u2", "--user2", action="store", type=int, dest="user2", help="python3 gifts.py -u1 [user_id] -u2 [user_id]")
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
        

def main():
    print(BANNER)
    account = authorize()

    u1 = account.friends.get(user_id=args.user1).get("items")
    u2 = account.friends.get(user_id=args.user2).get("items")
    print(f"Merge: %s / %s" % ("vk.com/id" + str(args.user1), "vk.com/id" + str(args.user2)))

    for u in u1:
        if u in u2:
            print("\tvk.com/id" + str(u))


if __name__ == "__main__":
    main()
    delete_vk_config()
