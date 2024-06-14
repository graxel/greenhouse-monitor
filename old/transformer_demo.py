# from transformers import BertModel, BertTokenizer
from scipy.spatial.distance import cosine
import torch

import fil

# # Load pre-trained BERT model and tokenizer
# model_name = 'bert-base-uncased'
# tokenizer = BertTokenizer.from_pretrained(model_name)
# model = BertModel.from_pretrained(model_name)

user_id = 1
how_recent = '3 days'

print('checking db', flush=True)
unvectored_jobs = fil.sql("""
    SELECT
        jobs.job_id,
        jobs.description
    FROM jobs
    LEFT JOIN vectors
    ON jobs.job_id = vectors.job_id
    WHERE vectors.vector IS null
    LIMIT 3
    ;""")
print('finished', flush=True)

# the_latest_jobs = fil.sql("""
#     SELECT
#         jobs.scraped_at,
#         jobs.company_name,
#         jobs.job_title,
#         jobs.location,
#         jobs.job_page_url,
#         vectors.vector
#     FROM application_history
#     LEFT JOIN vectors
#     ON vectors.job_id = application_history.job_id
#     WHERE jobs.scraped_at >= CURRENT_DATE - INTERVAL %s
#     ;""", (how_recent,))

# jobs_applied_to = fil.sql("""
#     SELECT
#         vectors.job_id,
#         vectors.vector
#     FROM application_history
#     LEFT JOIN vectors
#     ON vectors.job_id = application_history.job_id
#     WHERE application_history.user_id = %s
#     ;""", (user_id,))

from transformers import LongformerTokenizer, LongformerModel
import torch

print('loading model')
# Load pretrained Longformer model and tokenizer
model_name = 'allenai/longformer-base-4096'
tokenizer = LongformerTokenizer.from_pretrained(model_name)
model = LongformerModel.from_pretrained(model_name)


# Tokenize and obtain embeddings for each document
document_embeddings = []

for job in unvectored_jobs:
    
    description = job[1]
    print (description)
    # Tokenize and obtain embeddings
    tokens = tokenizer(description, return_tensors='pt', padding=True, truncation=True)


    chunk_size = 512
    overlap = 0.20

    overlap_size = chunk_size * overlap

    start_index = 0
    chunk_embeddings = []
    while True:
        end_index = start_index + chunk_size

        chunk = tokens[start_index:end_index]
        outputs = model(**chunk)
        embeddings = outputs.last_hidden_state
        print('len of embeddings:', len(embeddings))
        print('len of embeddings[0]:', len(embeddings[0]))
        print('embeddings:', embeddings)
        # Apply mean pooling or other aggregation methods if needed
        chunk_embedding = torch.mean(embeddings, dim=1)
        print('chunk_embedding:', chunk_embedding)
        chunk_embeddings.append(chunk_embedding)

        start_index = int(end_index - overlap_size)
        if end_index >= len(tokens):
            break

    # Aggregate chunk embeddings if needed
    document_embedding = torch.cat(chunk_embeddings, dim=0)


    print('document_embedding:', document_embedding,'\n~\n')

    # Append document_embedding to the list
    # document_embeddings.append(document_embedding)

# Convert the list of document embeddings to a tensor
# document_embeddings_tensor = torch.stack(document_embeddings)


# print(document_embeddings_tensor)


# count = 0
# for job in unvectored_jobs:

    # print('.', end='', flush=True)
    # count += 1
    # if count % 100 == 0:
    #     print(flush=True)

    # description = job[1]
    # print(description, flush=True)

    # print('tokenizing')
    # tokens = tokenizer(description, return_tensors='pt')
    # print(len(tokens), flush=True)
    # embedding = model(**tokens).last_hidden_state.mean(dim=1).detach().numpy().flatten()
    # pickled_embedding = pickle.dumps(embedding)
    # fil.sql("""
    #     INSERT INTO vectors (job_id, vector)
    #     VALUES (%s, %s))
    #     ;""", (job[0], pickled_embedding)
    # )



# # Compute the average embedding of the reference sentences
# average_embedding = torch.tensor(description_embeddings).mean(dim=0).numpy()

# # Tokenize and encode the other sentences for comparison
# tokenized_others = [tokenizer(sentence, return_tensors='pt') for sentence in other_sentences]

# # Forward pass through the BERT model to get embeddings for other sentences
# embedding_others = [model(**tokens).last_hidden_state.mean(dim=1).detach().numpy().flatten() for tokens in tokenized_others]

# # Compute cosine similarity scores to the average embedding
# similarity_scores = [1 - cosine(embedding, average_embedding) for embedding in embedding_others]


# # Print the similarity scores
# for i, score in enumerate(similarity_scores):
#     print(f"Similarity score for text {i + 1}: {score:.4f}")







# # Tokenize and encode the texts
# tokenized_texts = [tokenizer(text, return_tensors='pt') for text in texts]

# # Forward pass through the BERT model to get embeddings
# embeddings = [model(**tokens).last_hidden_state.mean(dim=1) for tokens in tokenized_texts]

# # Convert embeddings to a list of numpy arrays
# embedding_arrays = [embedding.detach().numpy() for embedding in embeddings]
# # Print the vector representations for each text
# for i, embedding_array in enumerate(embedding_arrays):
#     print(f"Vector representation for text {i + 1}:\n{len(embedding_array[0])}\n")
