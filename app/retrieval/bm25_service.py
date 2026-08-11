import re
from rank_bm25 import BM25Okapi


class BM25Service:

    def __init__(self, documents: list[dict]):

        self.documents = documents

        self.tokenized_documents = [
            self._tokenize(document["text"])
            for document in documents
        ]

        self.bm25 = BM25Okapi(
            self.tokenized_documents
        )

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[dict]:

        query_tokens = self._tokenize(query)

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        results = []

        for index in ranked_indices[:top_k]:

            results.append({
                "text": self.documents[index]["text"],
                "metadata": self.documents[index]["metadata"],
                "bm25_score": float(scores[index])
            })

        return results

    def _tokenize(
        self,
        text: str
    ) -> list[str]:

        return re.findall(
            r"\b\w+\b",
            text.lower()
        )