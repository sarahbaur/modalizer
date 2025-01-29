import spacy

nlp = spacy.load('en_core_web_sm')


def classify_count_lines(line_list: list, name_set: set) -> tuple[dict, dict]:
    """
    Classify each line by the person who said it and count the number of words per person.

    :param line_list: list of lines to classify
    :param name_set: set of names in the text
    :return: tuple of dictionaries of lines per person and word counts per person
    """
    name_line_dict = {}
    name_word_count_dict = {}

    for name in sorted(name_set):
        name_lines = [line for line in line_list if line.startswith(f'{name}:')]
        name_line_dict[name] = name_lines
        # store count > only count of tokens that are not punctuation or the name itself
        name_word_count_dict[name] = sum(
            1 for line in name_lines
            for token in nlp(line)
            if token.pos_ != 'PUNCT' and token.text != name
        )

    return name_line_dict, name_word_count_dict


def classify_modality(lines: list) -> dict:
    """
    Classifies the modality of each modal verb from the input lines.

    :param lines: list of lines to classify
    :return: dictionary of counts of each modality classification
    """
    classification_dict = {
        'Ability': 0,
        'Prediction': 0,
        'Obligation': 0,
        'Advice': 0,
        'Permission': 0,
        'Volition': 0,
        'Unclassified': 0
    }

    for line in lines:
        doc = nlp(line)
        for token in doc:
            if token.tag_ == 'MD':
                # ABILITY: 'can' or 'could'; verb modifying; no negative context
                if (token.lemma_ in ['can', 'could'] and
                        token.head.pos_ == 'VERB' and
                        'not' not in [child.lemma_ for child in token.children]):
                    classification_dict['Ability'] += 1
                # PREDICTION: 'will', 'shall', 'would', 'should'; verb modifying; no negative context
                elif (token.lemma_ in ['will', 'shall', 'would', 'should'] and
                      token.head.pos_ == 'VERB' and
                      'not' not in [child.lemma_ for child in token.children]):
                    classification_dict['Prediction'] += 1
                # OBLIGATION: 'must', 'have to', 'ought to'
                elif token.lemma_ in ['must', 'have to', 'ought to']:
                    classification_dict['Obligation'] += 1
                # ADVICE: 'should', 'ought'
                elif token.lemma_ in ['should', 'ought']:
                    classification_dict['Advice'] += 1
                # PERMISSION: 'can', 'may', 'could'; sentence is a question
                elif token.lemma_ in ['can', 'may', 'could'] and doc[-1].text == '?':
                    classification_dict['Permission'] += 1
                # VOLITION 'will', 'would', 'want to'
                elif token.lemma_ in ['will', 'would', 'want to']:
                    classification_dict['Volition'] += 1
                else:
                    classification_dict['Unclassified'] += 1

    return classification_dict
