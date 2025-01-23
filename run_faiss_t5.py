from src.faiss_query_t5 import FaissQueryT5
from src.faiss_indexer import Indexer
from src.data_enum import Enum

indexer = Indexer()
indexer.save_faiss_index()

query = FaissQueryT5()

with open(Enum.ANSWERS_FILE, 'a') as file:
    file.write('Question: ' + str(query.ask_t5_via_question(query.default_question, query.default_context)) + '\n')
    file.write('\nPrompt: ' + str(query.ask_t5_via_prompt(query.default_prompt)) + '\n')
