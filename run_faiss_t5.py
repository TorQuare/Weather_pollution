from src.faiss_query_t5 import FaissQueryT5
from src.faiss_indexer import Indexer

indexer = Indexer()
indexer.save_faiss_index()

query = FaissQueryT5()
query.ask_t5_via_question(query.question)

query.ask_t5_via_prompt(query.prompt)
