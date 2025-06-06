import json
import os

def ask(prompt, default=None):
    val = input(f"{prompt} {'[' + default + ']' if default else ''}: ").strip()
    return val if val else default

def multiline_input(prompt):
    print(prompt)
    print("(Enter one item per line, leave blank to finish):")
    lines = []
    while True:
        line = input("> ").strip()
        if line == "":
            break
        lines.append(line)
    return lines

def generate_compile_commands(compiler, src_dirs, include_dirs, defines, output_dir, entries=[]):
    for src_dir in src_dirs:
        for root, _, files in os.walk(src_dir):
            for file in files:
                if file.endswith(".c") or file.endswith(".cpp"):
                    src_path = os.path.join(root, file)
                    includes = " ".join([f"-I{d}" for d in include_dirs])
                    defs = " ".join([f"-D{d}" for d in defines])
                    cmd = f"{compiler} -c {defs} {includes} -o {output_dir}/{file}.o {src_path}"
                    entries.append({
                        "directory": os.getcwd(),
                        "command": cmd,
                        "file": src_path
                    })
    return entries

def write_compile_commands(entries):
    with open("compile_commands.json", "w") as f:
        json.dump(entries, f, indent=2)
    print("✅ Generated compile_commands.json")

def write_clangd_config(compilation_database_path):
    content = f"""CompileFlags:
  CompilationDatabase: {compilation_database_path}
"""
    # If file exists, overwrite.
    with open(".clangd", "w") as f:
        f.write(content)
    print("✅ Generated .clangd")

def main():
    print("🛠️  Clangd Setup Wizard for Embedded Projects")
    amend = False
    if os.path.exists("compile_commands.json"):
        print("compile_commands.json already exists. Amend or overwrite?")
        if ask("Overwrite?", "yes").lower().startswith("y"):
            os.remove("compile_commands.json")
        else:
            print("Amending...")
            amend = True

    if not amend:
        platform = ask("What platform are you using?", "ARM")
        compiler = ask("Enter compiler command", "arm-none-eabi-gcc")

    phrasing = "Amend" if amend else "Enter a"
    src_dirs = multiline_input(phrasing + " list of directories containing source files")
    include_dirs = multiline_input(phrasing + " list of include paths (relative or absolute)")
    defines = multiline_input(phrasing + " preprocessor defines (e.g., STM32G0xx)")
    output_dir = ask("Where should object files go?", "./build")

    os.makedirs(output_dir, exist_ok=True)
    if amend:
        # Pull JSON from existing compile_commands.json
        with open("compile_commands.json", "r") as f:
            entries = json.load(f)
            compiler = entries[0]["command"].split()[0]
    else:
        # Generate new entries
        entries = []
    entries = generate_compile_commands(compiler, src_dirs, include_dirs, defines, output_dir)

    print("Current directory ", os.getcwd())
    if ask("Generate .clangd file pointing to this directory?", "yes").lower().startswith("y"):
        write_clangd_config(os.getcwd())

    write_compile_commands(entries)

if __name__ == "__main__":
    main()
