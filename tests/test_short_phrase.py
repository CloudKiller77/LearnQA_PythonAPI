class TestShortPhrase:

    def test_short_phrase(self):
        phrase = input("Please, set a phrase less then 15 chars: ")

        assert len(phrase) < 15, "Your phrase is more then 15 chars"
