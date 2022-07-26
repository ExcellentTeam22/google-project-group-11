import os


def get_data() -> dict[list[int]]:
    """
    get_data function read all the files in the Resources, inside all directory and
    subdirectories.
    :return: A dictionary that each key is a word inside a file, and for each word a list of
        lines that contain that word (the line is converted to hash)
    """
    word_dict = {}
    for root, dirs, files in os.walk('resources'):
        for file in files:  #get each file within the directory and subdirectories
            path = (os.path.abspath(os.path.join(root, file)))  #get the full path of each file
            with open(path, encoding="utf8") as f:  #open the file
                for line in f:
                    for word in line.split(" "):    #every word seperated by space
                        if word not in word_dict.keys():
                            word_dict[word] = []
                        word_dict[word].append(hash(line)) #add the line to the key word
    return word_dict