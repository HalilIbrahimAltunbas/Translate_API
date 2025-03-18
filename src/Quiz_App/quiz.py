
import random
import pandas
import requests
### this function was developed for testing purpose 
def quiz():
    ab = pandas.read_csv('./test.csv')
    
    # test = open('./test.txt','r').read()
    words = ab.values#test.split('\n')
    word = random.choice(words)
    chars = [*word[0]]
    
    # s2 : lambda x:  "Positive" if x > 0 else "Negative" if x < 0 else "Zero"
    s = random.sample(chars,k = random.randint(1, len(chars)//2)) 
    
    # x = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word[0]}',)  
    # print(x.json()[0]['meanings'][0]['definitions'][0]['definition'])
    
    chars = [(lambda a : a.replace(a,'_') if s.__contains__(a) else a)(a) for a in chars]
    # print(test)
    print(chars)
    print(f'hint {word[1]}')
    a = input('lütfen tahmin et : \n')
    if a.upper() == word[0].upper() :
        print('bildin')
        return
    print('bilemedin')


quiz()
