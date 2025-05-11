
import random
import pandas
import requests
from flask import Flask, jsonify
# from Authentication.utils import auth_required
### this function was developed for testing purpose 

app = Flask(__name__)

@app.route('/quiz',methods = ['GET'])
# @auth_required
def quiz():
    ab = pandas.read_csv('./src/Quiz_App/test.csv')
    quest_count = 15
    words = ab.values
    word = random.sample([*words],k=quest_count)
    response : list[dict] = []
    print(word)
    for i in range(0,quest_count):
        chars = [*word[i][0]]
        sample = random.sample(chars,k = random.randint(len(chars)//3, len(chars)//2)) 
    
    # x = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word[0]}',)  
    # print(x.json()[0]['meanings'][0]['definitions'][0]['definition'])

        #{"soru": "E_a__le", "cevap": "Example"},
        chars = [(lambda char : char.replace(char,'_') if sample.__contains__(char) else char)(char) for char in chars]
        response.append({"soru": "".join(chars), "cevap": word[i][0],"hint":word[i][1]})
    
    # print(f'hint {word[1]}')

    return jsonify(response)




if __name__ == '__main__':
    # app.run(debug=True, port=5005)# host='0.0.0.0',
    app.run(host='0.0.0.0', port=5005)
