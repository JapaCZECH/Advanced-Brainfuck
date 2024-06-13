import json
import sys
from read import read

chars = "".join(chr(i) for i in range(255))

def main():
    with open("lang.json", "r") as f:
        data = json.load(f)
        keywords = data["keywords"]
        settings = data["settings"]
    
    content = read(sys.argv[1])
    pointer = 0
    cells = [0] * settings.get("start_cells", 1)

    output = ""

    loop_stack = []
    loop_index = 0

    while loop_index < len(content):
        char = content[loop_index]

        if char == keywords["increment"]:
            cells[pointer] += 1
        elif char == keywords["decrease"]:
            if cells[pointer] > 0:
                cells[pointer] -= 1
        elif char == keywords["left"]:
            pointer = max(0, pointer - 1)
        elif char == keywords["right"]:
            pointer += 1
            if pointer >= len(cells):
                cells.append(0)
        elif char == keywords["loop_start"]:
            if cells[pointer] == 0:
                loop_depth = 1
                while loop_depth > 0:
                    loop_index += 1
                    if loop_index >= len(content):
                        break
                    if content[loop_index] == keywords["loop_start"]:
                        loop_depth += 1
                    elif content[loop_index] == keywords["loop_end"]:
                        loop_depth -= 1
            else:
                loop_stack.append(loop_index)
        elif char == keywords["loop_end"]:
            if cells[pointer] != 0:
                loop_index = loop_stack[-1]
            else:
                loop_stack.pop()
        elif char == keywords["output"]:
            try:
                output += chars[cells[pointer]]
            except IndexError:
                pass
        elif char == keywords["raw_output"]:
            output += str(cells[pointer])
        elif char == keywords["pointer_pos"]:
            cells[pointer] = pointer
        elif char == keywords["cell_count"]:
            cells[pointer] = len(cells)
        elif char == keywords["space"]:
            cells[pointer] = 32
        elif char == keywords["mem_1"]:
            mem1 = cells[pointer]
        elif char == keywords["mem_2"]:
            mem2 = cells[pointer]
        elif char == keywords["add"]:
            cells[pointer] = mem1 + mem2
        elif char == keywords["subtract"]:
            cells[pointer] = mem1 - mem2
        elif char == keywords["divide"]:
            cells[pointer] = mem1 / mem2
        elif char == keywords["multiply"]:
            cells[pointer] = mem1 * mem2
        elif char == keywords["load_mem1"]:
            cells[pointer] = mem1
        elif char == keywords["load_mem2"]:
            cells[pointer] = mem2
        elif char == keywords["jump"]:
            if (cells[pointer] > len(cells)):
                i = pointer
                for i in range(cells[pointer]):
                    cells.append(0)
            pointer = cells[pointer]
        elif char == keywords["end"]:
            break

        loop_index += 1

    print(output)

if __name__ == "__main__":
    main()
