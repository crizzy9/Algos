# https://leetcode.com/problems/simplify-path/
class Solution:
    def simplifyPath(self, path):
        import re
        truncated_path = re.sub("/+", "/", path).split("/")
        
        new_path = []
        for p in truncated_path:
            if p in ['', '.']:
                pass
            elif p == '..':
                if len(new_path) > 0:
                    new_path.pop()
            else:
                new_path.append(p)

        print(new_path)
        return '/' + '/'.join(new_path)

if __name__ == '__main__':
    sol = Solution()
    assert sol.simplifyPath("/home/") == "/home"
    assert sol.simplifyPath("/../") == "/"
    assert sol.simplifyPath("/home//foo/") == "/home/foo"
    assert sol.simplifyPath("/a/./b/../../c/") == "/c"
    assert sol.simplifyPath("/a/../../b/../c//.//") == "/c"
    assert sol.simplifyPath("/a//b////c/d//././/..") == "/a/b/c"
