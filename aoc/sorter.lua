local tbl = {
  ["abc"] = 15,
  ["def"] = 51,
  ["ghi"] = 1,
  ["jkl"] = 12,
  ["mno"] = 56,
  ["pqrs"] = 12,
  ["tuv"] = 22,
  ["wxyz"] = 90,
}

local function print_table(t)
  print("===FINAL TABLE===")

  for k, v in pairs(t) do
    print(k .. " -> " .. v)
  end
end

print_table(tbl)

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

local sortedKeys = getKeysSortedByValue(tbl, function(a, b)
  return a < b
end)

local function print_sorted_table(t, sortedKeys)
  print("===SORTED TABLE===")

  for _, key in ipairs(sortedKeys) do
    print(key .. " -> " .. t[key])
  end
end

print_sorted_table(tbl, sortedKeys)


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

local sortedKeys = getKeysSortedByKeys(tbl, function(a, b)
  return a < b
end)

print_sorted_table(tbl, sortedKeys)

