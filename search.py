import os
from dataclasses import dataclass


class DB:
    def __init__(self):
        self.words_dict = get_data()


def get_data() -> dict[set[str]]:
    """
    Read all the files from the Resources.
    :return:A dictionary which each key is a word inside a file,
    and for each word a list of number of lines where contain this word.
    """
    word_dict = {}
    sentence_list = list(list())
    for root, dirs, files in os.walk('Archive'):
        for file in files:  # get each file within the directory and subdirectories
            path = (os.path.abspath(os.path.join(root, file)))  # get the full path of each file
            with open(path, encoding="utf8") as f:  # open the file
                line_num = 0
                for line in f:
                    line_num += 1
                    sentence_list.append([line, file[:-4], line_num])
                    for word in line.split(" "):  # every word separated by space
                        word = word.lower()
                        if word not in word_dict.keys():
                            word_dict[word] = set()
                        word_dict[word].add(line)  # add the line to the key word
    print(sentence_list)
    return word_dict

get_data()

@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int

    def __init__(self, completed_sentence, source_text, offset, score):
        self.completed_sentence = completed_sentence
        self.source_text = source_text
        self.offset = offset
        self.score = score

    def print(self):
        print(self.completed_sentence)


def get_best_k_completions(prefix: str) -> list[str]:
    results = []
    data = get_data()
    prefix = prefix.lower()
    user_search_list = prefix.split(" ")
    for sentence in data[user_search_list[0]]:
        if sentence.lower().find(prefix) != -1:
            results.append(sentence)
            if len(results) == 5:
                break
    return results


def print_user_input() -> None:
    user_search = input('Enter your text:')
    for result in get_best_k_completions(user_search):
        print(result)


#print_user_input()
