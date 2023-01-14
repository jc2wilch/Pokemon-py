from os import access
import json
import random
import time
from sqlite3 import enable_callback_tracebacks
from PokemonClasses import Pokemon, Move, StatusMove, StatusCondition


maxPokemon = 3
maxMoves = 4 # Change back to 4 --------------------------------------------------------

# status conditions
none = StatusCondition("None", False, [], 0, "N/A", "N/A")
burn = StatusCondition("Burn", False, ["Fire"], 1/16, "Enemy", "burned")
poison = StatusCondition("Poison", False, ["Poison", "Steel"], 1/8, "Enemy", "poisoned")
badPoison = StatusCondition("Badly Poisoned", True, ["Poison", "Steel"], 1/16, "Enemy", "badly poisoned")
paralysis = StatusCondition("Paralysis", False, ["Electric"], 0, "Enemy", "paralyzed")
restSleep = StatusCondition("Sleep", False, [], 0, "Self", "asleep")
sleep = StatusCondition("Sleep", False, [], 0, "Enemy", "asleep")
freeze = StatusCondition("Freeze", False, ["Ice"], 0, "Enemy", "frozen")

# moves - name, catagory, type, accuracy, dmg, effect, effect acc, priority
# Status moves - name, catagory, type, acc, effect on enemy, eff on enemy stats, eff on player, eff on player stats, player stat eff amount, priority
# Electric
thunderbolt = Move("Thunderbolt", "Special", "Electric", 100, 90, none, 0, 0)
thunderWave = StatusMove("Thunder Wave", "Status", "Electric", 90, paralysis, "None", none, "None", 0, 0)
# Steel
ironTail = Move("Iron Tail", "Physical", "Steel", 75, 100, none, 0, 0)
# Normal
quickAttack = Move("Quick Attack", "Physical", "Normal", 100, 40, none, 100, 1)
pound = Move("Pound", "Physical", "Normal", 100, 40, none, 0, 0)
facade = Move("Facade", "Physical", "Normal", 100, 70, none, 0, 0)
# Water
hydroPump = Move("Hydro Pump", "Special", "Water", 80, 110, none, 0, 0)
scald = Move("Scald", "Special", "Water", 100, 80, burn, 30, 0) 
# Psychic
rest = StatusMove("Rest", "Status", "Psychic", 100, none, "None", restSleep, "Heal", 0, 0) # 0 instead of 1 for pstEff amount b/c i alr coded for rest move specifically and don't want any bugs out of nowhere
# Ice
iceBeam = Move("Ice Beam", "Special", "Ice", 100, 90, freeze, 10, 0)
# Ground
earthquake = Move("Earthquake", "Physical", "Ground", 100, 100, none, 0, 0)
# Fire
flamethrower = Move("Flamethrower", "Special", "Fire", 100, 90, burn, 10, 0)
fireBlast = Move("Fire Blast", "Special", "Fire", 80, 110, burn, 10, 0)
# Dragon
dragonClaw = Move("Dragon Claw", "Physical", "Dragon", 100, 80, none, 0, 0)
# Grass
petalBlizzard = Move("Petal Blizzard", "Physical", "Grass", 100, 90, none, 0, 0)
sleepPowder = StatusMove("Sleep Powder", "Status", "Grass", 75, sleep, "None", none, "None", 0, 0)
synthesis = StatusMove("Synthesis", "Status", "Grass", 100, none, "None", none, "Heal", 1/4, 0)
seedBomb = Move("Seed Bomb", "Physical", "Grass", 100, 80, none, 0, 0)
# Poison
poisonPowder = StatusMove("Poison Powder", "Status", "Poison", 75, poison, "None", none, "None", 0, 0)
venoShock = Move("Venoshock", "Special", "Poison", 100, 65, none, 0, 0)
sludgeBomb = Move("Sludge Bomb", "Special", "Poison", 100, 90, poison, 30, 0)
toxic = StatusMove("Toxic", "Status", "Poison", 90, badPoison, "None", none, "None", 0, 0)



idIndex = 1
# pokemon
def createPokemon(name):
    global idIndex

    # pokedicts
    pokemonDict = {
        # Using max lvl 50 stats (From bulbapedia)
        #                   name, maxHp, att, spAtt, defense, spDef, speed, ty, ty2, effect, identifier, priority
        "pikachu": Pokemon("Pikachu", 142, 117, 112, 101, 112, 156, "Electric", "None", none, idIndex, 0), # gen 6 onward
        "vaporeon": Pokemon("Vaporeon", 237, 128, 178, 123, 161, 128, "Water", "None", none, idIndex, 0),
        "charizard": Pokemon("Charizard", 185, 149, 177, 143, 150, 167, "Fire", "Flying", none, idIndex, 0),
        "venusaur": Pokemon("Venusaur", 187, 147, 167, 148, 167, 145, "Grass", "Poison", none, idIndex, 0)
    }

    # move dicts
    movesDict = {
        "pikachu": [thunderbolt, thunderWave, ironTail, quickAttack, pound],
        "vaporeon": [hydroPump, scald, pound, rest, iceBeam],
        "charizard": [flamethrower, earthquake, dragonClaw, fireBlast, pound, ironTail, facade],
        "venusaur": [synthesis, poisonPowder, sleepPowder, petalBlizzard, rest, facade, sludgeBomb, seedBomb, earthquake, toxic, venoShock]
    }

    pokemon = pokemonDict.get(name.lower())
    if pokemon:
        idIndex += 1
        pokemon.addMoves(*movesDict[name.lower()])
        return pokemon
    else:
        # If the Pokemon object was not found
        return 0

pokemonList = ["Pikachu", "Vaporeon", "Charizard", "Venusaur"]

playerPokemon = []
namesChosen = False

enemyPokemon = []

with open('teams.json', 'r') as f:
    prevData = json.load(f)
    dataLength = len(prevData)

if dataLength > 0:
    print("You have saved teams available!")
    print("Saved teams available: ")
    for team in prevData:
        print(prevData[team]['name'])

    confirm = ""
    while confirm != "yes":
        delTeam = ""
        while delTeam != "yes" and delTeam != "no":
            delTeam = str.lower(input("Would you like to delete a team? "))
            if delTeam != "yes" and delTeam != "no":
                print("Please type in 'yes' or 'no'!")

        if delTeam == "yes":
            found = False
            while not found:
                delTeam = str.lower(input("Which team? "))
                for team in prevData:
                    if str.lower(prevData[team]['name']) == delTeam:
                        found = True
                        delTeam = team
                if not found:
                    print("That's not a team name! Please check your spelling and try again!")
            confirm = ""
            while confirm != "yes" and confirm != "no":
                confirm = str.lower(input("Are you sure? "))

            if confirm == "yes":
                del prevData[delTeam]

                if len(prevData) > 0:
                    i = 1
                    for teamName in prevData.copy():
                        prevData['team_' + str(i)] = prevData[teamName]
                        del prevData[teamName]
                        i += 1

                with open('teams.json', 'w') as f:
                    json.dump(prevData,f)
        else:
            break

    with open('teams.json', 'r') as f:
        prevData = json.load(f)
        dataLength = len(prevData)

    if dataLength > 0:
        print("")
        confirm = ""
        while confirm != "yes":
            selectTeam = ""
            while selectTeam != "yes" and selectTeam != "no":
                selectTeam = str.lower(input("Would you like to select one of your saved teams? "))
                if selectTeam != "yes" and selectTeam != "no":
                    print("Please type in 'yes' or 'no'!")

            if selectTeam == "yes":
                found = False
                while not found:
                    selectTeam = str.lower(input("Which team? "))
                    for team in prevData:
                        if str.lower(prevData[team]['name']) == selectTeam:
                            found = True
                            selectTeam = team
                    if not found:
                        print("That's not a team name! Please check your spelling and try again!")

                confirm = ""
                while confirm != "yes" and confirm != "no":
                    confirm = str.lower(input("Are you sure? "))
    
                if confirm == "yes":
                    for i in range(maxPokemon):
                        pokemon = prevData[selectTeam]['pokemon_' + str(i + 1)]['pokemon']
                        pokemon = createPokemon(str.lower(pokemon))
                        pokemon.setName(prevData[selectTeam]['pokemon_' + str(i + 1)]['name'])
                        for x in range(4):
                            pokemonMove = str.lower(prevData[selectTeam]['pokemon_' + str(i + 1)]['move_' + str(x + 1)])
                            for move in pokemon.moves:
                                if str.lower(move.name) == pokemonMove:
                                    pokemon.addAvailMove(move)

                        playerPokemon.append(pokemon)
            else:
                break

    


if len(playerPokemon) == 0:
    print("List of Available Pokemon: ")
    for i in pokemonList:
        print(i)


    while len(playerPokemon) < maxPokemon:
        pokemonChoice = input("Choose your Pokemon! ")

        pokemonChoice = createPokemon(pokemonChoice)
        if pokemonChoice != 0:
            playerPokemon.append(pokemonChoice)
        else:
            print("An error occurred, please check your spelling")

    while not namesChosen:

        print("\nYour Pokemon are: ")
        for i in range(len(playerPokemon)):
            if playerPokemon[i].nickname == playerPokemon[i].name:
                print(playerPokemon[i].nickname)
            else:
                print(playerPokemon[i].nickname + " (" + playerPokemon[i].name + ")")

        rename = input("Would you like to rename any of your pokemon? (yes or no) ")
        if str.lower(rename) == "yes":
            renamePokemon = input("Which pokemon? (Please type number in order as listed above) ")
            if renamePokemon.isnumeric():
                renamePokemon = int(renamePokemon, 10) - 1
                if renamePokemon >= 0 and renamePokemon < maxPokemon:
                    newName = input("What will be it's new name? ")
                    if type(newName) == str:
                        playerPokemon[renamePokemon].setName(str.capitalize(newName))
                        displayNicks = True
                else:
                    print("Please make sure that the number is in range")
            else:
                print("Please make sure that you are only typing a number")
        elif str.lower(rename) == "no":
            namesChosen = True
        else:
            print("Please make sure you are either typing 'yes' or 'no'")

    for p in playerPokemon:

        idStatement = False
        for i in playerPokemon:
            if i.ident == p.ident:
                continue
            else:
                if str.lower(i.name) == str.lower(p.name) and str.lower(i.nickname) == str.lower(p.nickname):
                    idStatement = True
                else:
                    pass

        if idStatement:
            if p.name == p.nickname:
                print("\nMoves available for " + p.nickname + " (" + str(p.ident) + ")"+ ":")
            else:
                print("\nMoves available for " + p.nickname + " (" + p.name + ")" + " (" + str(p.ident) + ")"+ ":")
        else:
            if p.name == p.nickname:
                print("\nMoves available for " + p.nickname + ":")
            else:
                print("\nMoves available for " + p.nickname + " (" + p.name + ")" + ":")

        for i in p.moves:
            print(i.name)
        movesChosen = False
        while not movesChosen:
            moveChoice = str.lower(input("Choose a move: "))
            loopFlag = False

            for i in p.moves:
                if moveChoice == str.lower(i.name):
                    for x in p.availMoves:
                        if moveChoice == str.lower(x.name):
                            print("You already chose this move!")
                            loopFlag = True
                            break
                    if loopFlag:
                        break
                    p.addAvailMove(i)
                    if len(p.availMoves) == maxMoves:
                        movesChosen = True
                    break
                else:
                    if i == p.moves[len(p.moves) - 1]:
                        print("An error occurred, please check your spelling!")
           

    saveChoice = ""
    while saveChoice != "yes" and saveChoice != "no":
        saveChoice = str.lower(input("Would you like to save this team? "))
    if saveChoice == "yes":
        teamName = input("What would you like to call this team? ")
        teamKey = "team_" + str(dataLength + 1)
        newTeam = {
                'name': teamName,
                'pokemon_1': {
			        'name': playerPokemon[0].nickname,
			        'pokemon': playerPokemon[0].name,
			        'move_1': playerPokemon[0].availMoves[0].name,
			        'move_2': playerPokemon[0].availMoves[1].name,
			        'move_3': playerPokemon[0].availMoves[2].name,
			        'move_4': playerPokemon[0].availMoves[3].name
		        },
		        'pokemon_2': {
			        'name': playerPokemon[1].nickname,
			        'pokemon': playerPokemon[1].name,
			        'move_1': playerPokemon[1].availMoves[0].name,
			        'move_2': playerPokemon[1].availMoves[1].name,
			        'move_3': playerPokemon[1].availMoves[2].name,
			        'move_4': playerPokemon[1].availMoves[3].name
		        },
		        'pokemon_3': {
			        'name': playerPokemon[2].nickname,
			        'pokemon': playerPokemon[2].name,
			        'move_1': playerPokemon[2].availMoves[0].name,
			        'move_2': playerPokemon[2].availMoves[1].name,
			        'move_3': playerPokemon[2].availMoves[2].name,
			        'move_4': playerPokemon[2].availMoves[3].name
		        }
            }
        prevData[teamKey] = newTeam

        with open('teams.json', 'w') as f:
            json.dump(prevData, f)
else:
    print("\nYour Pokemon are: ")

    for p in playerPokemon:
        idStatement = False
        for i in playerPokemon:
            if i.ident == p.ident:
                continue
            else:
                if str.lower(i.name) == str.lower(p.name) and str.lower(i.nickname) == str.lower(p.nickname):
                    idStatement = True
                else:
                    pass

        if idStatement:
            if p.name == p.nickname:
                print(p.nickname + " (" + str(p.ident) + ")")
            else:
                print(p.nickname + " (" + p.name + ")" + " (" + str(p.ident) + ")")
        else:
            if p.name == p.nickname:
                print(p.nickname)
            else:
                print(p.nickname + " (" + p.name + ")")



while len(enemyPokemon) < maxPokemon:
    randomChoice = random.randint(0, len(pokemonList) - 1)
    enemyPokemon.append(createPokemon(pokemonList[randomChoice]))

for i in range(maxPokemon):
    while True:
        loopFlag = False
        randomChoice = random.randint(0, len(enemyPokemon[i].moves) - 1)
        randomChoice = enemyPokemon[i].moves[randomChoice]

        if len(enemyPokemon[i].availMoves) > 0:
            for chosenMove in enemyPokemon[i].availMoves:
                if chosenMove == randomChoice:
                    loopFlag = True
            if loopFlag == False:
                enemyPokemon[i].addAvailMove(randomChoice)
        else:
            enemyPokemon[i].addAvailMove(randomChoice)
        if len(enemyPokemon[i].availMoves) == 4:
            break


def switch(dead):
    popFlag = False
    def switchInput():
        switchChoice = "placeholder"
        while not switchChoice.isnumeric() and str.lower(switchChoice) != "none":
            if dead:
                switchChoice = input("Which Pokemon do you want to switch to? Type number of pokemon starting from 1.\nIgnore any numbers next to names, they are only for reference. ")
            else:
                switchChoice = input("Which Pokemon do you want to switch to? Type number of pokemon starting from 1 and 'none' if you wish to go back.\nIgnore numbers next to names, they are only for reference. ")
            if not switchChoice.isnumeric():
                if (not switchChoice == "none") or dead:
                    print("Please check your spelling! ")
        if switchChoice.isnumeric():
            switchChoice = int(switchChoice, 10) - 1

            if playerPokemon[switchChoice] == playerPokemon[0] and not popFlag:
                print("You already have that Pokemon out!")
                switchInput()

            playerPokemon[0].effect.switchReset()
            playerPokemon[0], playerPokemon[switchChoice] = playerPokemon[switchChoice], playerPokemon[0]
            return True
        else:
            return False


    for i in range(len(playerPokemon) - 1):
        if playerPokemon[i].hp <= 0:
            playerPokemon.pop(i)
            popFlag = True

    print("\nAvailable Pokemon to switch to:")
    for i in playerPokemon:
        idStatement = False
        for p in playerPokemon:
            if p.ident == i.ident:
                continue
            else:
                if str.lower(p.name) == str.lower(i.name) and str.lower(p.nickname) == str.lower(i.nickname):
                    idStatement = True

        if idStatement:
            if i.name == i.nickname:
                print(i.nickname + " (" + str(i.ident) + ")")
            else:
                print(i.nickname + + " (" + i.name + ")" + " (" + str(i.ident) + ")")
        else:
            if i.name == i.nickname:
                print(i.nickname)
            else:
                print(i.nickname + " (" + i.name + ")")

    return switchInput()


def addStatusCondition(user, foe, move):
    if str.lower(move.cata) == "status":
        enemyEff = move.eff
        playerEff = move.pEff
        playerStatEff = move.pstEff
        
        if not foe.isAffected:
            for i in move.eff.typeImm:
                if str.lower(i) == str.lower(foe.ty):
                    return " was immune to ", str.lower(enemyEff.name), True, foe
                if str.lower(i) == str.lower(foe.ty2):
                    return " was immune to ", str.lower(enemyEff.name), True, foe
            if str.lower(enemyEff.name) != "none":
                foe.effect = enemyEff
                foe.isAffected = True
                return " was inflicted with ", str.lower(enemyEff.name), True, foe
                
        if not user.isAffected:
            for i in move.pEff.typeImm:
                if str.lower(i) == str.lower(user.ty):
                    return " was immune to ", str.lower(playerEff.name), True, user
                if str.lower(i) == str.lower(user.ty2):
                    return " was immune to ", str.lower(playerEff.name), True, user
            if str.lower(playerEff.name) != "none" and str.lower(playerEff.name) != "sleep" and str.lower(playerEff.affected) != "self":
                user.effect = playerEff
                user.isAffected = True
                return " was inflicted with ", str.lower(playerEff.name), True, user

        if str.lower(playerEff.name) == "sleep" and str.lower(playerEff.affected) == "self":
            if str.lower(user.effect.name) != "sleep":
                user.effect = playerEff
                user.isAffected = True
                user.hp = user.maxHp
                user.turns = 2

                if user is playerPokemon[0]:
                    print("Your " + playerPokemon[0].nickname + " has healed!")
                    print("Your " + playerPokemon[0].nickname + " now has " + str(round(playerPokemon[0].hp, 2)) + " HP!")
                elif user is enemyPokemon[0]:
                    print("The enemy's " + enemyPokemon[0].nickname + " has healed!")
                    print("The enemy's " + enemyPokemon[0].nickname + " now has " + str(round(enemyPokemon[0].hp, 2)) + " HP!")
                return " was inflicted with ", str.lower(playerEff.name), True, user


        if str.lower(playerEff.name) != "none" and str.lower(user.effect.name) != "none":
            return " already has ", "an effect", True, user
        if str.lower(enemyEff.name) != "none" and str.lower(foe.effect.name) != "none":
            return " already has ", "an effect", True, foe

        if str.lower(playerStatEff) == "heal":
            healAmount = move.pstEffAmount * user.maxHp
            user.hp += healAmount
            if user.hp > user.maxHp:
                user.hp = user.maxHp

            if user is playerPokemon[0]:
                print("Your " + playerPokemon[0].nickname + " has healed!")
                print("Your " + playerPokemon[0].nickname + " now has " + str(round(playerPokemon[0].hp, 2)) + " HP!")
            elif user is enemyPokemon[0]:
                print("The enemy's " + enemyPokemon[0].nickname + " has healed!")
                print("The enemy's " + enemyPokemon[0].nickname + " now has " + str(round(enemyPokemon[0].hp, 2)) + " HP!")


        return "", "", False
    else:
        eff = move.eff
        accuracy = move.accCalc(user, foe, True)
        if not accuracy:
            return "", "", False

        if str.lower(eff.affected) == "enemy":
            if not foe.isAffected:
                for i in move.eff.typeImm:
                    if str.lower(i) == str.lower(foe.ty):
                        return " was immune to ", str.lower(eff.name), True, foe
                    if str.lower(i) == str.lower(foe.ty2):
                        return " was immune to ", str.lower(eff.name), True, foe
                if str.lower(eff.name) != "none":
                    foe.effect = eff
                    foe.isAffected = True
                    return " was inflicted with ", str.lower(eff.name), True, foe
                return "", "", False
            return " already has ", "an effect", True, foe

        elif str.lower(eff.affected) == "self":
            if not user.isAffected:
                for i in move.eff.typeImm:
                    if str.lower(i) == str.lower(user.ty):
                        return " was immune to ", str.lower(eff.name), True, user
                    if str.lower(i) == str.lower(user.ty2):
                        return " was immune to ", str.lower(eff.name), True, user
                if str.lower(eff.name) != "none":
                    user.effect = eff
                    user.isAffected = True
                    return " was inflicted with ", str.lower(eff.name), True, user
                return "", "", False
            return " already has ", "an effect", True, user
        else:
            return "", "", False





fightChoice = 0
winner = False



while winner != True:
    time.sleep(1)

    msg = ""
    enemySwitch = False
    switched = False
    idStatement = False
    for i in playerPokemon:
        if i.ident == playerPokemon[0].ident:
            continue
        else:
            if str.lower(i.nickname) == str.lower(playerPokemon[0].nickname) and str.lower(i.name) == str.lower(playerPokemon[0].name):
                idStatement = True


    pokemonNameDisplay = "\nYour pokemon is " + playerPokemon[0].nickname
    if playerPokemon[0].nickname != playerPokemon[0].name:
        pokemonNameDisplay += " (" + playerPokemon[0].name + ")"
    if idStatement:
        pokemonNameDisplay += " (" + str(playerPokemon[0].ident) + ")"

    print(pokemonNameDisplay)
    print("Your opponent has a " + enemyPokemon[0].name)
    print("\nTime to fight!")

    def pickAction():
        while True:
            fightChoice = str.lower(input("\nWould you like to Fight or Switch pokemon?(type 'fight' or 'switch') "))

            if str.lower(fightChoice) == "fight":
                return str.lower(fightChoice)
            elif str.lower(fightChoice) == "switch":
                return str.lower("switch")
            else:
                print("An error occurred, please check your spelling!")
            
    fightChoice = pickAction()


    if str.lower(fightChoice) == "switch":
        switched = switch(False)
        if not switched:
            continue

    if str.lower(fightChoice) == "fight":
        print("Please choose a move to use from this list of available moves:")
        for z in playerPokemon[0].availMoves:
            print(z.name)
        while True:
            loopFlag = False
            attackChoice = str.lower(input("Move: "))
        
            for move in playerPokemon[0].availMoves:
                if str.lower(move.name) == attackChoice:
                    playerPokemon[0].moveChoice.append(move)
                    loopFlag = True
                    break
                else:
                    if move == playerPokemon[0].availMoves[len(playerPokemon[0].availMoves) - 1]:
                        print("Please check your spelling and try again.")
            if loopFlag == True:
                break

    enemyPokemon[0].moveChoice.append(enemyPokemon[0].availMoves[random.randint(0, len(enemyPokemon[0].availMoves) - 1)])
 
    # reset priority from last attack
    playerPokemon[0].priority = 0
    enemyPokemon[0].priority = 0


    # set priority to new attack (last move in moveChoice)
    if not switched:
        playerPokemon[0].priority = playerPokemon[0].moveChoice[len(playerPokemon[0].moveChoice) - 1].priority
    else:
        playerPokemon[0].priority = 0

    if not enemySwitch:
        enemyPokemon[0].priority = enemyPokemon[0].moveChoice[len(enemyPokemon[0].moveChoice) - 1].priority
    else:
        enemyPokemon[0].priority = 0


    if playerPokemon[0].priority == enemyPokemon[0].priority:
        # Non priority moves
        if switched:
            first = enemyPokemon
            second = playerPokemon
        elif playerPokemon[0].speed > enemyPokemon[0].speed:
            first = playerPokemon
            second = enemyPokemon
        elif playerPokemon[0].speed < enemyPokemon[0].speed:
            first = enemyPokemon
            second = playerPokemon
        elif playerPokemon[0].speed == enemyPokemon[0].speed:
            first = random.randint(0,1)
            if first == 0:
                first = playerPokemon
                second = enemyPokemon
            else:
                first = enemyPokemon
                second = playerPokemon
    else:
        # priority moves like quick attack
        if switched:
            first = enemyPokemon
            second = playerPokemon
        else:
            if playerPokemon[0].priority > enemyPokemon[0].priority:
                first = playerPokemon
                second = enemyPokemon
            elif playerPokemon[0].priority < enemyPokemon[0].priority:
                first = enemyPokemon
                second = playerPokemon

    def fight(firstPlayer, secondPlayer):
        global switched

        dmg, hit  = firstPlayer[0].moveChoice[len(firstPlayer[0].moveChoice) - 1].dmgCalc(firstPlayer[0], secondPlayer[0])
        dmg = round(dmg, 2)

        if not switched:
            secondDmg, hit2 = secondPlayer[0].moveChoice[len(secondPlayer[0].moveChoice) - 1].dmgCalc(secondPlayer[0], firstPlayer[0])
            secondDmg = round(secondDmg, 2)

        if firstPlayer[0] == playerPokemon[0]:
            firstPronoun = "Your "
            secondPronoun = "The enemy's "
            firstPlayerWin = "You win!"
            secondPlayerWin = "The enemy has won!"
        else:
            firstPronoun = "The enemy's "
            secondPronoun = "Your "
            firstPlayerWin = "The enemy has won!"
            secondPlayerWin = "You win!"


        firstPlayer[0].effect.clearState(firstPlayer[0])
        msg = firstPlayer[0].effect.update(firstPlayer[0], True, 1)
        if not msg[0]:
            print(firstPronoun + firstPlayer[0].nickname + msg[2] + "!")


        if firstPlayer[0].canMove:
            deadPokemon = 0
            print("\n" + firstPronoun + firstPlayer[0].nickname + " used " + firstPlayer[0].moveChoice[len(firstPlayer[0].moveChoice) - 1].name + "!")
            if not hit:
                print(firstPronoun + firstPlayer[0].nickname + " missed!")

            # Facade dmg addon
            if str.lower(firstPlayer[0].moveChoice[-1].name) == "facade" and str.lower(firstPlayer[0].effect.name) != "none":
                if str.lower(firstPlayer[0].effect.name) == "poison" or str.lower(firstPlayer[0].effect.name) == "badly poisoned" or str.lower(firstPlayer[0].effect.name) == "paralysis" or str.lower(firstPlayer[0].effect.name) == "burn":
                    dmg = (2 * dmg) - 2 # Im adding this in after all the dmg code has been done. This is the calculated factor by which the total damage increases if the move damage doubles
                    if str.lower(firstPlayer[0].effect.name) == "burn":
                        dmg *= 2 # cancel out the burn effect of halving dmg (facade is a physical move)

            # venoshock dmg addon
            if str.lower(firstPlayer[0].moveChoice[-1].name) == "venoshock" and (str.lower(secondPlayer[0].effect.name) == "poison" or str.lower(secondPlayer[0].effect.name) == "badly poisoned"):
                dmg = (2 * dmg) - 2

            if str.lower(firstPlayer[0].moveChoice[-1].cata) != "status":
                print(firstPronoun + firstPlayer[0].nickname + " did " + str(dmg) + " damage!")
            secondPlayer[0].dealDmg(dmg, 0)
            if secondPlayer[0].hp < 0:
                secondPlayer[0].setHP(0)

            if str.lower(firstPlayer[0].moveChoice[- 1].cata) != "status":
                print(secondPronoun + secondPlayer[0].nickname + " now has " + str(round(secondPlayer[0].hp, 2)) + " HP!")

            if secondPlayer[0].hp == 0:
                print(secondPronoun + secondPlayer[0].nickname + " has fainted!")

                for mon in secondPlayer:
                    if mon.hp <= 0:
                        deadPokemon += 1
                if deadPokemon == len(secondPlayer):
                    print(firstPlayerWin)
                    return True

                if secondPlayer == playerPokemon:
                    switched = switch(True)
                elif secondPlayer == enemyPokemon:
                    enemyPokemon.pop(0)
                return False
            if hit:
                msg = addStatusCondition(firstPlayer[0], secondPlayer[0], firstPlayer[0].moveChoice[len(firstPlayer[0].moveChoice) - 1])
                if msg[2]:
                    if msg[3] is firstPlayer[0]:
                        print(firstPronoun + firstPlayer[0].nickname + msg[0] + msg[1])
                    elif msg[3] is secondPlayer[0]:
                        print(secondPronoun + secondPlayer[0].nickname + msg[0] + msg[1])
                    else:
                        print("Check if addStatusCondition is returning pokemon object at index 3") #????

            time.sleep(1)
        else:
            print("\n" + firstPronoun + firstPlayer[0].nickname + " is " + firstPlayer[0].effect.msg + "!")

        # for paralyze and frozen so you are not forever stuck
        firstPlayer[0].effect.clearState(firstPlayer[0])
        secondPlayer[0].effect.clearState(secondPlayer[0])

        # updates states of pokemon but not dmg
        msg = secondPlayer[0].effect.update(secondPlayer[0], True, 2)
        if not msg[0]:
            print("\n" + secondPronoun + secondPlayer[0].nickname + msg[2] + "!")

        if secondPlayer[0].canMove:
            if not switched:
                deadPokemon = 0
                print("\n" + secondPronoun + secondPlayer[0].nickname + " used " + secondPlayer[0].moveChoice[len(secondPlayer[0].moveChoice) - 1].name + "!")
                if not hit2:
                    print(secondPronoun + secondPlayer[0].nickname + " missed!")

                # Facade dmg addon
                if str.lower(secondPlayer[0].moveChoice[-1].name) == "facade" and str.lower(secondPlayer[0].effect.name) != "none":
                    if str.lower(secondPlayer[0].effect.name) == "poison" or str.lower(secondPlayer[0].effect.name) == "badly poisoned" or str.lower(secondPlayer[0].effect.name) == "paralysis" or str.lower(secondPlayer[0].effect.name) == "burn":
                        secondDmg = (2 * secondDmg) - 2 # Im adding this in after all the dmg code has been done. This is the calculated factor by which the total damage increases if the move damage doubles
                        if str.lower(secondPlayer[0].effect.name) == "burn":
                            secondDmg *= 2 # cancel out the burn effect of halving dmg (facade is a physical move)
                            

                # venoshock dmg addon
                if str.lower(secondPlayer[0].moveChoice[-1].name) == "venoshock" and (str.lower(firstPlayer[0].effect.name) == "poison" or str.lower(firstPlayer[0].effect.name) == "badly poisoned"):
                    secondDmg = (2 * secondDmg) - 2

                if str.lower(secondPlayer[0].moveChoice[-1].cata) != "status":
                    print(secondPronoun + secondPlayer[0].nickname + " did " + str(secondDmg) + " damage!")
                firstPlayer[0].dealDmg(secondDmg, 0)
                if firstPlayer[0].hp < 0:
                    firstPlayer[0].setHP(0)

                if str.lower(secondPlayer[0].moveChoice[- 1].cata) != "status":
                    print(firstPronoun + firstPlayer[0].nickname + " now has " + str(round(firstPlayer[0].hp, 2)) + " HP!")
                if firstPlayer[0].hp == 0:
                    print(firstPronoun + firstPlayer[0].nickname + " has fainted!")
        
                    for mon in firstPlayer:
                        if mon.hp <= 0:
                            deadPokemon += 1
                    if deadPokemon == len(firstPlayer):
                        print(secondPlayerWin)
                        return True

                    if firstPlayer == playerPokemon:
                        switched = switch(True)
                    elif firstPlayer == enemyPokemon:
                        enemyPokemon.pop(0)
                    return False
                if hit2:
                    msg = addStatusCondition(secondPlayer[0], firstPlayer[0], secondPlayer[0].moveChoice[len(secondPlayer[0].moveChoice) - 1])
                    if msg[2]:
                        if msg[3] is firstPlayer[0]:
                            print(firstPronoun + firstPlayer[0].nickname + msg[0] + msg[1])
                        elif msg[3] is secondPlayer[0]:
                            print(secondPronoun + secondPlayer[0].nickname + msg[0] + msg[1])
                        else:
                            print("Check if addStatusCondition is returning pokemon object at index 3")
                time.sleep(1)
        else: 
            print("\n" + secondPronoun + secondPlayer[0].nickname + " is " + secondPlayer[0].effect.msg + "!") 

        
        secondPlayer[0].effect.clearState(secondPlayer[0])


        msg = secondPlayer[0].effect.update(secondPlayer[0], False, 2)
        if msg[1] > 0:
            print(secondPronoun + secondPlayer[0].nickname + " took " + str(msg[1]) + " " + str.lower(secondPlayer[0].effect.name) + " damage!")


        msg = firstPlayer[0].effect.update(firstPlayer[0], False, 1)
        if msg[1] > 0:
            print(firstPronoun + firstPlayer[0].nickname + " took " + str(round(msg[1],2)) + " " + str.lower(firstPlayer[0].effect.name) + " damage!")


        if firstPlayer[0].hp <= 0:
            print(firstPronoun + firstPlayer[0].nickname + " has fainted!")
        
            for mon in firstPlayer:
                if mon.hp <= 0:
                    deadPokemon += 1
            if deadPokemon == len(firstPlayer):
                print(secondPlayerWin)
                return True

            if firstPlayer == playerPokemon:
                switched = switch(True)
            elif firstPlayer == enemyPokemon:
                enemyPokemon.pop(0)
            return False

        if secondPlayer[0].hp <= 0:
            print(secondPronoun + secondPlayer[0].nickname + " has fainted!")

            for mon in secondPlayer:
                if mon.hp <= 0:
                    deadPokemon += 1
            if deadPokemon == len(secondPlayer):
                print(firstPlayerWin)
                return True

            if secondPlayer == playerPokemon:
                switched = switch(True)
            elif secondPlayer == enemyPokemon:
                enemyPokemon.pop(0)
            return False

        return False

    winner = fight(first,second)
