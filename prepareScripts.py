from pathlib import Path

INPUT_PATH = "./lua_scripts"
OUTPUT_PATH = "./src/scripts"
NEW_LINE_SIMBOL = "\n"


class ScriptType:
    PlaneText = "PlaneText"
    Compiled = "Compiled"
    Hashed = "Hashed"
    CompiledAndHashed = "CompiledAndHashed"

    def __init__(self, type):
        if (type != self.PlaneText and type != self.Compiled and type != self.Hashed and type != self.CompiledAndHashed):
            raise RuntimeError(f"There is no ScriptType \"{type}\"")
        self.type = type

    def get_property(self):
        return self.type


def sliceString(string, start, stop):
    return string[:start] + string[stop:]

def removeRangeFromString(string, start_str, stop_str):
    start_pos = string.find(start_str)
    while (start_pos > -1):
        substr = string[(start_pos + 1):]
        stop_pos = start_pos + substr.find(stop_str) + 1
        string = sliceString(string, start_pos, stop_pos)
        start_pos = string.find(start_str)

    return string


def removeLuaComments(script_content):
    new_script_content = script_content

    # remove inline comments
    new_script_content = removeRangeFromString(new_script_content, "--", "\\r\\n")
    # remove multiline comments
    new_script_content = removeRangeFromString(new_script_content, "--[[", "]]")

    return new_script_content

def prepareScript(script_name, script_path, script_content, type):
    new_script_content = script_content
    new_script_content = new_script_content.replace("\\", "\\\\")
    new_script_content = new_script_content.replace("\n", "\\r\\n")
    new_script_content = new_script_content.replace("\"", "\\\"")
    new_script_content = new_script_content.replace("\'", "\\\'")

    new_script_content = " ".join(new_script_content.split())
    new_script_content = removeLuaComments(new_script_content)
    new_script_content = removeRangeFromString(new_script_content, "\\r\\n\\r\\n", "\\r\\n")
    new_script_content = removeRangeFromString(new_script_content, "\\r\\n \\r\\n", "\\r\\n")

    file_content = "#pragma once" + NEW_LINE_SIMBOL
    file_content += "#include \"../lua_script.hpp\"" + NEW_LINE_SIMBOL + NEW_LINE_SIMBOL

    file_content += "namespace LuaScripts" + NEW_LINE_SIMBOL
    file_content += "{" + NEW_LINE_SIMBOL

    file_content += "  static const LuaScript " + script_name + "_lua = {" + NEW_LINE_SIMBOL
    file_content += f"    .path = \"{script_path}\\0\"," + NEW_LINE_SIMBOL
    file_content += f"    .content = \"{new_script_content}\\0\"," + NEW_LINE_SIMBOL
    file_content += f"    .length = {len(new_script_content)}," + NEW_LINE_SIMBOL
    file_content += f"    .type = LuaScriptType::{type}," + NEW_LINE_SIMBOL
    file_content += "  };" + NEW_LINE_SIMBOL

    file_content += "};" + NEW_LINE_SIMBOL

    return file_content


if __name__ == "__main__":
    input_path = Path(INPUT_PATH)
    output_path = Path(OUTPUT_PATH)

    pathlist = input_path.rglob("*.lua")
    for path in pathlist:
        script_path = str(path.relative_to(input_path))
        script_name = str(script_path[0:-4]).replace("/", "_").replace("\\", "_")

        print(f"Script - {path} -> {output_path.joinpath(Path(script_name))}_lua.h")

        script_file = path.open("r", encoding=("utf-8"))
        script_content = script_file.read()
        script_file.close()

        output_file = open(output_path.joinpath(Path(script_name + "_lua.h")), "w", encoding=("utf-8"))
        output_file.write(prepareScript(script_name, script_path, script_content, ScriptType.PlaneText))
        output_file.close()
