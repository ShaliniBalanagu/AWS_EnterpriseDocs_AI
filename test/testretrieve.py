import boto3

client = boto3.client(
    "bedrock-agent-runtime",
    region_name="ap-southeast-2"
)

response = client.retrieve(
    knowledgeBaseId="CZGLUU6RCV",
    retrievalQuery={
        "text": "What is the company report about?"
    },
    retrievalConfiguration={
        "managedSearchConfiguration": {
            "numberOfResults": 5
        }
    }
)

for result in response["retrievalResults"]:
    print(result["content"]["text"][:300])
    print("----------------")