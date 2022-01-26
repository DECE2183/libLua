#pragma once
#include "../lua_script.hpp"

namespace LuaScripts
{
  static const LuaScript hello_world_lua = {
    .path = "hello_world.lua\0",
    .content = "local str = \"Hello World\"\r\nprintln(str)\r\n\0",
    .length = 41,
    .type = LuaScriptType::PlaneText,
  };
};
