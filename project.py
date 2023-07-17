"""
Created with ❤️ by
Pratyush Roshan Mallik
Ghaziabad, India
July,2023
"""
from ascii_art import start, woah, bye
from merge import create_card, paste_pdf, add_text_to_image
import random
import time
import sys
import csv
import os
import re
import threading
from pyfiglet import Figlet

f = Figlet()
f.setFont(font="big")

# Global Var
money = 0

def main(chk=0):
    os.system('clear')
    if chk == 0:
        print("Pocket Monsters Trading Cards")           # default starting
    elif chk == 1:
        print("Please enter the correct letter")        #called when code is wrong
    print()
    start()
    ans = input("\nDo you want to buy some ⚡Pokémon🐭 trading cards (Y/N): ").strip().lower()       #start the game or quit
    if ans == "y":
        vault(30.0)
        os.system('clear')
        buy()
    elif ans == 'n':
        os.system('clear')
        bye()
        print("\nOkay then, See you later 😄\n")        #goodbye message
    elif ans == 'CS':
        print('Dev Mode \n Under works')      #under works
        sys.exit()
    else:
        main(chk=1)         #return to start

def menu(ans=None):  #Menu to select from buy, sell, save and exit
    try:
        print()
        if ans == None:
            print("You currently have: ${:.2f}".format(vault(0.0)))
            out = int(input("""What do you want to do now:
                Buy more Pokemon:        [1]
                Show/Sell your Pokemon:  [2]
                Save your Pokemon Cards: [3]
                Exit:                    [0]
                Enter your choice: """))
            return menu(ans=out)            #call the menu again with an ans
        if ans == 1:
            os.system('clear')
            return buy()
        elif ans == 2:
            os.system('clear')
            return sell()
        elif ans == 3:
            menu(save())
        elif ans == 0:
            os.system('clear')
            bye()
            print("\nOkay then, See you later 😄\n")
            try:                                                #remove temporary files created during the procedure
                os.remove("Vault/poke_details.csv")
                os.remove("asset/temp.PNG")
                for filename in os.listdir("asset/Temp/"):
                    file_path = os.path.join("asset/Temp/", filename)
                    os.remove(file_path)
            except:
                sys.exit()
        else:
            raise ValueError
    except ValueError:
        os.system("clear")
        woah()
        print("Enter the correct key")
        return menu()

def vault(m=0.0, row_index=None):           #vault to store money and pokemon cards
    global money

    if type(m) == float:
        money += m
        return money
    elif m == 'show':
        print(f.renderText(" Your Collection "))
        with open("Vault/poke_details.csv", mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) == 1:
                print("Your Collection is empty")
                return 0
            print(f" Index: ", end='  ')
            print("   Pokemon:  ", end=' ')
            print("       Card Tier: ",  end=' ')
            print(" Pokemon Value: ", )
            for row_counter, row in enumerate(rows[1:], start=1):
                pokemon_name = row[4]
                card_tier = int(row[7])
                pokemon_value = row[6]
                print('  ', row_counter, end='  ')
                print(pokemon_name, end='     ')
                print(star(card_tier), end='   ')
                print("  $", pokemon_value)
                print("-------------------------------------------------------------")
    elif m == 'remove' and row_index is not None:
        with open("Vault/poke_details.csv", mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) < 1:
                os.system("clear")
                return menu(0)
            if row_index >= 1 and row_index < len(rows):
                removed_row = rows.pop(row_index)
                value = float(removed_row[6])
                os.remove(removed_row[8])
                vault(value)
                print("You sold ", removed_row[4], " for $", value)
        with open("Vault/poke_details.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        return menu()
    else:
        return menu(0)

def buy():              #buy pokemon
    if vault() < 10.0:
        s = input("""Uh Oh you don't have enough money to buy more packs.
You have to sell some of your cards to get more money. [Y/N]: """)
        if s == 'y':
            return sell()
        else:
            return menu()
    vault(-10.0)
    print(f.renderText(" You got :"))
    print("-------------------------------------------------------------")
    for _ in range(4):
        show_spinners(0.6)
        get_pm()
    return menu()

def sell():             #sell pokemon
    os.system("clear")
    check = vault('show')
    if check == 0:
        return menu()
    idx = input("Please enter the index of the Pokemon you want to sell:\nOR [Enter any letter to exit]: ")
    if idx.isnumeric():
        idx = int(idx)
        vault('remove', row_index=idx)
        return None
    else:
        return menu()

def get_pm():               # get a random pokemon card of varying rarity
    type_card = [
        {"tier": 'Common    ', "pm": {'c_1': {'name': '    🥬Bulbasaur🥬   ', 'value': (900, 60), 'money': 2},
                                      'c_2': {'name': '     👻Gastly👻     ', 'value': (650, 200), 'money': 2},
                                      'c_3': {'name': '    🐟Magikarp🐟    ', 'value': (660, 190), 'money': 1},
                                      'c_4': {'name': '  🦆❓Psyduck❓🦆   ', 'value': (700, 150), 'money': 4},
                                      'c_5': {'name': '    💦Squirtle💦    ', 'value': (850, 90), 'money': 2}},
         "weights": [5, 3, 10, 1, 5]
        },
        {"tier": 'Rare      ', "pm": {'r_1': {'name': '     ⚡Pikachu⚡    ', 'value': (700, 180), 'money': 6},
                                      'r_2': {'name': '     💤Snorlax💤    ', 'value': (550, 240), 'money': 8}},
         "weights": [4, 1]
        },
        {"tier": 'Super Rare', "pm": {'sr_1': {'name': '     🔥Charizard🔥  ', 'value': (550, 260), 'money': 14},
                                      'sr_2': {'name': '     🌊Gyarados🌊   ', 'value': (530, 260), 'money': 20}},
         "weights": [3, 2]
        },
        {"tier": 'Legendary ', "pm": {'l_1': {'name': '     🐲Dragonite🐲  ', 'value': (530, 230), 'money': 30},
                                      'l_s': {'name': '  ✨🐲Dragonite🐲✨', 'value': (530, 230), 'money': 40}},
         "weights": [9, 1]
        },
        {"tier": 'Mythic    ', "pm": {'m_1': {'name': '       🍥Mew🍥      ', 'value': (730, 130), 'money': 40},
                                      'm_s': {'name': '     ✨🍥Mew🍥✨   ', 'value': (730, 130), 'money': 50}},
         "weights": [9, 1]
        }
    ]

    weights = [50, 24, 15, 7, 4]
    pokemon_tier_index = random.choices(range(5), weights=weights)[0]
    pokemon_tier = type_card[pokemon_tier_index]["tier"]

    pokemon_index = random.choices(range(len(type_card[pokemon_tier_index]["pm"])),
                                   weights=type_card[pokemon_tier_index]["weights"])[0]
    random_dict = list(type_card[pokemon_tier_index]["pm"].values())[pokemon_index]
    pokemon_name = random_dict["name"]

    pokemon_size, pokemon_y = random_dict["value"]
    pokemon_value = random_dict["money"]
    pokemon_file = list(type_card[pokemon_tier_index]["pm"].keys())[pokemon_index]

    card_tier_type = [{"Common": 1, "multiplier": 1},
                      {"Rare": 2, "multiplier": 1.1},
                      {"Super Rare": 3, "multiplier": 1.2},
                      {"Legendary": 4, "multiplier": 1.5},
                      {"Mythic": 5, "multiplier": 2}
    ]

    card_tier = random.choices(card_tier_type, weights=weights)
    card_dict = card_tier[0]

    stars = [card_dict[x] for x in card_dict][0]
    multiplier = [card_dict[x] for x in card_dict][1]
    bg = f"b_{stars}"
    is_shiny = False
    pokemon_value = round(pokemon_value ** multiplier, 2)
    s_pokemon_tier = pokemon_tier.strip()

    if '✨' in pokemon_name:
        text_color_code = 93  # yellow
        is_shiny = True
    elif s_pokemon_tier == 'Mythic':
        text_color_code = 94  # blue
    elif s_pokemon_tier == 'Rare':
        text_color_code = 95  # magenta
    elif s_pokemon_tier == 'Super Rare':
        text_color_code = 92  # green
    elif s_pokemon_tier == 'Legendary':
        text_color_code = 31  # red
    else:
        text_color_code = 96  # cyan

    colour_tier = f"\033[{text_color_code}m{pokemon_tier}\033[0m"
    colour_name = f"\033[{text_color_code}m{pokemon_name}\033[0m"
    print("You Got:", colour_name, end=" ")
    print("Pokemon Tier:", colour_tier, end=" ")
    print("Card Tier: ", star(stars), end=" ")
    print("Est. Value: $", "{:.2f}".format(pokemon_value))
    print("-----------------------------------------------------------------------------------------------")

    if matches := re.findall(r"\b[\w\s]+\b", pokemon_name):
        base_name = matches[0]

    poke_details = {
        "file_name": pokemon_file,
        "background": bg,
        "pokemon_size": pokemon_size,
        "pokemon_y": pokemon_y,
        "pokemon_name": colour_name,
        "is_shiny": is_shiny,
        "pokemon_value": pokemon_value,
        "card_tier": stars,
        "image_file": '',
        "base_name": base_name
    }

    output = create_card(poke_details)
    output = add_text_to_image(output[0], output[1])
    poke_details["image_file"] = output
    write_to_csv(poke_details)
    return None

def show_spinners(duration):                # a basic spinning indicator
    spinners = ['/', '-', '\\', '|', '/', '-', '\\', '|']
    start_time = time.time()

    while time.time() - start_time < duration:
        print("       ", end="")
        output = ' '.join(spinners)
        sys.stdout.write(output + '\r')
        sys.stdout.flush()
        spinners.insert(0, spinners.pop())
        time.sleep(0.1)
    sys.stdout.write(' ' * 40 + '\r')
    sys.stdout.flush()
    return None

def write_to_csv(poke_details):             # write details of pokemon to a csv file for retreival later
    csv_file = "Vault/poke_details.csv"
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a' if file_exists else 'w', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(poke_details.keys())
        writer.writerow(poke_details.values())
    return None

def save(chk=None):                 # save you pokemon in a pdf file and exit
    try:
        print()
        if chk == None:
            chk = input("If you save now, the game will end. Are you sure you want to save right now? [Y/N]: ").strip().lower()
        if chk == 'y':
            files = os.listdir("asset/Temp/")
            if len(files) == 0:
                return 0
            else:
                spinner_thread = threading.Thread(target=show_spinners, args=(2,))
                spinner_thread.start()
                paste_pdf()
                spinner_thread.join()
                return 0
        elif chk == 'n':
            os.system("clear")
            return None
        else:
            os.system('clear')
            woah()
            return None
    except ValueError:
        return 0

def star(s):                        #print different number of stars according to the card tier
    if 0 < s < 6:
        s = s - 1
        stars = [
            "    ⭐      ",
            "   ⭐⭐     ",
            "  ⭐⭐⭐   ",
            " ⭐⭐⭐⭐  ",
            "⭐⭐⭐⭐⭐ ",
        ]
        return stars[s]
    else:
        raise ValueError

if __name__ == "__main__":
    main()
