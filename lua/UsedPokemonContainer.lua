cfg = require 'cfg'
utils = require 'utils'

local M = {}

local tempUnusedPokemon = {}
for i=1,cfg.maxPokemonId do
    table.insert(tempUnusedPokemon, i)
end

UsedPokemonContainer = {
    unusedPokemon = tempUnusedPokemon
}

function UsedPokemonContainer:new()
    o = {}
    setmetatable(o, self)
    self.__index = self
    self.unusedPokemon = {}--tempUnusedPokemon

    local usedPokemon = {}
    --remove party pokemon from list of unused pokemon
    for i=1,#cfg.partyPokemonPointers do
        local id = getPokemonIdAtPosition(cfg.partyPokemonPointers[i])
        if id ~= 0 then
            usedPokemon[id] = true
        end
    end
    -- add boxed pokemon to list of pokemon in use
    if cfg.boxSearched then
        --check first boxed mon separately
        local id = getPokemonIdAtPosition(cfg.box1start)
        if id ~= 0 then
            usedPokemon[id] = true
        end
        --check remaining box mon
        for i=0,cfg.boxPositionCount-2 do
            -- updated this line to use boxPokemonDataSize
            local id = getPokemonIdAtPosition(cfg.box1second+i*cfg.boxPokemonDataSize)
            if id ~= 0 then
                usedPokemon[id] = true
            end
        end
    end

    for i=1,cfg.maxPokemonId do
        if usedPokemon[i] ~= true then
            table.insert(self.unusedPokemon, i)
        end
    end

    print(self.unusedPokemon)
    return o
end

function UsedPokemonContainer:nextPokemon()
    if #self.unusedPokemon == 0 then
        self.addUnusedPokemon()
    end
    
    -- randomize the next pokemon
    c = math.random(1,#self.unusedPokemon-1)
    return table.remove(self.unusedPokemon, c)
end

function UsedPokemonContainer:addUnusedPokemon()
    local usedPokemon = {}
    -- add party pokemon to list of pokemon in use
    for i=1,#cfg.partyPokemonPointers do
        local id = getPokemonIdAtPosition(cfg.partyPokemonPointers[i])
        if id ~= 0 then
            usedPokemon[id] = true
        end
    end
    -- add boxed pokemon to list of pokemon in use
    for i=0,cfg.boxPositionCount-1 do
        -- updated this line to use boxPokemonDataSize
        local id = getPokemonIdAtPosition(cfg.box1start+i*cfg.boxPokemonDataSize)
        if id ~= 0 then
            usedPokemon[id] = true
        end
    end
    for i=1,cfg.maxPokemonId do
        if usedPokemon[i] ~= true then
            table.insert(self.unusedPokemon, i)
        end
    end
end

function getPokemonIdAtPosition(position)
    local growth, attacks, ev, misc = utils.readPokemon(position)
    --print(growth)
    --print(attacks)
    --print(ev)
    --print(misc)
    return growth[1] + growth[2]*0x100
end

M.UsedPokemonContainer = UsedPokemonContainer
M.getPokemonIdAtPosition = getPokemonIdAtPosition
return M