import random

class Move:
    def __init__(self, name, cata, attType, acc, dmg, eff, effAcc, priority):
        self.name = name
        self.cata = cata
        self.attType = attType
        self.acc = acc
        self.dmg = dmg
        self.eff = eff
        self.effAcc = effAcc
        self.priority = priority

    def typeBonus(self, enemyType, enemyType2):

        # type bonuses dictionary
        type_bonus_dict = {
            "Normal": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, .5, 0, 1, 1, .5, 1],
            "Fighting": [2, 1, .5, .5, 1, 1, 1, 1, 2, 1, .5, .5, 2, 0, 1, 2, 2, .5],
            "Flying": [1, 2, 1, 1, 1, 1, 2, .5, 1, 1, 2, .5, 1, 1, 1, .5, 1],
            "Poison": [1, 1, 1, .5, 1, 1, 2, 1, 1, .5, 1, 1, .5, .5, 1, 1, 0, 2],
            "Fire": [1, 1, 1, 1, .5, .5, 2, 1, 2, 1, 1, 2, .5, 1, .5, 1, 2, 1],
            "Water": [1, 1, 1, 1, 2, .5, .5, 1, 1, 2, 1, 1, 2, 1, .5, 1, 1, 1],
            "Grass": [1, 1.5, .5, .5, 2, .5, 1, 1, 2, 1, .5, 2, 1, .5, 1, .5, 1],
            "Electric": [1, 1, 2, 1, 1, 2, .5, .5, 1, 0, 1, 1, 1, 1, .5, 1, 1, 1],
            "Ice": [1, 1, 2, 1, .5, .5, 2, 1, .5, 2, 1, 1, 1, 1, 2, 1, .5, 1],
            "Ground": [1, 1, 0, 2, 2, 1, .5, 2, 1, 1, 1, .5, 2, 1, 1, 1, 2, 1],
            "Psychic": [1, 2, 1, 2, 1, 1, 1, 1, 1, 1, .5, 1, 1, 1, 1, 0, .5, 1],
            "Bug": [1, .5, .5, .5, .5, 1, 2, 1, 1, 1, 2, 1, 1, .5, 1, 2, .5, .5],
            "Rock": [1, .5, 2, 1, 2, 1, 1, 1, 2, .5, 1, 2, 1, 1, 1, 1, .5, 1],
            "Ghost": [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, .5, 1, 1],
            "Dragon": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, .5, 0],
            "Dark": [1, .5, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, .5, 1, .5],
            "Steel": [1, 1, 1, 1, .5, .5, 1, .5, 2, 1, 1, 1, 2, 1, 1, 1, .5, 2],
            "Fairy": [1, 2, 1, .5, .5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, .5, 1]
        }

        # dictionary for indices of each type
        type_index_dict = {
        "Normal": 0,
        "Fighting": 1,
        "Flying": 2,
        "Poison": 3,
        "Fire": 4,
        "Water": 5,
        "Grass": 6,
        "Electric": 7,
        "Ice": 8,
        "Ground": 9,
        "Psychic": 10,
        "Bug": 11,
        "Rock": 12,
        "Ghost": 13,
        "Dragon": 14,
        "Dark": 15,
        "Steel": 16,
        "Fairy": 17
    }
    
         # look up the indices of the types
        enemy_type_index = type_index_dict[enemyType]


        if enemyType2 == "None":
            effectiveness = type_bonus_dict[self.attType][enemy_type_index]
        else:
            enemy2_type_index = type_index_dict[enemyType2]
            effectiveness = type_bonus_dict[self.attType][enemy_type_index] * type_bonus_dict[self.attType][enemy2_type_index]

        return effectiveness



    def accCalc(self, user, enemy, effect):
        if not effect:
            accuracy = (self.acc * user.acc / enemy.evasion) * 100
            # if the random number is above the accuracy then it misses and returns no damage and if it hit
            if random.randint(1, 100) > accuracy:
                return 0, False
            else:
                return 0, True
        else:
            if random.randint(1, 100) > self.effAcc:
                return False
            else:
                return True


    def dmgCalc(self, player, enemy):
        
        accuracy = self.accCalc(player, enemy, False)
        if not accuracy[1]:
            return accuracy


        def dmgForm(att, spAtt, defense, specialDef, crit, tyBonus, stab, burn): # Gen 5 onward
            randDmg = random.randint(85,100) / 100 
            if str.lower(self.cata) == "physical":
                return (((((((2 * 50) / 5) + 2) * self.dmg * (att / defense)) / 50) + 2) * crit * tyBonus * stab * burn * randDmg)
            elif str.lower(self.cata) == "special":
                return (((((((2 * 50) / 5) + 2) * self.dmg * (spAtt / specialDef)) / 50) + 2) * crit * tyBonus * stab * randDmg)
            else:
                return 0


        crit = random.randint(1,100)

        if crit <= 6.25:
            crit = 1.5
        else:
            crit = 1

        burn = 1

        if str.lower(player.effect.name) == "burn":
            if str.lower(self.cata) == "physical":
                burn = 0.5
            else:
                burn = 1
        
        if str.lower(self.attType) == str.lower(player.ty) or str.lower(self.attType) == str.lower(player.ty2):
            stab = 1.5
        else: 
            stab = 1

        tyBonus = self.typeBonus(enemy.ty, enemy.ty2)


        return dmgForm(player.att, player.spAtt, enemy.defense, enemy.spDef, crit, tyBonus, stab, burn), True


class StatusMove(Move):
    # name, catagory, attack type, accuracy, enemy effect, enem stat effect, player eff, p stat eff, who is affected, priority
    def __init__(self, name, cata, attType, acc, eff, stEff, pEff, pstEff, pstEffAmount, priority):
        self.name = name
        self.cata = cata
        self.attType = attType
        self.acc = acc
        self.eff = eff
        self.stEff = stEff
        self.pEff = pEff
        self.pstEff = pstEff
        self.pstEffAmount = pstEffAmount
        self.priority = priority


class StatusCondition():
    def __init__(self, name, reset, typeImm, dmg, affected, msg):
        self.name = name
        self.reset = reset
        self.typeImm = typeImm
        self.msg = msg
        self.affected = affected
        self.dmg = dmg
        self.increment = 1/16

    def update(self, pokemon, first, player):

        if not first:
            if str.lower(self.name) == "burn":
                dmg = pokemon.maxHp * self.dmg
                pokemon.hp -= dmg
                return True, dmg, ""
            elif str.lower(self.name) == "poison":
                dmg = pokemon.maxHp * self.dmg
                pokemon.hp -= dmg
                return True, dmg, ""
            elif str.lower(self.name) == "badly poisoned":
                dmg = pokemon.maxHp * self.dmg
                pokemon.hp -= dmg
                self.dmg += self.increment
                return True, dmg, ""
        if str.lower(self.name) == "freeze" and first:
            pokemon.canMove = False
            frozen = random.randint(1, 100)
            if frozen <= 20:
                pokemon.canMove = True
                none = StatusCondition("None", False, [], 0, "N/A", "N/A")
                pokemon.effect = none
                pokemon.isAffected = False
                return False, 0, " thawed"
            return True, 0, ""
        elif str.lower(self.name) == "paralysis" and first:
            pokemon.speed = pokemon.speed * .5
            paralyze = random.randint(1, 100)
            if paralyze <= 25:
                pokemon.canMove = False
            return True, 0, ""
        elif str.lower(self.name) == "sleep" and first:
            if pokemon.turns == 0:
                pokemon.canMove = True
                pokemon.turns = -1
                none = StatusCondition("None", False, [], 0, "N/A", "N/A")
                pokemon.effect = none
                pokemon.isAffected = False
                
                return False, 0, " woke up"
            elif pokemon.turns != 0:
      
                if pokemon.turns == -1:

                    if str.lower(self.affected) != "self":
                        pokemon.turns = random.randint(1,3)

                pokemon.turns -= 1

                pokemon.canMove = False
                return True, 0, ""
            else:
                print("idk wtf just happened... pokemon.turns not 0 or non 0")
                return True, 0, ""
        return True, 0, ""
                

       
    def clearState(self, pokemon):
        if str.lower(self.name) != "sleep":
            pokemon.canMove = True


    def switchReset(self):
        if self.reset:
            self.dmg = self.increment


class Pokemon():
    def __init__(self, name, maxHp, att, spAtt, defense, spDef, speed, ty, ty2, effect, ident, priority):
        self.name = name
        self.nickname = name
        self.moves = []
        self.maxHp = maxHp
        self.hp = maxHp
        self.att = att
        self.attStage = 0
        self.spAtt = spAtt
        self.spAttStage = 0
        self.defense = defense
        self.defStage = 0
        self.spDef = spDef
        self.spDefStage = 0
        self.speed = speed
        self.speedStage = 0
        self.evasion = 100
        self.evasionStage = 0
        self.acc = 100
        self.accStage = 0
        self.ty = ty
        self.ty2 = ty2
        self.availMoves = []
        self.moveChoice = []
        self.effect = effect
        self.isAffected = False
        self.volEffect = ""
        self.canMove = True
        self.turns = -1
        self.ident = ident
        self.priority = priority

    # *arg is a variable number of arguments
    def addMoves(self, *move):
        # for item in move list, append item 
        for i in move:
            self.moves.append(i)

    def addAvailMove(self, move):
        self.availMoves.append(move)
        

    def setHP(self, newHealth):
        self.hp = newHealth

    def dealDmg(self, dmg, heal):
        self.hp -= dmg
        self.hp += heal
        self.hp = self.hp

    def setName(self, newName):
        self.nickname = newName
