-- vim: tabstop=2 shiftwidth=2 expandtab
-- https://learnxinyminutes.com/docs/lua/https://learnxinyminutes.com/docs/lua/

local num = 42

local s = 'hello'
local t = "double quoted string"
local u = [[double brackets
      start and end a multi-line string.
      Embedded newlines are okay.]]
local n = nil

while num < 50 do
	num = num + 1
end


print(num)
print(s,t,u,n)

if num > 50 then
	print('over 40')
elseif s ~= 'bac' then
  io.write('not over 40\n')
else
  ThisIsGlobal = 5
  local line = io.read()
  print('Winter is coming, ' .. line)
end

local foo = unknownVal
local boolVal = false

if not foo then print('its false') end

local ans = boolVal and 'yes' or 'no'
print(ans)

local kSum = 0
for i = 1, 100 do
  kSum = kSum + i
end

local fSum = 0
for j = 100, 1, -1 do fSum = fSum + j end

print(kSum, fSum)

num = 5
repeat
  print('this is the way')
  num = num - 1
until num == 0

local dict = {a = 'val1', b = 'val2'}
print(dict)

local function print_table(tbl)
  if type(tbl) == 'table' then
    print('{')
    for k, v in pairs(tbl) do
      print('  ' .. k .. ' -> ' .. v)
      -- print(k,v)
    end
    print('}')
  end
end

print_table(dict)

-- rec fibonacci
local function fib(k)
  if k < 4 then return 1 end
  return fib(k-2) + fib(k-1)
end

print('fib1: ' .. fib(13))

-- rec fibonacci with memoization
-- both table def okay
-- local fibt = { [1] = 0, [2] = 1 }
local fibt = { 0, 1 }
local function fib2(k)
  fibt[k] = (fibt[k-2] or fib2(k-2)) + (fibt[k-1] or fib2(k-1))
  return fibt[k]
end

print("fib2: " .. fib2(13))
print("fibseq: ")
print_table(fibt)
print('table length: ' .. #fibt)

-- fibonacci with for loop
local fibseql = '0 1'
local function fibloop(k)
  local curl = 0
  local curn = 1
  if k < 3 then return 1 end
  for _ = 3, k, 1 do
    curn, curl = curn+curl, curn
    fibseql = fibseql .. ' ' .. curn
  end
  return curn

end

print(fibloop(13))
print("fibseql: " .. fibseql)

local function adder(x)
  return function(y) return y + x end
end

print(adder(1)(2))
print(adder(10)(15))

local a,b = 5,7
print(a,b)
a,b = b,a
print(a,b)

local f = function(x) return x,10 end
local x,y = f 'hello'
print(x,y)

local g; g = function(z) return math.sin(z) end
print(g(10))
print 'hello2'


local wtab = { k12 = 15, ['@#!'] = 17, [6.213] = 15, [{}] = 1512 }
-- print_table(wtab)
print(wtab.k12)
print(wtab['@#!'])
print(wtab[6.213])
print(wtab[{}])
print(wtab['{}'])

local function h(x) print(x.key1) end
h{key1 = '123ha'}

-- _G is inbuilt table of global variables
print(_G['math'])
print(_G['_G'])
GlobalVar = '1521'
print(_G['GlobalVar'])
-- # prints length of tables
print(#_G)
-- print_table(_G)

local arr = { '123', 'val2', "!@#" }
print(#arr)
arr[2] = nil
print_table(arr)

local function print_full_table(tb)
  for k,v in pairs(tb) do
    print(k,v)
  end
end

-- Meta tables and Meta method
local f1 = {a=1, b=2}
local f2 = {a=2, b=3}

-- fails now but works with metatables
-- print(f1+f2)

local metafraction = {}
function metafraction.__add(fx,fy)
  local sum = {}
  sum.a = fx.a + fy.a
  sum.b = fx.a*fy.b + fy.a*fx.b
  return sum
end

setmetatable(f1, metafraction)
setmetatable(f2, metafraction)

local sas = f1 + f2
print_table(sas)

print(metafraction['__add'])

print_full_table(getmetatable(f1))

-- below fails, use a class like pattern
-- print(sas+sas)

local defaultFavs = { animal = 'gru', food = 'donuts' }
local myFavs = { food = 'pizza' }

setmetatable(myFavs, { __index = defaultFavs })

-- sets default from defaultFavs using __index
print(myFavs.animal)


-- Class like tables and inheritance

Dog = {}

function Dog:new()
  local newObj = { sound = 'woof' }
  self.__index = self
  return setmetatable(newObj, self)
end

function Dog:makeSound()
  print('I make this sound: ' .. self.sound)
end

local newDog = Dog:new()
newDog:makeSound()

Dog.makeSound(newDog)
newDog.makeSound(newDog)
-- newDog.makeSound(Dog)

print_full_table(newDog)
print_full_table(getmetatable(newDog))


-- Inheritance
LoudDog = Dog:new()

function LoudDog:makeSound()
  s = self.sound .. ' '
  print(s .. s .. s)
end

local husky = LoudDog:new()
husky:makeSound()


-- Modules

-- mod.lua file but can also import using local mod = (mod.file contents)

local mod = (
function()
  M = {}

  local function sayMyName()
    print("Lumino")
  end

  function M.sayHello()
    print("Hello there")
    sayMyName()
  end

  return M
end
)()
-- above is equivalent to local mod = require('mod')

mod.sayHello()
-- mod.sayMyName()

-- require('mod') uses cached value for the function
-- dofile('mod.lua') runs without caching


-- f = loadfile('mod.lua') only loads the module without running it
-- f() to run it

-- load works similar to loadfile but for strings
g = load("print('The End')")
if g then g() end
print('-----------------------')



-- fibonacci using metatables

local function setDefault(tabl,d)
  local mt = { __index = function() return d end }
  setmetatable(tabl, mt)
end

local tab = {x=10, y=20}
print(tab.x, tab.z)
setDefault(tab, 0)
print(tab.x, tab.z)


-- ipairs will only go from 1->n keys and will stop at first nil value
x = {[1]="c", [3]="a",[4]="b",[7]="l"}
for i, k in ipairs(x) do
  print(i, k)
end

print('-----------------------')

-- fibonacci using inbuilt memoization with auxiliary tables
local fibx = { 0, 1 }
setmetatable(fibx, { __mode = 'v' })
local function fib3(k)
  fibx[k] = (fibx[k-2] or fib3(k-2)) + (fibx[k-1] or fib3(k-1))
  return fibx[k]
end

print("fib3: " .. fib3(13))
print("fibseq: ")
print_table(fibx)
print('table length: ' .. #fibx)

print('-----------------------')
-- the index function way

-- Fibo = {}
-- Fibo.seq = { 0, 1, 1, 2, 3, 5 }
-- Fibo.mt = {}
-- function Fibo:new(o)
--   setmetatable(o, self.mt)
--   return o
-- end
--
-- Fibo.mt.__index = function(tabl, k)
--   -- print(tabl, k)
--   if tabl[k] then return tabl[k] end
--   tabl[k] = tabl[k-2] + tabl[k-1]
--   return tabl[k]
-- end
--
-- f = Fibo:new({})
-- print(f[3])

print('-----------------------')
-- default funct

--
-- local function setDefaultFunc(tabl,d)
--   print(tabl, d)
--   local mt = { __index = d() }
--   return setmetatable(tabl, mt)
-- end
--
-- local fibm = { 0, 1 }

-- local function fibmeta(k)
  -- fibt[k] = (fibt[k-2] or fib2(k-2)) + (fibt[k-1] or fib2(k-1))
  -- print(k)
  -- fibm[k] = fibm[k-2] + fibm[k-1]
  -- fibm[k] = fibm[k-1]
  -- return fibm[k]
-- end

-- setDefaultFunc(fibm, fibmeta)

-- print_full_table(getmetatable(fibm))
-- print("fibmeta: " .. fibm[3])
-- print("fibmeta: " .. fibmeta(4))
-- print("fibseq: ")
-- print_table(fibm)
-- print('table length: ' .. #fibm)

print('-----------------------')

-- fibonacci using an iterator

FibIterator = {}

FibIterator.seq = { 0, 1 }
-- FibIterator.mt = {}
FibIterator.len = 2

function FibIterator:new(o)
  setmetatable(o, self)
  self.__index = self
  return o
end

function FibIterator:iter()
  local i = 1
  return function()
    i = i + 1
    if i <= self.len then return self.seq[i] end
    if i > self.len then return self.next(i) end
  end
end

function FibIterator:next(k)
  self.seq[k] = self.seq[k-2] + self.seq[k-1]
  self.len = self.len + 1
  return self.seq[k]
end

-- local fibi = { 0, 1 }
-- setmetatable(fibi, { __mode = 'v' })
local fibi = FibIterator:new({0, 1})
fibi.iter = fibi:iter()






