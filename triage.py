from ollama import chat
import json

with open("tickets.json", "r", encoding="UTF-8") as tickets:
    file = json.load(tickets)
    response = []
    for line in file:
        answer = chat(
            model='llama3.2:3b',
            messages=[{'role': "user", "content": "Trie les tickets suivants par le champ [category] : (bug, payment, account, suggestion, toxicity, autre), [severity] : (int de 1 à 5, 5 étant le plus urgent), [sentiment] : (positive, neutral, negative), [summary] : (une phrase courte résumant le sujet)." + str(line)}],
            format='json'
        )
        response.append((line, answer.message.content))
    response = json.dumps(response)
    with open("outputs/results.json", "w") as results:
        results.write(response)

        
