from vectorai import ViClient 
vi_client = ViClient()
cn = 'test_cn'
docs = vi_client.create_sample_documents(10)
vector_field = 'item_tf-auto-transofmers_vector_'
{x.update({vector_field: vi_client.generate_vector(15)}) for x in docs}

vi_client.insert_documents(cn, docs)
print(vi_client.search(cn, vi_client.generate_vector(15), vector_field))
