from sys import argv

if __name__ == "__main__":
    try:
        if len(argv) < 2:
            raise ValueError("You need to provide the file configuration")
        if len(argv > 2):
            raise ValueError("No more that the programme name and config file should be provide")
    except Exception as e:
        print(e)