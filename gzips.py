import gzip
import os


class TreeNode:
    def __init__(self, name, content=None):
        self.name = name
        self.content = content  # Para armazenar o conteúdo de "arquivos"
        self.children = []  # Lista de filhos

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self, level=0):
        indent = "  " * level
        result = f"{indent}{self.name}"
        if self.content:
            result += f" (File Content: {self.content})"
        result += "\n"
        for child in self.children:
            result += child.__repr__(level + 1)
        return result


def parse_tree(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    root = TreeNode("Root")
    node_stack = [(-1, root)]  # Armazena (nível, nó)
    
    for line in lines:
        stripped_line = line.lstrip()
        level = (len(line) - len(stripped_line)) // 2  # Calcula o nível baseado nos espaços iniciais
        stripped_line = stripped_line.strip()

        # Verificar se é um "arquivo"
        if "=" in stripped_line:
            name, content = stripped_line.split("=", 1)
            # Substituir "\n" e "\r" por seus equivalentes binários
            content = content.replace("\\n", "\n").replace("\\r", "\r")
            new_node = TreeNode(name.strip(), content.strip())
        else:
            new_node = TreeNode(stripped_line)

        # Encontrar o pai no nível adequado
        while node_stack and node_stack[-1][0] >= level:
            node_stack.pop()

        parent = node_stack[-1][1]
        parent.add_child(new_node)
        node_stack.append((level, new_node))

    return root


def save_tree_to_gzip(tree, output_path):
    def serialize(node, level=0):
        lines = []
        indent = "  " * level
        if node.content:
            lines.append(f"{indent}{node.name}={node.content}\n")
        else:
            lines.append(f"{indent}{node.name}\n")
        for child in node.children:
            lines.extend(serialize(child, level + 1))
        return lines

    serialized_data = "".join(serialize(tree))

    with gzip.open(output_path, "wt", encoding="utf-8") as gzip_file:
        gzip_file.write(serialized_data)


def main():
    file_path = input("Enter the name of the text file to parse: ").strip()
    if not os.path.exists(file_path):
        print("File does not exist.")
        return

    tree = parse_tree(file_path)
    print("Tree structure:")
    print(tree)

    output_path = input("Enter the name for the gzip output file: ").strip()
    if not output_path.endswith(".gz"):
        output_path += ".gz"

    save_tree_to_gzip(tree, output_path)
    print(f"Tree saved to {output_path}")


if __name__ == "__main__":
    main()

