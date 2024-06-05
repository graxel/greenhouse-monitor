long_list = list(range(1,31))
chunk_size = 10
overlap = 0.20

overlap_size = chunk_size * overlap

start_index = 0
while True:
    end_index = start_index + chunk_size
    sublist = long_list[start_index:end_index]
    print(sublist)
    start_index = int(end_index - overlap_size)
    if end_index >= len(long_list):
        break