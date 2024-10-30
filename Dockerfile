
FROM python:3.12-slim


WORKDIR /app


COPY . /app


RUN pip install -r requirements.txt


EXPOSE 8501


CMD ["sh", "-c", "python3 inserting_json_documents_into_mongodb.py && python3 storing_index_into_mongodb_collection.py && streamlit run rag_system.py --server.port 8501"]


