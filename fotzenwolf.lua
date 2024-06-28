-- name dank rampagosRAP
-- tankt eine state file

local args = {...}
local hoi4 = require("hoi4")

local first = hoi4.parse("./history/states/" .. args[1]).state

local debug = false

function printd(d, str)
    print(string.rep("\t", d) .. str)
end

function iter(iterator, d)
    for val in iterator:iter() do
        if val.value ~= nil then
            printd(d, val.name .. " = " .. val.value)
        end
        if val.type == "literal" then
            printd(d, val.name)
        end
        if val.type == "section" then
            printd(d, val.name .. " = {")
            iter(val, d+1)
            printd(d, "}")
        end
    end
end

function append(state)
    if debug then
        print("state " .. state.id.value)
    end
    local id = state.id.value
    if state.manpower ~= nil then
        first.manpower.value = first.manpower.value + state.manpower.value
    end
    --history
    if state.history ~= nil then
        --vps
        for val in state.history:iter() do
            if val.name == "victory_points" then
                first.history:add(val)
            end
        end
        --buildings
        if state.history.buildings ~= nil then
            if first.history.buildings == nil then 
                first.history:add(state.history.buildings)
            else
                for val in state.history.buildings:iter() do
                    if debug then
                        print(val)
                    end
                    --ignore air und infra
                    if val.name == "infrastructure" or val.name == "air_base" then
                        goto SKIP
                    end
                    --skip alr added
                    if val ~= nil then
                        if val.value ~= nil then
                            first.history.buildings:add(val)
                        end
                    end
                    ::SKIP::
                end
            end
        end
    end
    -- owner core gets ignored, faggot shit
    --provs
    if state.provinces ~= nil then
        for val in state.provinces:iter() do
            first.provinces:add(val,nil)
        end
    end
end

print("#args" .. #args)
for i = 2,#args do
    print("#"..args[i]:gsub("[^a-zA-Z0-9_.+-]", "_"))
    local file = hoi4.parse("./history/states/" .. args[i])
    append(file.state)
end

print("state = {")
iter(first, 1)
print("}")