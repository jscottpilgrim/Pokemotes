import libs
import pokemonCommandLibs
from downloadEmote import NoEmoteException
from random import randint

def generatePokemon(text, username):
    params = text.split()
    ret = {}
    ret['Username'] = username
    ret['Gender'] = str(randint(0, 2))
    ret['Moves Learnable'] = {}
    movesLearnableCount = randint(10, 20)
    for i in range(1,movesLearnableCount):
        ret['Moves Learnable'][i] = {}
        ret['Moves Learnable'][i]["'level'"] = str(randint(1,60))
        ret['Moves Learnable'][i]["'move'"] = str(randint(1, pokemonCommandLibs.attackCount))
    ret['Image Link'] = params[0]
    ret['Name'] = params[0]
    if len(params) >= 3:
        ret['Type1'] = str(pokemonCommandLibs.types[params[1].lower()])
        ret['Type2'] = str(pokemonCommandLibs.types[params[2].lower()])
        if len(params) >= 4:
            if int(params[3]) < pokemonCommandLibs.abilityCount:
                ret['Ability'] = params[3]
            else:
                ret['Ability'] = str(randint(1, pokemonCommandLibs.abilityCount))
            if len(params) >= 8:
                # add check for attacks out of range
                ret['Attack1'] = params[4]
                ret['Attack2'] = params[5]
                ret['Attack3'] = params[6]
                ret['Attack4'] = params[7]
            elif len(params) >= 7:
                ret['Attack1'] = params[4]
                ret['Attack2'] = params[5]
                ret['Attack3'] = params[6]
                ret['Attack4'] = str(randint(1, pokemonCommandLibs.attackCount))
            elif len(params) >= 6:
                ret['Attack1'] = params[4]
                ret['Attack2'] = params[5]
                ret['Attack3'] = str(randint(1, pokemonCommandLibs.attackCount))
                ret['Attack4'] = str(randint(1, pokemonCommandLibs.attackCount))
            elif len(params) >= 5:
                ret['Attack1'] = params[4]
                ret['Attack2'] = str(randint(1, pokemonCommandLibs.attackCount))
                ret['Attack3'] = str(randint(1, pokemonCommandLibs.attackCount))
                ret['Attack4'] = str(randint(1, pokemonCommandLibs.attackCount))
            else:
                ret['Attack1'] = str(randint(1, pokemonCommandLibs.attackCount))
                ret['Attack2'] = str(randint(1, pokemonCommandLibs.attackCount))
                ret['Attack3'] = str(randint(1, pokemonCommandLibs.attackCount))
                ret['Attack4'] = str(randint(1, pokemonCommandLibs.attackCount))
        else:
            ret['Attack1'] = str(randint(1, pokemonCommandLibs.attackCount))
            ret['Attack2'] = str(randint(1, pokemonCommandLibs.attackCount))
            ret['Attack3'] = str(randint(1, pokemonCommandLibs.attackCount))
            ret['Attack4'] = str(randint(1, pokemonCommandLibs.attackCount))
            ret['Ability'] = str(randint(1, pokemonCommandLibs.abilityCount))
    elif len(params) == 2:
        ret['Type1'] = str(pokemonCommandLibs.types[params[1]])
        ret['Type2'] = str(ret['Type1'])
        ret['Attack1'] = str(randint(1, pokemonCommandLibs.attackCount))
        ret['Attack2'] = str(randint(1, pokemonCommandLibs.attackCount))
        ret['Attack3'] = str(randint(1, pokemonCommandLibs.attackCount))
        ret['Attack4'] = str(randint(1, pokemonCommandLibs.attackCount))
        ret['Ability'] = str(randint(1, pokemonCommandLibs.abilityCount))
    elif len(params) == 1:
        ret['Type1'] = str(randint(0, pokemonCommandLibs.typesCount - 1))
        ret['Type2'] = str(randint(0, pokemonCommandLibs.typesCount - 1))
        ret['Attack1'] = str(randint(1, pokemonCommandLibs.attackCount))
        ret['Attack2'] = str(randint(1, pokemonCommandLibs.attackCount))
        ret['Attack3'] = str(randint(1, pokemonCommandLibs.attackCount))
        ret['Attack4'] = str(randint(1, pokemonCommandLibs.attackCount))
        ret['Ability'] = str(randint(1, pokemonCommandLibs.abilityCount))
    return ret


def pokemonCommand(username, sock, queue, text, validators):
    jsonPokemon = generatePokemon(text, username)
    error, errorMessage = validatePokemon(jsonPokemon, validators, queue)
    if (error):
        libs.chat(sock, errorMessage)
        return
    try:
        formattedInput = pokemonCommandLibs.formatInput(jsonPokemon)
        queue.put([jsonPokemon, formattedInput.encode("ascii", "ignore")])
        libs.chat(sock, text + " has been added to the queue (queue position: " + str(queue.qsize()) + ") (" + str(pokemonCommandLibs.types2[int(jsonPokemon["Type1"])]) + ", " + str(pokemonCommandLibs.types2[int(jsonPokemon["Type2"])]) + ")")
    except NoEmoteException:
        libs.chat(sock, "That does not appear to be a valid Twitch or FFZ emote :(")

def validatePokemon(jsonPokemon, validators, queue):
    for validatorName, validator in validators.items():
        error, errorMessage = validator.validate(jsonPokemon, queue)
        if error:
            return True, errorMessage
    return False, None
