def read_file(path):
    file = open(path)
    try:
        contents = file.read()
    finally:
        file.close()
    return contents
