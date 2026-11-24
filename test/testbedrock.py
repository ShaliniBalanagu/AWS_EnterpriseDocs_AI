import boto3

client = boto3.client(
    "bedrock-agent",
    region_name="ap-southeast-2"
)

response = client.list_knowledge_bases(
    maxResults=10
)

for kb in response["knowledgeBaseSummaries"]:
    print(kb["name"], kb["knowledgeBaseId"], kb["status"])