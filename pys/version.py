import os
def version(release_node_path):
    with open(release_node_path, 'r+') as f:
        print(f.read())

if __name__ == '__main__':
    version("../release_note.txt")