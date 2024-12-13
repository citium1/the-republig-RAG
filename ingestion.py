from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import time

try:
    # Initialize Pinecone
    print("Initializing Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Get list of existing indexes
    existing_indexes = pc.list_indexes().names()
    print(f"Existing indexes: {existing_indexes}")
    
    # Delete existing index if it exists
    if INDEX_NAME in existing_indexes:
        print(f"Deleting existing index: {INDEX_NAME}")
        pc.delete_index(INDEX_NAME)
        time.sleep(10)  # Wait for deletion to complete
    
    # Create new index with starter (free tier) configuration
    print(f"Creating new index: {INDEX_NAME}")
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
    
    print("Waiting for index to initialize...")
    time.sleep(20)  # Wait longer for index to be fully ready
    
    # Get the index
    index = pc.Index(INDEX_NAME)
    
    # Load the PDF documents
    print("Loading PDF documents...")
    loader = PyPDFLoader("../data/the_republic_plato.pdf")
    documents = loader.load()

    # Split documents into chunks
    print("Splitting documents into chunks...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    # Create embeddings
    print("Creating embeddings...")
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    # Create vectors and upsert them directly to Pinecone
    print("Creating and upserting vectors...")
    for i, text in enumerate(texts):
        # Create embedding for the text
        vector = embeddings.embed_query(text.page_content)
        
        # Create metadata
        metadata = {
            "text": text.page_content,
            **text.metadata
        }
        
        # Upsert to Pinecone
        index.upsert(vectors=[(str(i), vector, metadata)])
        
        if i % 10 == 0:  # Print progress every 10 documents
            print(f"Processed {i} documents...")

    print("Process completed successfully!")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Type of error:", type(e))
    raise e