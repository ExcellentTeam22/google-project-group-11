from AutoCompleteData import AutoCompleteData
import Data
import Sentence

data = Data.Data()


def get_best_k_completions(prefix: str) -> list[AutoCompleteData]:
    misspelled_words_counter, misspelled_word, intersection_of_lines = find_perfect_match(prefix)
    if misspelled_words_counter == 0:
        return find_complete_sentence(prefix, intersection_of_lines)[:5]
    # elif misspelled_words_counter == 1:
    #     Search.try_to_fix_word(prefix, misspelled_word, intersection_of_lines)


def find_perfect_match(prefix: str) -> tuple[int, str, set[int]]:
    intersection_of_lines = set()
    misspelled_words_counter = 0
    misspelled_word = ''
    prefix_list = prefix.lower().split(" ")
    for word in prefix_list:
        numbers_of_lines = data.get_data_word_to_sentence(word)
        if numbers_of_lines:
            intersection_of_lines = make_intersection(intersection_of_lines, numbers_of_lines)
        else:
            misspelled_words_counter += 1
            misspelled_word = word

    return misspelled_words_counter, misspelled_word, intersection_of_lines


def make_intersection(intersection_of_lines: set[int], numbers_of_lines: set[int]) -> set[int]:
    if intersection_of_lines:
        intersection_of_lines = intersection_of_lines.intersection(numbers_of_lines)
    else:
        intersection_of_lines = numbers_of_lines
    return intersection_of_lines


def find_complete_sentence(prefix: str, intersection_of_lines: set[int]) -> list[AutoCompleteData]:
    results = list()
    for line in intersection_of_lines:
        offset = data.get_data_sentence_to_file(line).get_sentence().find(prefix)
        if offset != -1:
            results.append(AutoCompleteData(
                           data.get_data_sentence_to_file(line).get_sentence(),
                           data.get_data_sentence_to_file(line).get_file_name(),
                           offset, 0))
    return results


#     for id in numbers_of_lines:
#     #for id in make_intersection(prefix_list):
#         sentence = data.get_data_sentence_to_file(id)
#         if sentence.get_sentence().lower().find(prefix) != -1:
#             results.append(AutoCompleteData(id, prefix, sentence.get_sentence(), sentence.get_line(), 0, sentence.get_file_name()))

#def get_score(sentence: str, list: list[bool, ])

#
# def get_best_k_completions(input : str) -> list[str]:
#     """
#     :param input:
#     :return:
#     """
#     perfect_list = get_perfect_match(input)
#     perfect_list = list()
#     #perf_list = list()
#     max_score = 0
#     #if len(perfect_list) != 0:
#     input_by_words = input.split(" ")
#     for i in range(len(input_by_words)):
#         prefix = input_by_words[:i]
#         suffix = input_by_words[i+1:]
#         full_prefix_string = ' '.join(map(str, prefix))
#         full_suffix_string = ' '.join(map(str, suffix))
#         prefix_list = get_perfect_match(full_prefix_string)
#         suffix_list = get_perfect_match(full_suffix_string)
#         if len(prefix_list) == 0 or len(suffix_list) == 0:
#             continue
#
#         prefix_set = get_id_set(prefix_list)
#         suffix_set = get_id_set(suffix_list)
#         possible_match_list = prefix_set.intersection(suffix_set)
#         for id in possible_match_list:
#             sentence = data.get_data_sentence_to_file(id).get_sentence()
#             sentence = sentence.lower()
#             prefix_index = sentence.find(' ' + full_prefix_string.lower() + ' ')
#             suffix_index = sentence.find(' ' + full_suffix_string.lower() + ' ')
#             if prefix_index < suffix_index:
#                 fix_parameters = fix_words(input_by_words[i], sentence[prefix_index + len(full_prefix_string) + 2: suffix_index])
#                 if fix_parameters[0] is True:
#                     perfect_list.append(sentence)
#                 if len(perfect_list) == 5:
#                     return perfect_list
#     return perfect_list


def get_id_set(li :list[AutoCompleteData]) -> set[int]:
    sentence_id_set = set()
    for item in li:
        sentence_id_set.add(item.get_id())
    return sentence_id_set


def print_user_input() -> None:
    user_search = ""
    while user_search != "#":
        user_search = input('Enter your text:')
        counter = 0
        list = get_perfect_match(user_search)
        if len(list) != 0:
            for result in list:
                counter += 1
                if counter == 6:
                    break
                print(str(counter) + ". " + result.get_str())
        else:
            for result in get_best_k_completions(user_search):
                counter += 1
                print(str(counter) + ". " + result)
        print("\n")

def fix_by_delete(target_word: str, wanted_word: str) -> str:
    """
    Find if it's possible to fix the target word to wanted word by delete only one of the letters.
    :param target_word: Target word to fix
    :param wanted_word: wanted word to fix the target word to
    :return: Index of the change in the target_word, -1 otherwise.
    """
    for i in range(1, len(target_word)):
        if target_word[:i] + target_word[i + 1:] in wanted_word:
            return i
    return -1


def fix_by_add_letter(target_word: str, wanted_word: str) -> str:
    """
    Find if it's possible to fix the target word to wanted word by add only one letter inside target word.
    :param target_word: Target word to fix
    :param wanted_word: wanted word to fix the target word to
    :return:Index of the change in the target_word, -1 otherwise.
    """
    if len(target_word)+1 != len(wanted_word):
        return [False, 0, 0]
    if target_word[0] == wanted_word[0] and len(target_word) == 1:
        return [True, 1, 1]

    for i in range(1, len(target_word)):
        if target_word[:i] == wanted_word[:i] and target_word[i:] == wanted_word[i + 1:]:
            return i
    return -1


def fix_by_change_letter(target_word: str, wanted_word: str) -> str:
    """
    Find if it's possible to fix the target word to wanted word by change only one letter inside target word.
    :param target_word: Target word to fix.
    :param wanted_word: wanted word to fix the target word to.
    :return: Index of the change in the target_word, -1 otherwise.
    """
    for i in range(len(target_word)):
        if target_word[:i] == wanted_word[:i] and target_word[i + 1:] == wanted_word[i + 1:]:
            return i
    return -1


def fix_words(target_word: str, wanted_word: str) -> list:
    """
    Check if can fix target_word to wanted_word by delete, add_letter or change_letter,
    retrun list contain
    1)True/false if can fix the word by 1 change
    2)Index of the fix in the word
    3)Which change we fic the word by delete, add_letter or change_letter.
    :param target_word: Target word to fix
    :param wanted_word: wanted word to fix the target word to.
    :return: list- True/False, Index of fix, kind of fix
    """
    if target_word == wanted_word:
        return [True, 0, 0]
    if len(wanted_word.split(" ")) != 1:
        return [False, 0, 0]
    fix_index = fix_by_delete(target_word, wanted_word)
    if fix_index != -1:
        return [True, fix_index, 1]
    fix_index = fix_by_add_letter(target_word, wanted_word)
    if fix_index != -1:
        return [True, fix_index, 2]
    fix_index = fix_by_delete(target_word, wanted_word)
    if fix_index != -1:
        return [True, fix_index, 3]
    return [False, 0, 0]


