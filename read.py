def read(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except Exception as e:
        print(e)
        return