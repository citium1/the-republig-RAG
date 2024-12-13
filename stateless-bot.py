from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as LangchainPinecone



try:
    # Initialize Pinecone
    print("Initializing Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Get the index
    print("Getting Pinecone index...")
    index = pc.Index(INDEX_NAME)

    # Initialize OpenAI embeddings
    print("Initializing OpenAI embeddings...")
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    # Create a retriever from the index
    print("Creating vector store...")
    vectorstore = LangchainPinecone(index, embeddings.embed_query, "text")

    # Initialize the ChatOpenAI model
    print("Initializing ChatOpenAI...")
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model_name="gpt-3.5-turbo",
        temperature=0
    )

    # Create a retrieval chain
    print("Creating retrieval chain...")
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )

    # Chat history
    chat_history = []

    print("\nReady for questions!")
    print("="*50 + "\n")

    # Main loop
    while True:
        # Get user input
        question = input("Ask a question (or type 'exit' to quit): ")
        
        # Check for exit condition
        if question.lower() == 'exit':
            break
        
        # Get response from the chain
        result = qa_chain({"question": question, "chat_history": chat_history})
        
        # Print the answer
        print("\nAnswer:", result["answer"])
        
        # Print sources if available
        if result.get("source_documents"):
            print("\nSources:")
            for doc in result["source_documents"]:
                print("- Page", doc.metadata.get("page", "unknown"))
        
        # Update chat history
        chat_history.append((question, result["answer"]))
        print("\n" + "="*50 + "\n")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Type of error:", type(e))
    raise e