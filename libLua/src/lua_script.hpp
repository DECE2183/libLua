#pragma once

enum class LuaScriptType
{
  PlaneText,
  Compiled,
  Hashed,
  CompiledAndHashed,
};

struct LuaScript
{
  const char *path;
  const char *content;
  const unsigned int length;
  const LuaScriptType type;
};
