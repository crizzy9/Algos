class Solution:
    def reverseVowels(self, s: str) -> str:
        vowels = set({"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"})
        x = ""
        for c in s:
            if c in vowels:
                x += c
        
        new = ""
        for c in s:
            if c in vowels:
                new += x[-1]
                x = x[:-1]
            else:
                new += c
        
        return new
