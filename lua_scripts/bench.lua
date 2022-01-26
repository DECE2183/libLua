println("Free mem in lua 0: "..getFreeMem())
local t = 1 + 2
println("Free mem in lua 1: "..getFreeMem())
local t = nil
println("Collected garbage: "..collectGarbage())
println("Free mem in lua 2: "..getFreeMem())

function benchCalc()
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