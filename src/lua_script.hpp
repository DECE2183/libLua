#pragma once
#include <lua.hpp>

enum class LuaScriptType
{
  PlainText,
  Compiled,
  Compressed,
  CompiledAndCompressed,
};

struct LuaScript
{
  const char *path;
  const char *content;
  const unsigned int length;
  const LuaScriptType type;

  int call(lua_State *L) const
  {
#ifdef LUA_USE_COMPRESSION
    // TODO: implement gzip compression
#endif

    int status = luaL_loadbuffer(L, content, length, path);
    if (status != LUA_OK)
    {
      return status;
    }

    status = lua_pcall(L, 0, LUA_MULTRET, 0);
    if (status != LUA_OK)
    {
      return status;
    }

    return LUA_OK;
  }
};
