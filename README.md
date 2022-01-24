# libLua
Lua interpreter library for Arduino boards. Used official Lua sources from https://www.lua.org/. The library provides standard Lua C API, so you can learn more about Lua and its API here https://www.lua.org/manual/5.4/.

## How to
To convert your Lua scripts just put them in "lua_scripts" folder and run Python script "prepareScripts.py". It will convert .lua files in headers. You can find converted scripts in "src/scripts" folder.

Simple C++ Arduino example:
```C++
#include <Arduino.h>
// Include library
#include <lua.hpp>
// Include script
#include <scripts/hello_world_lua.h>

// Function to be run from Lua
int luaprint_func(lua_State *L)
{
  // Get amount of provided arguments
  int n = lua_gettop(L);

  if (n < 0)
  {
    lua_pushstring(L, "Not enough parameter.");
    return lua_error(L);
  }

  // Get first string argument and print it
  Serial.println(lua_tostring(L, 1));
  
  return 0;
};

void setup()
{
  // Open serial
  Serial.begin(115200);
  
  // Create Lua state
  lua_State *L = luaL_newstate();
  if (L == NULL)
  {
    Serial.println("Cannot create Lua state: not enough memory.");
    while(1);
  }
  
  // Register custom println library
  lua_register(L, "println", luaprint_func);
  
  // Register standard Lua libraries
  luaL_openlibs(L);
  
  // Execute script
  luaL_dostring(L, LuaScripts::hello_world_lua.content);
}

void loop() {
  
}
```
