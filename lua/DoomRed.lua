PokemonWriter = require 'PokemonWriter'
PokemonChanges = require 'PokemonChanges'
container = require 'UsedPokemonContainer'
cfg = require 'cfg'
saveload = require 'saveload'

function tablesMatch(a, b)
    if #a ~= #b then
        return false
    else
        for i=1,#a do
            if a[i] ~= b[i] then
                return false
            end
        end
        return true
    end
end

function findBox()
    firstBoxPokemonDat = require 'savedFirstBox'
    secondBoxPokemonDat = require 'savedFirstBox2'
    if type(firstBoxPokemonDat) ~= "table" or type(secondBoxPokemonDat) ~= "table" then
        cfg.setBoxSearched(false)
    else
        utils = require 'utils'
        --find track pokemon
        local searchPointer = 0x20292DC
        print('Searching for box first')
        while searchPointer < 0x2040000 do
            local growth, attacks, ev, misc = utils.readPokemon(searchPointer)
            if tablesMatch(misc, firstBoxPokemonDat) then
                print('match')
                print(searchPointer)
                cfg.setBox1Start(searchPointer)
                break
            end
            searchPointer = searchPointer + 1
            print(searchPointer)
        end
        print('Searching for box second')
        while searchPointer < 0x2040000 do
            local growth, attacks, ev, misc = utils.readPokemon(searchPointer)
            if tablesMatch(misc, secondBoxPokemonDat) then
                print('match')
                print(searchPointer)
                cfg.setBox1Second(searchPointer)
                break
            end
            searchPointer = searchPointer + 1
            print(searchPointer)
        end
        print('Search complete.')
        cfg.setBoxSearched(true)
    end
end
findBox()

boxmon = {}
function storeBoxPokemon()
    utils = require 'utils'
    for i=0,cfg.boxPositionCount-1 do
        local pointer = cfg.box1start+i*cfg.boxPokemonDataSize
        local id = container.getPokemonIdAtPosition(pointer)
        local trackgrowth, trackattacks, trackev, trackmisc = utils.readPokemon(pointer)
        
        if id ~= 0 then
            --add growth to table
            table.insert(boxmon, trackgrowth)
        end
    end
end
storeBoxPokemon()

function findAllBoxMons()
    utils = require 'utils'
    for i=1,#boxmon do
        --find track pokemon
        local searchPointer = 0x20292DC
        print('Searching for box')
        while searchPointer < 0x2040000 do
            local growth, attacks, ev, misc = utils.readPokemon(searchPointer)
            if tablesMatch(growth, boxmon[i]) then
                print('match')
                print(searchPointer)
                break
            end
            searchPointer = searchPointer + 1
        end
    end
    print('Search complete.')
end

currentBattleType = 0

usedPokemonContainer = container.UsedPokemonContainer:new{}

cumulativeChanges = {}

function readPipe()
    f = io.open(cfg.fileName, 'r')
    io.input(f)
    return io.read()
end

function initializePokemon(pokemonPointer)
    input = readPipe()
    if input == "0" or input == nil then
        return
    end
    
    local nextPokemon = usedPokemonContainer:nextPokemon()
    pokemonChanges = PokemonChanges.PokemonChanges:new(input)
    PokemonWriter.writePokemon(pokemonChanges, pokemonPointer, nextPokemon, false, false)

    cumulativeChanges[nextPokemon] = pokemonChanges
    saveload.saveChanges(cumulativeChanges)
end

function battleStarting()
    battleType = memory.readbyte(cfg.battleTypePointer)
    if battleType ~= currentBattleType and currentBattleType == 0 or currentBattleType == 8 then
        currentBattleType = battleType
        return true
    end
    currentBattleType = battleType
    return false
end

function battleTransition()
    battleType = memory.readbyte(cfg.battleTypePointer)
    if battleType ~= currentBattleType and currentBattleType == 0 or currentBattleType == 8 then
        currentBattleType = battleType
        return 1
    elseif battleType ~= currentBattleType and battleType == 0 or battleType == 8 then
        currentBattleType = battleType
        return 2
    end
    currentBattleType = battleType
    return 0
end

function tablesEqual(t1,t2)
    if (#t1~=#t2) then return false end
    for i=1,#t1 do
        if (t1[i] ~= t2[i]) then
            return false
        end
    end
    return true
end

function getPokemonCount()
    for i=1,6 do
        nickname = memory.readbyterange(cfg.enemyPokemonPointers[i]+cfg.pokemonNicknameOffset,10)
        if (tablesEqual(nickname,{0,0,0,0,0,0,0,0,0,0})) then return i-1 end
    end
    return 6
end

function run()
    --print growth data of pokemon in party for box purposes
    for i=1,#cfg.partyPokemonPointers do
        local growth, attacks, ev, misc = utils.readPokemon(cfg.partyPokemonPointers[i])
        print(misc)
    end

    print 'battle start'
    pokemonCount = getPokemonCount()
    for i=1,pokemonCount do
        initializePokemon(cfg.enemyPokemonPointers[i])
    end
end

function onFrame()
    if battleStarting() then
        run()
    end
end

print('script started')

saveload.loadChangesTable()
memory.registerexec(cfg.wildPokemonBattleFunction,run)
