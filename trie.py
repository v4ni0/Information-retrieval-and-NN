class Node:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = Node()

    def add_word(self, word) -> None:
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = Node()
            current_node = current_node.children[char]
        current_node.is_end_of_word = True


    def contains(self, word) -> bool:
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return current_node.is_end_of_word

    def _find_words_from_node(self, node, prefix) -> list:
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        for char, child_node in node.children.items():
            words += self._find_words_from_node(child_node, prefix + char)
        return words

    def find_words_with_prefix(self, prefix) -> list:
        current_node = self.root
        for char in prefix:
            if char not in current_node.children:
                return []
            current_node = current_node.children[char]
        return self._find_words_from_node(current_node, prefix)
        
