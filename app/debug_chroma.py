from chromadb import PersistentClient

client = PersistentClient(path="vectorstore")

print("📂 Available Collections:")
for c in client.list_collections():
    print("-", c.name)
