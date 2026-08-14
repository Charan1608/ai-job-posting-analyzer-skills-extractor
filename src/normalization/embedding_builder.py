"""
=========================================================
ESCO EMBEDDING BUILDER
AI-Powered Job Posting Analyzer
=========================================================
"""

from pathlib import Path
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

from src.normalization.taxonomy_loader import ESCOTaxonomy


MODEL_NAME = "all-MiniLM-L6-v2"

OUTPUT_DIR = Path("models/embeddings")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_FILE = OUTPUT_DIR / "esco_embeddings.npy"
METADATA_FILE = OUTPUT_DIR / "esco_metadata.pkl"


class EmbeddingBuilder:

    def __init__(self):

        print("=" * 60)
        print("LOADING ESCO")
        print("=" * 60)

        taxonomy = ESCOTaxonomy()
        taxonomy.load()
        taxonomy.build_lookup()

        self.skills = taxonomy.skills

        print("\nLoading SentenceTransformer model...")
        self.model = SentenceTransformer(MODEL_NAME)

    def build(self):

        print("\nPreparing skill texts...")

        texts = (
            self.skills["preferredLabel"]
            .fillna("")
            .astype(str)
            .tolist()
        )

        print(f"Encoding {len(texts):,} ESCO skills...")

        embeddings = self.model.encode(

            texts,

            show_progress_bar=True,

            batch_size=64,

            convert_to_numpy=True,

            normalize_embeddings=True

        )

        np.save(EMBEDDING_FILE, embeddings)

        metadata = []

        for _, row in self.skills.iterrows():

            metadata.append({

                "preferred_label": row["preferredLabel"],

                "concept_uri": row["conceptUri"],

                "skill_type": row["skillType"],

                "definition": ""
                if str(row["definition"]) == "nan"
                else str(row["definition"])

            })

        with open(METADATA_FILE, "wb") as f:

            pickle.dump(metadata, f)

        print("\n" + "=" * 60)
        print("DONE")
        print("=" * 60)

        print(f"Embeddings : {EMBEDDING_FILE}")
        print(f"Metadata   : {METADATA_FILE}")
        print(f"Vectors    : {embeddings.shape}")


if __name__ == "__main__":

    builder = EmbeddingBuilder()

    builder.build()