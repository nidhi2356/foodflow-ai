from app.data.document_builder import build_documents
from app.reranking.service import RerankerService


reranker = RerankerService()

query = "healthy high protein vegetarian dinner"

documents = build_documents()

document_texts = [
    document["text"]
    for document in documents
]

results = reranker.rerank(
    query,
    document_texts
)

for document, score in results:
    print(f"\nScore: {score:.4f}")
    print(document)