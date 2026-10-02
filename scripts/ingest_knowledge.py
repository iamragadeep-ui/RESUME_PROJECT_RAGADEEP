from pathlib import Path

from app.rag.knowledge import KnowledgeAgent


def main() -> None:
    data_dir = Path(__file__).resolve().parents[1] / "data" / "knowledge_base"
    agent = KnowledgeAgent()
    for file_path in data_dir.glob("*.txt"):
        agent.ingest_file(str(file_path))
        print(f"Ingested {file_path.name}")


if __name__ == "__main__":
    main()
