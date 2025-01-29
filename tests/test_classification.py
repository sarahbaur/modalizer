import pytest

from modalizer.classifications import classify_count_lines, classify_modality


def test_classify_count_lines():
    # input
    line_list = [
        "CLINTON: Mr. Trump, you may want to change that.",
        "CLINTON: If I could change that.",
        "COOPER: You might want to say that again.",
        "COOPER: What is your problem.",
        "RADDATZ: I'll be careful.",
        "TRUMP: What would you want to change?.",
        "TRUMP: I ought to.",
        "TRUMP: How about tomorrow?"
    ]
    name_set = {"CLINTON", "COOPER", "RADDATZ", "TRUMP"}

    # output
    name_line_dict = {
        "CLINTON": [
            "CLINTON: Mr. Trump, you may want to change that.",
            "CLINTON: If I could change that."
        ],
        "COOPER": [
            "COOPER: You might want to say that again.",
            "COOPER: What is your problem."
        ],
        "RADDATZ": ["RADDATZ: I'll be careful."],
        "TRUMP": [
            "TRUMP: What would you want to change?.",
            "TRUMP: I ought to.",
            "TRUMP: How about tomorrow?"
        ]
    }
    name_word_count_dict = {"CLINTON": 13, "COOPER": 11, "RADDATZ": 4, "TRUMP": 12}

    # tests
    result = classify_count_lines(line_list, name_set)
    assert result == (name_line_dict, name_word_count_dict)
    assert isinstance(result[0], dict)
    assert isinstance(result[1], dict)
    for word_count in result[1].values():
        assert isinstance(word_count, int)


def test_classify_modality():
    # input
    example_sentences = [
        "She can play the guitar very well.",
        "He will finish the project by tomorrow.",
        "You must arrive on time for the meeting.",
        "You should consider taking a vacation.",
        "Could I take a break now?",
        "I want to visit Japan next year.",
        "You ought to see a doctor.",
        "Could I borrow your book?",
        "I will go to the store later."
    ]

    # output
    classification_dict = {
        'Ability': 3,
        'Prediction': 3,
        'Obligation': 1,
        'Advice': 1,
        'Permission': 0,
        'Volition': 0,
        'Unclassified': 0
    }

    # tests
    assert classify_modality(example_sentences) == classification_dict
    assert isinstance(classify_modality(example_sentences), dict)
