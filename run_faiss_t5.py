from src.faiss_query_t5 import FaissQueryT5
from src.faiss_indexer import Indexer
from src.data_enum import Enum

indexer = Indexer()
indexer.save_faiss_index()

query = FaissQueryT5()

options = [f'Default: {query.default_prompt}', f'Default: {query.default_question}', 'My question']

while True:
    print('\nSelect option:')
    position = 1
    for option in options:
        print(str(position) + '. ' + option)
        position += 1

    question_or_default = input('Your choice: ')

    if question_or_default == '1':
        question, answer = query.ask_t5_via_prompt(query.default_prompt + query.default_following_data)
    elif question_or_default == '2':
        question, answer = query.ask_t5_via_question(query.default_question, query.default_context)
    elif question_or_default == '3':
        prompt = input('Your question: ')
        prompt.join('. Use following data: ')
        question, answer = query.ask_t5_via_prompt(prompt + query.default_following_data)

    if question_or_default in ['1', '2', '3']:
        with open(Enum.ANSWERS_FILE, 'a') as file:
            file.write(f'\nQuestion: {question} \n Answer: {answer}')
    else:
        print('Incorrect option.')
