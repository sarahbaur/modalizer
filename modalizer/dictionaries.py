from collections import defaultdict
import spacy

nlp = spacy.load("en_core_web_sm")


def get_modals_counts_lemmas_lines(name_line_dict: dict) -> tuple[dict, dict, dict, dict]:
    """Collects modal counts, modal verbs, and lemmas from the processed lines of each person."""
    modal_counts_dict = {}
    person_modal_dict = defaultdict(set)
    person_lemma_dict = defaultdict(set)
    processed_lines_dict = {}  # Storing processed lines to avoid re-processing them later

    for person, lines in name_line_dict.items():
        processed_lines = [nlp(line) for line in lines]
        # store tokens in list if spacy tags them as modal verbs (MD)
        all_modals = [token for doc in processed_lines for token in doc if token.tag_ == 'MD']
        for modal in all_modals:
            person_modal_dict[person].add(modal.text)
            person_lemma_dict[person].add(modal.lemma_)
        modal_counter = len(all_modals)
        # store these variables as dictionary values, with the person name as the key
        modal_counts_dict[person] = modal_counter
        processed_lines_dict[person] = processed_lines

    return person_modal_dict, modal_counts_dict, person_lemma_dict, processed_lines_dict


def get_modal_examples(person_lemma_dict: dict, processed_lines_dict: dict) -> dict:
    """
    Gets examples of modal verbs from the processed lines of each person.

    :param person_lemma_dict: dictionary mapping person names to sets of modal lemmas.
    :param processed_lines_dict: dictionary mapping person names to lists of processed lines.
    :return: dictionary mapping person names to dictionaries mapping modal lemmas to example sentence.
    """
    examples_dict = {}

    for person, lemmas in person_lemma_dict.items():
        lemma_examples = {}
        for lemma in lemmas:
            for doc in processed_lines_dict[person]:
                for sent in doc.sents:
                    sentence = sent.text
                    # Remove person name prefix from sentence
                    if sentence.startswith(f'{person}:'):
                        sentence = sentence[len(person) + 1:].strip()
                    for token in sent:
                        # Check if the token is a modal verb or a contraction
                        # to eliminate cases like AmeriCAN
                        if token.tag_ == 'MD' and (
                            token.text == lemma or
                            (token.lemma_ == lemma and not token.is_alpha)
                        ):
                            # the contraction would not solely be alphabetic because of the apostrophe
                            lemma_examples[lemma] = sentence
                            break

        examples_dict[person] = lemma_examples
    return examples_dict
