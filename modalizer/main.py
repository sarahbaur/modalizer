"""
Count the number of modals for each person appearing in the dialogue/text.
If the --example flag is indicated, provide an example sentence for each unique modal (per person).
If the --categorize flag is indicated, split the modal verbs into categories (based on linguistic research).

Please find sample program calls in the README.md file.
"""


from typing import TextIO, List, Optional
from argparse import ArgumentParser, FileType

import spacy
import time

from memory_profiler import memory_usage

from modalizer.dictionaries import get_modals_counts_lemmas_lines, get_modal_examples
from modalizer.classifications import classify_count_lines, classify_modality


nlp = spacy.load("en_core_web_sm")


def process_lines(file: TextIO) -> List[str]:
    """Read the lines of a file and return them as a list."""
    return [line.rstrip('\n') for line in file]


def get_names(line_list: list) -> set:
    """Store all dialogue names in the text in a list."""
    return {name.rstrip(':') for name in (line.split(' ')[0] for line in line_list)}


def pretty_print(
    modal_counts_dict: dict,
    word_count_dict: dict,
    examples_dict: Optional[dict] = None,
    classify_modals: Optional[dict] = None
) -> None:
    """
    Format results for console output.

    :param modal_counts_dict: dictionary of modal counts per person
    :param word_count_dict: dictionary of word counts per person
    :param examples_dict: dictionary of examples per person, only present with -e flag
    :param classify_modals: dictionary of modal categories per person, only present with -c flag
    """
    print('\n' + "=" * 80)
    for person, modal_count in modal_counts_dict.items():
        if modal_count > 0:
            word_count = word_count_dict[person]
            norm_count = modal_count / word_count * 1000  # normalize modal count per 1000 words
            print(
                '\n\033[1;34m' + "{:<10s}".format(person) + '\033[0m\n' + "-" * 80
            )
            print(
                'Number of modals: ' + '\033[1;32m' + "{:3d}".format(modal_count) + '\033[0m'
            )
            print(
                'Normalized (by 1000 words): ' + '\033[1;32m' + "{:.2f}".format(round(norm_count, 2)) + '\033[0m'
            )

            if examples_dict and person in examples_dict:  # if -e, print examples
                examples = examples_dict[person]
                print('\n\033[1;33mExamples:\033[0m')

                for lemma, example in examples.items():  # using replace to avoid things like AmeriCAN
                    print(
                        '\t' + "{:10s}".format(lemma) + ' ' + example.replace(
                            lemma, "\033[1;31m" + "{}".format(lemma) + "\033[0m", 1
                        )
                    )

            if classify_modals and person in classify_modals:  # if -c, print classification
                print('\n\033[1;33mModal classification:\033[0m')
                for modal, count in classify_modals[person].items():
                    percentage = count / modal_count * 100  # calculate percentage of modal
                    formatted_modal = "{:10s}".format(modal)
                    formatted_count = "{:5d}".format(count)
                    formatted_percentage = "{:.2f}%".format(round(percentage, 2))
                    if percentage > 0:  # highlight if percentage is > 0
                        print(
                            '\t' + formatted_modal + '\t' + formatted_count +
                            '\tThis is \033[1;31m' + formatted_percentage + '\033[0m' + ' of all modals.'
                        )
                    else:
                        print(
                            '\t' + formatted_modal + '\t' + formatted_count +
                            '\tThis is ' + formatted_percentage + ' of all modals.'
                        )

    print('\n' + "=" * 80 + '\n')


def main():
    # measure the start time
    start_time = time.time()
    # measure the start memory
    start_memory = memory_usage()[0]

    # define console argument parser
    parser = ArgumentParser(
        description="Identifies modal auxiliaries in debate/dialogue files and computes their frequency."
    )
    parser.add_argument(
        'filename',
        type=FileType('r', encoding='UTF-8'),
        help="The file containing the text to be analyzed, in dialogue format as specified in the README."
    )
    parser.add_argument(
        '-e',
        '--example',
        action='store_true',
        help='Prints an example sentence for each modal auxiliary.'
    )
    parser.add_argument(
        '-c',
        '--categorize',
        action='store_true',
        help='Groups the modal auxiliary verbs into categories and returns counts.'
    )
    # parse console argument
    args = parser.parse_args()

    # call functions and supply arguments
    processed_file = process_lines(args.filename)
    name_set = get_names(processed_file)
    name_line_dict, name_word_count_dict = classify_count_lines(processed_file, name_set)
    person_modal_dict, modal_counts_dict, person_lemma_dict, processed_lines_dict = \
        get_modals_counts_lemmas_lines(name_line_dict)
    examples_dict = get_modal_examples(person_lemma_dict, processed_lines_dict) if args.example else None

    # if -c, call the classify_modality function per person
    classification_counts = {}
    if args.categorize:
        for person, lines in name_line_dict.items():
            classification_counts[person] = classify_modality(lines)
    pretty_print(modal_counts_dict, name_word_count_dict, examples_dict, classification_counts)

    # measure the end time
    end_time = time.time()
    # measure the end memory
    end_memory = memory_usage()[0]
    # round execution time and memory usage to 2 decimals in nice print statement
    print(f"Execution time: {round(end_time - start_time, 2)} seconds")
    print(f"Memory usage: {round(end_memory - start_memory, 2)} MB")


if __name__ == '__main__':
    main()
