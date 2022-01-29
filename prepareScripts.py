import os
import sys
from pathlib import Path

INPUT_PATH = "./lua_scripts"
BINARIES_PATH = "./lua_binaries"
BITSTREAMS_PATH = "./lua_compiled"
OUTPUT_PATH = "./src/scripts"
NEW_LINE_SIMBOL = "\n"


class ScriptType:
    PlainText = "PlainText"
    Compiled = "Compiled"
    Compressed = "Compressed"
    CompiledAndCompressed = "CompiledAndCompressed"

    def __init__(self, stype):
        stype = str(stype)
        if (stype != self.PlainText and stype != self.Compiled and stype != self.Compressed and stype != self.CompiledAndCompressed):
            raise RuntimeError(f"There is no ScriptType \"{stype}\"")
        self.type = stype

    @property
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

def compileLuaScript(script_path):
    bitstream_folder = Path(BITSTREAMS_PATH)
    binaries_folder = Path(BINARIES_PATH)

    bitstream_folder.mkdir(parents=True, exist_ok=True)

    bitstream_path = bitstream_folder.joinpath(script_path + "c")
    script_path = Path(INPUT_PATH).joinpath(script_path)
    binary_path = binaries_folder.joinpath("luac.exe")

    system_command = f"{binary_path} -o {bitstream_path} {script_path}"
    compilation_result = os.system(system_command)
    if (compilation_result != 0):
        print(f"Compilation error: {compilation_result}")
        return None

    script_file = open(bitstream_path, "rb")
    script_content = script_file.read()
    script_file.close()

    return script_content

def removeLuaComments(script_content):
    new_script_content = script_content

    # remove inline comments
    new_script_content = removeRangeFromString(new_script_content, "--", "\\r\\n")
    # remove multiline comments
    new_script_content = removeRangeFromString(new_script_content, "--[[", "]]")

    return new_script_content

def prepareScript(script_name, script_path, script_content, type):
    new_script_content = script_content
    new_script_length = 0

    if (type == ScriptType.Compiled or type == ScriptType.CompiledAndCompressed):
        script_binary = compileLuaScript(script_path)
        if (script_binary == None):
            return ""

        new_script_length = len(script_binary)
        new_script_content = ''.join(("0x" + format(x, '02x') + ", ") for x in script_binary)
        new_script_content = new_script_content[:-2]
        new_script_content = "{ " + new_script_content + " }"
    else:
        new_script_content = new_script_content.replace("\\", "\\\\")
        new_script_content = new_script_content.replace("\n", "\\r\\n")
        new_script_content = new_script_content.replace("\"", "\\\"")
        new_script_content = new_script_content.replace("\'", "\\\'")

        new_script_content = " ".join(new_script_content.split())
        new_script_content = removeLuaComments(new_script_content)
        new_script_content = removeRangeFromString(new_script_content, "\\r\\n\\r\\n", "\\r\\n")
        new_script_content = removeRangeFromString(new_script_content, "\\r\\n \\r\\n", "\\r\\n")
        new_script_length = len(new_script_content.replace("\\", ""))
        new_script_content = "\"" + new_script_content + "\\0\""

    file_content = "#pragma once" + NEW_LINE_SIMBOL
    file_content += "#include \"../lua_script.hpp\"" + NEW_LINE_SIMBOL + NEW_LINE_SIMBOL

    if (type == ScriptType.Compiled or type == ScriptType.CompiledAndCompressed):
        file_content += f"static const unsigned char {script_name}_lua_bytecode[] = {new_script_content};" + NEW_LINE_SIMBOL + NEW_LINE_SIMBOL
        new_script_content = f"(const char *){script_name}_lua_bytecode"

    file_content += "namespace LuaScripts" + NEW_LINE_SIMBOL
    file_content += "{" + NEW_LINE_SIMBOL

    file_content += "  static const LuaScript " + script_name + "_lua = {" + NEW_LINE_SIMBOL
    file_content += f"    .path = \"{script_path}\\0\"," + NEW_LINE_SIMBOL
    file_content += f"    .content = {new_script_content}," + NEW_LINE_SIMBOL
    file_content += f"    .length = {new_script_length}," + NEW_LINE_SIMBOL
    file_content += f"    .type = LuaScriptType::{type}," + NEW_LINE_SIMBOL
    file_content += "  };" + NEW_LINE_SIMBOL

    file_content += "};" + NEW_LINE_SIMBOL

    return file_content


if __name__ == "__main__":
    args = sys.argv

    input_path = Path(INPUT_PATH)
    output_path = Path(OUTPUT_PATH)
    output_path.mkdir(parents=True, exist_ok=True)

    scripts_type = ScriptType(ScriptType.PlainText)

    if len(args) > 1 and args[1] != None:
        scripts_type = ScriptType(args[1])

    pathlist = input_path.rglob("*.lua")
    for path in pathlist:
        script_path = str(path.relative_to(input_path))
        script_name = str(script_path[0:-4]).replace("/", "_").replace("\\", "_")

        print(f"Script - {path} -> {output_path.joinpath(Path(script_name))}_lua.hpp")

        script_file = path.open("r", encoding=("utf-8"))
        script_content = script_file.read()
        script_file.close()

        output_file = open(output_path.joinpath(Path(script_name + "_lua.h")), "w", encoding=("utf-8"))
        output_file.write(prepareScript(script_name, script_path, script_content, scripts_type.type))
        output_file.close()
