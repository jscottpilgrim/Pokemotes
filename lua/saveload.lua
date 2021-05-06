cfg = require 'cfg'
PokemonWriter = require 'PokemonWriter'
container = require 'UsedPokemonContainer'

local M = {}

newSave = {}

function saveAll()
    -- save all current memory to file
    local savefile = io.open("savemem.bin", "wb")
    local current = cfg.romStartAddress
    while current < cfg.romEndAddress do
        --write all memory to file
        local b = memory.readbyte(current)
        savefile:write(b)
        current = current + 1
    end
    savefile:close()
end

function loadAll()
    -- read savestate from file into memory
    local savefile = io.open("savemem.bin", "rb")
    local current = cfg.romStartAddress
    while current < cfg.romEndAddress do
        -- overwrite all memory with file
        local b = savefile:read(1)
        if not b then break end
        memory.writebyte(current, b)
        current = current + 1
    end
    savefile:close()
end

-- https://stackoverflow.com/questions/6589617/lua-convert-a-table-into-a-comma-separated-list
--This file exports a function, WriteTable, that writes a given table out to a given file handle.

local writeKey = {};

function writeKey.string(hFile, value, iRecursion)
    WriteFormatted(hFile, "[\"%s\"]", value);
end

function writeKey.number(hFile, value, iRecursion)
    WriteFormatted(hFile, "[%i]", value);
end

local writeValue = {};

function writeValue.string(hFile, value, iRecursion)
    WriteFormatted(hFile, "[==[%s]==]", value);
end

function writeValue.number(hFile, value, iRecursion)
    WriteFormatted(hFile, "%i", value);
end

function writeValue.boolean(hFile, value, iRecursion)
    if(value) then hFile:write("true"); else hFile:write("false"); end;
end

function writeValue.table(hFile, value, iRecursion)
    WriteTable(hFile, value, iRecursion)
end

function WriteFormatted(hFile, strFormat, ...)
    hFile:write(string.format(strFormat, ...));
end

local function WriteForm(hFile, strFormat, ...)
    hFile:write(string.format(strFormat, ...));
end

local function WriteTabs(hFile, iRecursion)
    for iCount = 1, iRecursion, 1 do
        hFile:write("\t");
    end
end

function WriteTable(hFile, outTable, iRecursion)
    if(iRecursion == nil) then iRecursion = 1; end

    hFile:write("{\n");

    local bHasArray = false;
    local arraySize = 0;

    if(#outTable > 0) then bHasArray = true; arraySize = #outTable; end;

    for key, value in pairs(outTable) do
        if(writeKey[type(key)] == nil) then print("Malformed table key."); return; end
        if(writeValue[type(value)] == nil) then
            print( string.format("Bad value in table: key: '%s' value type '%s'.", key, type(value)));
            return;
        end

        --If the key is not an array index, process it.
        if((not bHasArray) or
                (type(key) ~= "number") or
                not((1 <= key) and (key <= arraySize))) then
            WriteTabs(hFile, iRecursion);
            writeKey[type(key)](hFile, key, iRecursion + 1);
            hFile:write(" = ");
            writeValue[type(value)](hFile, value, iRecursion + 1);

            hFile:write(",\n");
        end
    end

    if(bHasArray) then
        for i, value in ipairs(outTable) do
            WriteTabs(hFile, iRecursion);
            writeValue[type(value)](hFile, value, iRecursion + 1);
            hFile:write(",\n");
        end
    end

    WriteTabs(hFile, iRecursion - 1);
    hFile:write("}");
end

function saveChanges(changesTable)
    print 'Saving changes table to file'

    --local savingChanges = newSave + changesTable
    for k, v in pairs(changesTable) do
        newSave[k] = v
    end

    local savetable = io.open("savedChanges.lua", "w")
    --saveTable:write(changesTable)
    savetable:write("local M =\n")
    WriteTable(savetable, newSave)
    savetable:write("\nreturn M")
    savetable:close()

    print 'Changes saved'
end

function loadChangesTable()
    print 'Loading from changes table'
    --load saved pokemotes back into party and box
    --overwrite old save with new save, storing only the pokemon in use
    loadedTable = require 'savedChanges'

    newSave = {}

    -- load party pokemon
    for i=1,#cfg.partyPokemonPointers do
        local pointer = cfg.partyPokemonPointers[i]
        local id = container.getPokemonIdAtPosition(pointer)
        if id ~= 0 then
            if loadedTable[id] ~= nil then
                newSave[id] = loadedTable[id]
                PokemonWriter.writePokemon(loadedTable[id], pointer, id, true, false)
            end
        end
    end
    -- load boxed pokemon
    if cfg.boxSearched then
        --load first separate because its address can be weird
        local pointer = cfg.box1start
        local id = container.getPokemonIdAtPosition(pointer)
        
        if id ~= 0 then
            if loadedTable[id] ~= nil then
                --print(id)
                newSave[id] = loadedTable[id]
                PokemonWriter.writePokemon(loadedTable[id], pointer, id, true, true)
            end
        end
        --load remaining box mon
        for i=0,cfg.boxPositionCount-2 do
            local pointer = cfg.box1second+i*cfg.boxPokemonDataSize
            local id = container.getPokemonIdAtPosition(pointer)
            
            if id ~= 0 then
                if loadedTable[id] ~= nil then
                    --print(id)
                    newSave[id] = loadedTable[id]
                    PokemonWriter.writePokemon(loadedTable[id], pointer, id, true, true)
                end
            end
        end
    end

    --backup old table
    local backupTable = io.open("backupChanges.lua", "w")
    backupTable:write("local M =\n")
    WriteTable(backupTable, loadedTable)
    backupTable:write("\nreturn M")
    backupTable:close()

    local savetable = io.open("savedChanges.lua", "w")
    savetable:write("local M =\n")
    WriteTable(savetable, newSave)
    savetable:write("\nreturn M")
    savetable:close()

    print 'Changes loaded'
end

function saveFirstBox()
    print 'Saving data of first pokemon in pc'

    local trackgrowth, trackattacks, trackev, trackmisc = utils.readPokemon(cfg.box1start)

    local boxsave = io.open("savedFirstBox.lua", "w")
    boxsave:write("local M =\n")
    WriteTable(boxsave, trackgrowth)
    boxsave:write("\nreturn M")
    boxsave:close()

    print 'First boxed pokemon saved'
end

M.saveAll = saveAll
M.loadAll = loadAll
M.saveChanges = saveChanges
M.loadChangesTable = loadChangesTable
M.saveFirstBox = saveFirstBox
return M