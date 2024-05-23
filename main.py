import json
import random
import uuid
import time
from anytree import Node, RenderTree


class TreeNode:
    def __init__(self, value):
        self.id = str(uuid.uuid4())
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


def generate_n_tree(depth, max_children, current_depth=0):
    if current_depth == depth:
        return None

    root = TreeNode(random.randint(0, 100))
    num_children = random.randint(0, max_children)
    for _ in range(num_children):
        child = generate_n_tree(depth, max_children, current_depth + 1)
        if child:
            root.add_child(child)

    return root


def tree_to_anytree(node):
    anytree_node = Node(f"Value: {node.value}")
    for child in node.children:
        child_anytree = tree_to_anytree(child)
        child_anytree.parent = anytree_node
    return anytree_node


def tree_to_dict(node):
    if not node:
        return None
    return {
        "id": node.id,
        "value": node.value,
        "children": [tree_to_dict(child) for child in node.children]
    }


def save_tree_to_json(root, filename):
    tree_dict = tree_to_dict(root)
    with open(filename, 'w') as f:
        json.dump(tree_dict, f, indent=4)


def load_tree_from_json(filename):
    with open(filename, 'r') as f:
        tree_dict = json.load(f)

    def dict_to_tree(d):
        if not d:
            return None
        node = TreeNode(d['value'])
        node.id = d['id']
        for child_dict in d['children']:
            child = dict_to_tree(child_dict)
            if child:
                node.add_child(child)
        return node

    return dict_to_tree(tree_dict)


def find_depth_to_leaves(node):
    if not node.children:
        return 0
    return 1 + max(find_depth_to_leaves(child) for child in node.children)


def count_nodes_at_level(node, level):
    if level == 0:
        return 1
    count = 0
    for child in node.children:
        count += count_nodes_at_level(child, level - 1)
    return count


def find_widest_subtrees_with_target_height(root, target_height):
    if not root:
        return []

    max_width = 0
    widest_subtrees = []

    def dfs(node):
        nonlocal max_width, widest_subtrees

        depth = find_depth_to_leaves(node)
        if depth == target_height:
            width = count_nodes_at_level(node, target_height)
            if width > max_width:
                max_width = width
                widest_subtrees = [node]
            elif width == max_width:
                widest_subtrees.append(node)

        for child in node.children:
            dfs(child)

    dfs(root)
    return widest_subtrees


def find_narrowest_subtrees_with_target_height(root, target_height):
    if not root:
        return []

    min_width = float('inf')
    narrowest_subtrees = []

    def dfs(node):
        nonlocal min_width, narrowest_subtrees

        depth = find_depth_to_leaves(node)
        if depth == target_height:
            width = count_nodes_at_level(node, target_height)
            if width < min_width:
                min_width = width
                narrowest_subtrees = [node]
            elif width == min_width:
                narrowest_subtrees.append(node)

        for child in node.children:
            dfs(child)

    dfs(root)
    return narrowest_subtrees


if __name__ == "__main__":
    target_height = int(input("Укажите высоту поддеревьев: "))  # Height at which we are looking for the widest/narrowest subtree

    # Generate a tree
    #depth = int(input("Укажите глубину дерева: "))
    #max_children = int(input(" Укажите максимальное количество детей: "))
    root = generate_n_tree(5, 4)

    # Save the tree to a JSON file
    #save_tree_to_json(root, 'n_tree.json')

    # Load the tree from the JSON file
    root = load_tree_from_json('n_tree.json')

    # Convert the tree to an anytree structure for display
    root_anytree = tree_to_anytree(root)

    print("Original Tree Structure:")
    for pre, _, node in RenderTree(root_anytree):
        print("%s%s" % (pre, node.name))

    print()
    total_start_time = time.time()
    # Find the widest subtree at the given height
    widest_subtrees = find_widest_subtrees_with_target_height(root, target_height)
    narrowest_subtrees = find_narrowest_subtrees_with_target_height(root, target_height)
    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time
    if widest_subtrees:
        print(f"Самые широкие поддеревья на высоте {target_height}:")
        for i, subtree_root in enumerate(widest_subtrees, 1):
            print(f"\nSubtree {i}:")
            subtree_anytree = tree_to_anytree(subtree_root)
            for pre, _, node in RenderTree(subtree_anytree):
                print("%s%s" % (pre, node.name))
    else:
        print(f"Поддерево на высоте {target_height} не найдено.")

    print()

    # Find the narrowest subtree at the given height


    if narrowest_subtrees:
        print(f"Самые узкие поддеревья на высоте {target_height}:")
        for i, subtree_root in enumerate(narrowest_subtrees, 1):
            print(f"\nSubtree {i}:")
            subtree_anytree = tree_to_anytree(subtree_root)
            for pre, _, node in RenderTree(subtree_anytree):
                print("%s%s" % (pre, node.name))
    else:
        print(f"Поддерево на высоте {target_height} не найдено.")
    print(f"Общее время выполнения поиска всех поддеревьев: {total_elapsed_time:.6f} секунд")
