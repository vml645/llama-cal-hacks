import subprocess
from llama_stack_client import Agent, AgentEventLogger, RAGDocument, LlamaStackClient

def terminal_call(command: str) -> str:
    """Run the command in a shell and return its stdout."""
    print(f"Executing command: {command}")
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=True
    )
    output = result.stdout.strip()
    print(f"Command output: {output}")
    return output

def setup_agent(vector_db_id="my_demo_vector_db", base_url="http://localhost:8321"):
    client = LlamaStackClient(base_url=base_url)
    models = client.models.list()

    # Select the first LLM and first embedding models
    model_id = next(m for m in models if m.model_type == "llm").identifier
    embedding_model_id = (
        em := next(m for m in models if m.model_type == "embedding")
    ).identifier
    embedding_dimension = em.metadata["embedding_dimension"]

    _ = client.vector_dbs.register(
        vector_db_id=vector_db_id,
        embedding_model=embedding_model_id,
        embedding_dimension=embedding_dimension,
        provider_id="faiss",
    )

    agent = Agent(
        client,
        model=model_id,
        instructions="You are a helpful assistant that can execute terminal commands when needed. Be careful with command execution and only run safe commands.",
        tools=[
            {
                "name": "builtin::rag/knowledge_search",
                "args": {"vector_db_ids": [vector_db_id]},
            },
            {
                "name": "builtin::code_interpreter",
                "args": {},
            }
        ],
    )
    
    return agent, client

def ingest_document(client, vector_db_id, source):
    print(f"rag_tool> Ingesting document: {source}")
    document = RAGDocument(
        document_id="document_1",
        content=source,
        mime_type="text/html",
        metadata={},
    )
    client.tool_runtime.rag_tool.insert(
        documents=[document],
        vector_db_id=vector_db_id,
        chunk_size_in_tokens=50,
    )

def interactive_session():
    agent, client = setup_agent()
    session_id = agent.create_session("interactive_session")
    
    print("\nWelcome to the Interactive Agent!")
    print("Type 'exit' or 'quit' to end the session")
    print("Type your question and press Enter to get a response\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye!")
                break
                
            if not user_input:
                continue
                
            response = agent.create_turn(
                messages=[{"role": "user", "content": user_input}],
                session_id=session_id,
                stream=True,
            )
            
            print("\nAssistant: ", end="")
            for log in AgentEventLogger().log(response):
                log.print()
            print("\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    interactive_session() 