from typing import Self

class Item:
    def __init__(self) -> None:
        self.isFile: bool = False
        self.content: str = ""
        self.items:dict[str, Self] = {}

class FileSystem:

    def __init__(self):
        self.root: Item = Item()


    def __get_path_items(self, path: str) -> list[str]:
        if path == "/":
            return []
        else:
            return path[1:].split('/')

    def ls(self, path: str) -> list[str]:
        path_items = self.__get_path_items(path)

        curr = self.root
        for p in path_items:
            if curr.items.get(p) is None:
                return []
            elif not curr.isFile:
                curr = curr.items[p]

        if curr.isFile:
            return [path_items[-1]]
        return sorted(list(curr.items.keys()))

    def mkdir(self, path: str) -> None:
        path_items = self.__get_path_items(path)

        curr = self.root
        for p in path_items:
            if curr.items.get(p) is None:
                curr.items[p] = Item()
            curr = curr.items[p]

    def addContentToFile(self, filePath: str, content: str) -> None:
        path_items = self.__get_path_items(filePath)

        curr = self.root
        for p in path_items:
            if curr.items.get(p) is None:
                curr.items[p] = Item()
            curr = curr.items[p]
        curr.isFile = True
        curr.content += content

    def readContentFromFile(self, filePath: str) -> str:
        path_items = self.__get_path_items(filePath)

        curr = self.root
        for p in path_items:
            if curr.items.get(p) is not None:
                curr = curr.items[p]
        return curr.content


if __name__ == "__main__":
    # Test 1

    print("----- Test 1 -----")
    fs = FileSystem()

    p1 = fs.ls("/")
    print(f"ls /: {p1}")

    fs.mkdir("/a/b/c")

    fs.addContentToFile("/a/b/c/d", "hello")

    p2 = fs.ls("/")
    print(f"ls /: {p2}")

    p3 = fs.readContentFromFile("/a/b/c/d")
    print(f"readContentFromFile /a/b/c/d: {p3}")


    # Test 2
    # ["FileSystem","ls","mkdir","addContentToFile","ls","readContentFromFile","addContentToFile","readContentFromFile"]
    # [[],["/"],["/a/b/c"],["/a/b/c/d","hello world"],["/"],["/a/b/c/d"],["/a/b/c/d"," hello hello world"],["/a/b/c/d"]]

    print("----- Test 2 -----")

    fs = FileSystem()

    p1 = fs.ls("/")
    print(f"ls /: {p1}")

    fs.mkdir("/a/b/c")

    fs.addContentToFile("/a/b/c/d", "hello world")

    p2 = fs.ls("/")
    print(f"ls /: {p2}")

    p3 = fs.readContentFromFile("/a/b/c/d")
    print(f"readContentFromFile /a/b/c/d: {p3}")

    fs.addContentToFile("/a/b/c/d", "hello hello world")

    p4 = fs.readContentFromFile("/a/b/c/d")
    print(f"readContentFromFile /a/b/c/d: {p4}")

    # Test 3
    # ["FileSystem","ls","mkdir","ls","mkdir","ls"]
    # [[],["/"],["/a/b/c"],["/a/b"],["/a/b/a"],["/a/b"]]

    print("----- Test 3 -----")

    fs = FileSystem()

    p1 = fs.ls("/")
    print(f"ls /: {p1}")

    fs.mkdir("/a/b/c")

    p2 = fs.ls("/a/b")
    print(f"ls /: {p2}")

    fs.mkdir("/a/b/a")

    p3 = fs.ls("/a/b")
    print(f"ls /: {p3}")

    # Test 4
    # ["FileSystem","mkdir","ls","ls","mkdir","ls","ls","addContentToFile","ls","ls","ls"]
    # [[],["/goowmfn"],["/goowmfn"],["/"],["/z"],["/"],["/"],["/goowmfn/c","shetopcy"],["/z"],["/goowmfn/c"],["/goowmfn"]]

    print("----- Test 4 -----")

    fs = FileSystem()

    fs.mkdir("/goowmfn")

    p1 = fs.ls("/goowmfn")
    print(f"ls /goowmfn: {p1}")

    p2 = fs.ls("/")
    print(f"ls /: {p2}")

    fs.mkdir("/z")

    p3 = fs.ls("/")
    print(f"ls /: {p3}")

    p4 = fs.ls("/")
    print(f"ls /: {p4}")

    fs.addContentToFile("/goowmfn/c", "shetopcy")

    p5 = fs.ls("/z")
    print(f"ls /z: {p5}")

    p6 = fs.ls("/goowmfn/c")
    print(f"ls /goowmfn/c: {p6}")

    p7 = fs.ls("/goowmfn")
    print(f"ls /goowmfn: {p7}")

