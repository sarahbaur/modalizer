import pytest

from modalizer.main import get_names


def test_get_names():
    # input
    name_line_list = [
        "RADDATZ: We want to give the audience a chance.",
        "TRUMP: If you did that in the private sector, "
        "you'd be put in jail, let alone after getting a subpoena from the United States Congress.",
        "COOPER: Secretary Clinton, you can respond. "
        "Then we have to move on to an audience question.",
        "CLINTON: Look, it's just not true. And so please, go to...",
        "TRUMP: Oh, you didn't delete them?",
        "COOPER: Allow her to respond, please.",
        "CLINTON: It was personal e-mails, not official.",
        "TRUMP: Oh, 33,000? Yeah.",
        "CLINTON: Not - well, we turned over 35,000, so...",
        "TRUMP: Oh, yeah. What about the other 15,000?",
        "COOPER: Please allow her to respond. She didn't talk while you talked.",
        "CLINTON: Yes, that's true, I didn't.",
        "TRUMP: Because you have nothing to say."
    ]

    # output
    name_set = {"RADDATZ", "TRUMP", "COOPER", "CLINTON"}

    # test
    assert get_names(name_line_list) == name_set
    assert isinstance(get_names(name_line_list), set)
