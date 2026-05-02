import string

s = str(input())
snew = str()
alphs = list(string.ascii_lowercase)
alphl = list(string.ascii_uppercase)
for i in range(len(s)):
    if s[i] in alphs:
        snew += (alphl[alphs.index(s[i])])
    elif s[i] in alphl:
        snew += (alphs[alphl.index(s[i])])
    else:
        snew += s[i]
print(snew)