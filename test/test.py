import boto3
import os
import json
from dotenv import load_dotenv
from botocore.config import Config

# used to load environment variables from a .env file
load_dotenv()

client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    #os.environ.get("AWS_REGION"),
    #config=Config(
    #        retries={"mode": "adaptive", "total_max_attempts": 5}
     #   ),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)

print(os.getenv("BEDROCK_EMBED_MODEL"))

response= client.invoke_model(
    modelId=os.getenv("BEDROCK_EMBED_MODEL"),
    body=json.dumps({
        "inputText": "Amazon Bedrock",
        #"dimension": 1024,
        #"normalize": True,
    }),
    contentType="application/json",
    accept="application/json",
)

embedding_data = json.loads(response["body"].read())

print("Length of embedding vector:", len(embedding_data["embedding"]))


#Test 2: Amazon Nova Lite
chat_response = client.converse(
    modelId=os.getenv("BEDROCK_CHAT_MODEL"),
    messages=[
        {
            "role": "user",
            "content": [
                {"text": "Explain RAG in one sentence."}
            ]
        }
    ],
    inferenceConfig={"maxTokens": 200}
)


print("Chat Response:",chat_response["output"]["message"]["content"][0]["text"])






"""
embedding_data = json.loads(response["body"].read())
print("Embedding Data:", embedding_data)

#store the embeddings in pine cone vector database
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.index("insurance-rag")"""

#Test 1