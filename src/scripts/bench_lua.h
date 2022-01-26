#pragma once
#include "../lua_script.hpp"

namespace LuaScripts
{
  static const LuaScript bench_lua = {
    .path = "bench.lua\0",
    .content = "println(\"Free mem in lua 0: \"..getFreeMem())\r\nlocal t = 1 + 2\r\nprintln(\"Free mem in lua 1: \"..getFreeMem())\r\nlocal t = nil\r\nprintln(\"Collected garbage: \"..collectGarbage())\r\nprintln(\"Free mem in lua 2: \"..getFreeMem())\r\nfunction benchCalc()\r\n local t = 8521.0234\r\n local s = math.sin(t) + 21000\r\n s = t * math.sqrt(s)\r\n t = math.log(t)\r\n local sum = t\r\n for i = 1, 256 do\r\n sum = sum + math.log(t)\r\n end\r\n return (t / s) + sum\r\nend\r\nprintln(\"\")\r\nprintln(\"Start bench in Lua ...\")\r\nlocal bench_start_time = micros()\r\nlocal bench_result = benchCalc()\r\nlocal bench_time = micros() - bench_start_time\r\nprintln(\"Bench in Lua done by \"..bench_time..\" us with result:\"..bench_result)\0",
    .length = 676,
    .type = LuaScriptType::PlaneText,
  };
};
