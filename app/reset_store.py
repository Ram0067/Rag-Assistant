import shutil
import chromadb

def reset_chroma(delete_all: bool = False):
    """
    Safely reset Chroma vectorstore.

    Args:
        delete_all (bool): 
            - If True → deletes the entire 'vectorstore' folder (complete reset).
            - If False → deletes all collections inside the Chroma DB but keeps the folder.
    """
    client = chromadb.PersistentClient(path="vectorstore")

    if delete_all:
        # Completely remove the folder and all its data
        shutil.rmtree("vectorstore", ignore_errors=True)
        print("🧹 Deleted ENTIRE Chroma vectorstore (all collections + embeddings).")
    else:
        # Delete only individual collections
        collections = client.list_collections()
        if not collections:
            print("⚠️ No collections found in vectorstore.")
        else:
            for c in collections:
                print(f"🗑️ Deleting collection: {c.name}")
                client.delete_collection(c.name)
            print("✅ Deleted all Chroma collections (vectorstore folder retained).")

if __name__ == "__main__":
    # ✅ Change this to False if you only want to clear collections, not the entire folder
    reset_chroma(delete_all=True)

