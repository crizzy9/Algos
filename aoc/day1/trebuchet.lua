local function print_table(t)
  print("===FINAL TABLE===")

  for k, v in pairs(t) do
    print(k .. " -> " .. v)
  end
end


function getKeysSortedByValue(tbl, sortFunction)
  local keys = {}
  for key in pairs(tbl) do
    table.insert(keys, key)
  end

  table.sort(keys, function(a, b)
    return sortFunction(tbl[a], tbl[b])
  end)

  return keys
end

function getKeysSortedByKeys(tbl, sortFunction)
  local keys = {}
  for key in pairs(tbl) do
    table.insert(keys, key)
  end

  table.sort(keys, function(a, b)
    return sortFunction(a, b)
  end)

  return keys
end


local function print_sorted_table(t, sortedKeys)
  print("===SORTED TABLE===")

  for _, key in ipairs(sortedKeys) do
    print(key .. " -> " .. t[key])
  end
end

function lines_from(path)
  local lines = {}
  for line in io.lines(path, "*l") do
    lines[#lines + 1] = line
  end
  return lines
end

local ref = {
  ["zero"] = 0,
  ["one"] = 1,
  ["two"] = 2,
  ["three"] = 3,
  ["four"] = 4,
  ["five"] = 5,
  ["six"] = 6,
  ["seven"] = 7,
  ["eight"] = 8,
  ["nine"] = 9,
}

local function get_treb(str)
  local start
  local fin

  -- print("===START===")
  for i = 1, #str do
    local c = str:sub(i, i)
    -- print("char: " .. c)
    if string.match(c, '%d') then
      start = c
      break
    end
    for k, v in pairs(ref) do
      local j = i + #k
      local nm = str:sub(i, j-1)
      -- print(k .. " : " .. i .. "->" .. j .. ", ptrn: " .. nm)
      if (#k > #nm) then
        goto continue
      end
      if j-i > #str then break end
      if nm == k then
        start = v
        break
      end
      ::continue::
    end
    if start then break end
  end
  -- print("===END===")
  for i = #str, 1, -1 do
    local c = str:sub(i, i)
    -- print("char: " .. c)
    if string.match(c, '%d') then
      fin = c
      break
    end
    for k, v in pairs(ref) do
      local j = i - #k
      -- if j < 1 then break end
      local nm = str:sub(j+1, i)
      -- print(k .. " : " .. j .. "->" .. i .. ", ptrn: " .. nm)
      if (#k > #nm) then
        goto continue
      end
      if nm == k then
        fin = v
        break
      end
      ::continue::
    end
    if fin then break end
  end

  -- print("===RESULT===")
  -- print(str)
  -- print(tostring(start) .. " -> " .. tostring(fin))

  if not (start or fin) then
    return "0"
  end

  if not start then
    return tostring(fin) .. tostring(fin)
  end

  if not fin then
    return tostring(start) .. tostring(start)
  end

  return tostring(start) .. tostring(fin)
end


local function trebuchet(t)
  local nums = {}
  for k, v in pairs(t) do
    -- print("===ATTEMPTING===")
    -- print("STRING: " .. v)

    local num = get_treb(v)
    nums[v] = num

    -- print("str: " .. k .. " -> num: " .. num)
  end
  -- print_table(nums)
  return nums
end

local function sum_treb(t)
  local sum = 0
  for k, v in pairs(t) do
    sum = sum + v
  end
  return sum
end

-- local inp1 = {
--   "two1nine",
--   "eightwothree",
--   "abcone2threexyz",
--   "xtwone3four",
--   "4nineeightseven2",
--   "zoneight234",
--   "7pqrstsixteen",
-- }
--
-- local out1 = trebuchet(inp1)
-- print_table(out1)
--
-- print("===SUM 1===")
-- print("Trebuchet: " .. sum_treb(out1))

-- local inp2 = {
--   "1abc2",
--   "prs3stu8vwx",
--   "a1b2c3d4e5f",
--   "treb7uchet",
--   "aonesdx",
--   "aasninex",
--   "as",
--   "one",
--   "1",
--   "abcdtwoabcd",
-- }

local inp2 = {
  "6twomsbq",
  "81twokrqq",
  "6ninerfqlbxpx",
  "93one",
}

local out2 = trebuchet(inp2)
local sortedKeys = getKeysSortedByKeys(out2, function(a, b)
  return a < b
end)
print_sorted_table(out2, sortedKeys)

-- local sortedKeysByValue = getKeysSortedByValue(out2, function(a, b)
--   return a < b
-- end)
-- print_sorted_table(out2, sortedKeysByValue)

-- print_table(out2)

print("===SUM 2===")
print("Trebuchet: " .. sum_treb(out2))


------ INP 3 -----------
local inp3 = lines_from("aoc/treb_input.txt")
-- print_table(inp)

local out3 = trebuchet(inp3)
-- local sortedKeys = getKeysSortedByValue(out3, function(a, b)
--   return a < b
-- end)
-- print_sorted_table(out3, sortedKeys)

local sortedKeys = getKeysSortedByKeys(out3, function(a, b)
  return a < b
end)
print_sorted_table(out3, sortedKeys)


print("===SUM 3===")
print("Trebuchet: " .. sum_treb(out3))



