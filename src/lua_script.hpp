#pragma once

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
};
