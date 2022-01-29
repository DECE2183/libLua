
--[[
// Arduino micros func to register in Lua
int luamicros_func(lua_State *L)
{
  lua_pushnumber(L, micros());
  return 1;
}
]]

local function benchCalc()
  local t = 8521.0234
  local s = math.sin(t) + 21000
 
  s = t * math.sqrt(s)
  t = math.log(t)

  local sum = t
  for i = 1, 256 do
    sum = sum + math.log(t)
  end

  return (t / s) + sum
end

println("")
println("Start bench in Lua ...")
local bench_start_time = micros()
local bench_result = benchCalc()
local bench_time = micros() - bench_start_time

println("Bench in Lua done by "..bench_time.." us with result:"..bench_result)