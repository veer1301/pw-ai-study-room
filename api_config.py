import os
from dotenv import load_dotenv
load_dotenv()
auto_offset = "earliest"
chat_api_key=os.getenv('AZURE_GPT_KEY')
chat_api_base = os.getenv('AZURE_GPT_URL')
chat_api_version=os.getenv('AZURE_GPT_VERSION')
chat_model = os.getenv('AZURE_GPT_MODEL')

chat_server_address=os.getenv('KAFKA_BROKERS')
chat_username=os.getenv('KAFKA_SA_KEY')
chat_password=os.getenv('KAFKA_SA_SECRET')
chat_group_id=os.getenv('KAFKA_GROUP_ID')

chat_embedding_azure_endpoint =os.getenv('AZURE_EMB_URL')
chat_embedding_api_key=os.getenv('AZURE_EMB_KEY')
chat_embedding_name = os.getenv('AZURE_EMB_MODEL')
chat_input_topic_name  = "chat-text-input-topic"
chat_output_topic_name = "chat-text-output-topic"
chat_output_log_topic_name="chat-text-output-log"