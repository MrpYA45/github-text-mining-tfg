from typing import List, Text

from blingfire import text_to_sentences  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from markdown import markdown  # type: ignore


class DataUtils():

    @staticmethod
    def markdown_to_raw_text(markdown_str: str) -> str:
        """ Gets a string with markdown format,
                and returns the string without the text decorations.

        Args:
            markdown_str (str): The string with markdown format.

        Returns:
            str: The string without markdown format.
        """
        # Using markdown module (and extensions) we transform markdown to html.
        html_str: Text = markdown(markdown_str, extensions=[
            "markdown_checklist.extension", "mdx_gh_links", "fenced_code"])

        # BeautifulSoup let's us extract raw text from the html tags.
        soup = BeautifulSoup(html_str, "html.parser")

        # Removing code tags and it's content for a cleaner text.
        for tags in soup(["pre", "code"]):
            tags.decompose()

        # Getting the actual text from the html tags.
        raw_str = soup.get_text()

        # Strip newlines, tabulations and trailing whitespaces.
        raw_str = " ".join(raw_str.split())

        return raw_str

    @staticmethod
    def split_text_into_sentences(text_str: str) -> List[str]:
        """ Given a text string, it splits each sentence into his own string.

        Args:
            text_str (str): The initial text string.

        Returns:
            List[str]: A list with the sentences.
        """

        # Strip newlines, tabulations and trailing whitespaces.
        text_str = " ".join(text_str.split())

        # Adding dot at the end if necessary.
        if text_str[-1] not in ["?", "!", "."]:
            text_str += "."

        # Using blingfire module to split the text in lines.
        sentences: List[str] = text_to_sentences(text_str).splitlines()

        # If the previous sentence doesn't end with a closing exclamation,
        # an interrogation mark or a dot, then join the actual sentence
        # with the previous one.
        fixed_sentences: List[str] = [sentences[0]]

        for sentence in sentences[1:]:
            if fixed_sentences[-1][-1] not in ["?", "!", "."]:
                fixed_sentences[-1] += fixed_sentences[-1] + " " + sentence
            else:
                fixed_sentences.append(sentence)

        return fixed_sentences

    @staticmethod
    def remove_non_ascii_chars(dirty_string: str) -> str:
        """ Given a string, clears all the non ASCII characters.

        Args:
            dirty_string (str): A string with non ASCII characters.

        Returns:
            str: A string with only ASCII characters.
        """
        clean_str: str = dirty_string.encode('ascii', 'ignore').decode('ascii')
        return " ".join(clean_str.split())
