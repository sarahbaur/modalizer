import pytest
import spacy

from modalizer.dictionaries import get_modals_counts_lemmas_lines, get_modal_examples

nlp = spacy.load("en_core_web_sm")


def test_get_modals_counts_lemmas_lines():
    # input
    name_line_dict = {
        "CLINTON": [
            "CLINTON: You may want to change that.",
            "CLINTON: If I could change that."
        ],
        "COOPER": [
            "COOPER: You might want to say that again.",
            "COOPER: What is your problem."
        ],
        "RADDATZ": ["RADDATZ: I'll be careful"],
        "TRUMP": [
            "TRUMP: What would you want to change?.",
            "TRUMP: I ought to.",
            "TRUMP: How about tomorrow?"
        ]
    }

    # output
    name_modal_dict = {
        'CLINTON': {'may', 'could'},
        'COOPER': {'might'},
        'RADDATZ': {"'ll"},
        'TRUMP': {'would', 'ought'}
    }
    name_count_dict = {
        'CLINTON': 2,
        'COOPER': 1,
        'RADDATZ': 1,
        'TRUMP': 2
    }
    name_lemma_dict = {
        'CLINTON': {'may', 'could'},
        'COOPER': {'might'},
        'RADDATZ': {'will'},
        'TRUMP': {'would', 'ought'}
    }

    # test
    assert isinstance(get_modals_counts_lemmas_lines(name_line_dict), tuple)
    assert get_modals_counts_lemmas_lines(name_line_dict)[0] == name_modal_dict
    assert get_modals_counts_lemmas_lines(name_line_dict)[1] == name_count_dict
    assert get_modals_counts_lemmas_lines(name_line_dict)[2] == name_lemma_dict


def test_get_modal_examples():
    # input
    name_lemma_dict = {
        'CLINTON': {'may', 'could'},
        'COOPER': {'might'},
        'RADDATZ': {'will'},
        'TRUMP': {'would', 'ought'}
    }
    name_line_dict = {
        "CLINTON": [
            nlp("CLINTON: You may want to change that."),
            nlp("CLINTON: If I could change that.")
        ],
        "COOPER": [
            nlp("COOPER: You might want to say that again."),
            nlp("COOPER: What is your problem.")
        ],
        "RADDATZ": [nlp("RADDATZ: I'll be careful.")],
        "TRUMP": [
            nlp("TRUMP: What wouldn't you want to change?"),
            nlp("TRUMP: I ought to be American."),
            nlp("TRUMP: How about tomorrow?")
        ]
    }

    # output
    name_example_dict = {
        'CLINTON': {
            'may': 'You may want to change that.',
            'could': 'If I could change that.'
        },
        'COOPER': {
            'might': 'You might want to say that again.'
        },
        'RADDATZ': {
            'will': "I'll be careful."
        },
        'TRUMP': {
            'would': "What wouldn't you want to change?",
            'ought': 'I ought to be American.'
        }
    }

    # test
    assert get_modal_examples(name_lemma_dict, name_line_dict) == name_example_dict
    assert isinstance(get_modal_examples(name_lemma_dict, name_line_dict), dict)
