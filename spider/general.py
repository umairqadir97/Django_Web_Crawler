import os
import urllib.parse


# Create queue and crawled files (if not created)
def create_data_files(base_url, queue, crawled):
    write_file(queue, base_url)
    write_file(crawled, '')


# Create a new file
def write_file(path, data):
    with open(path, "w") as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, "a") as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    f = open(path, "w")
    f.close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, "rt") as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    # delete_file_contents(file_name)
    # for link in sorted(links):
    #   append_to_file(file_name, link)
    with open(file_name, "w") as f:
        for l in sorted(links):
            f.write(l+"\n")

