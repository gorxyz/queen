bruteforce = open("wordlists/wordlist.txt", 'r')
for brute in bruteforce: 
    brute.strip()
    print(str(brute))
