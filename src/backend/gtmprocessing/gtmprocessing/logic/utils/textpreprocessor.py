# Copyright (C) 2021 Pablo Fernández Bravo
#
# This file is part of github-text-mining-tfg.
#
# github-text-mining-tfg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# github-text-mining-tfg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with github-text-mining-tfg.  If not, see <http://www.gnu.org/licenses/>.

""" TextPreprocessor class module.
"""

from typing import List, Tuple

from transformers.tokenization_utils import PreTrainedTokenizer  # type: ignore


class TextPreprocessor():
    """ Class in charge of the text preprocessing process.
    """

    def __init__(self, tokenizer: PreTrainedTokenizer):
        self.__tokenizer: PreTrainedTokenizer = tokenizer
        self.__max_model_length = self.__tokenizer.model_max_length or 512
        self.section_points: List[int] = [0]

    def preprocess(self, sentences: List[str]) -> List[List[str]]:
        """  Groups the sentences in sections suitable to the tokenizer limits.

        Args:
            sentences (List[str]): A list of sentences.

        Returns:
            List[List[str]]: A list that contains a list per section.
                Each inner list contains the sentences of that section.
        """
        sentences_tokens: List[int] = [
            len(self.__tokenizer.encode(sentence)) for sentence in sentences]

        prev_section_points, _ = self.__sentences_compactator(sentences_tokens)

        self.section_points = self.__balance_sections(
            sentences_tokens, prev_section_points)

        return [sentences[self.section_points[i]:self.section_points[i+1]]
                for i in range(len(self.section_points) - 2)]

    def __sentences_compactator(self, sentences_tokens: List[int]) -> Tuple[List[int], List[int]]:
        # pylint: disable=line-too-long
        """ Given a list with the number of tokens per sentence the function groups
        the sentences in sections that don't surpass the model limit.
        Original concept:  https://github.com/dmlls/jizt-tfg/blob/b566f22a1714408893ca7a590da8e9d1ff18068f/src/services/t5_large_text_encoder/text_encoding.py#L153

        Args:
            sentences_tokens (List[str]): A list with the number of tokens per sentence.

        Returns:
            Tuple[List[int], List[int]]: A tuple is composed by two lists.
                The first list contains the starting points of each section in the sentences list.
                The second list contains the number of tokens of each section.
        """
        section_points: List[int] = [0]
        sections_tokens: List[int] = [0]

        # We loop over the tokens per sentence grouping the sentences
        # in sections that don't surpass the model limit.
        for i in range(len(sentences_tokens)):
            n_sentence_tokens = sentences_tokens.pop(0)
            if sections_tokens[-1] + n_sentence_tokens < self.__max_model_length:
                sections_tokens[-1] += n_sentence_tokens
            else:
                sections_tokens.append(n_sentence_tokens)
                section_points.append(i)

        return (section_points, sections_tokens)

    def __balance_sections(self, sentences_tokens: List[int],
                           prev_section_points: List[int]) -> List[int]:
        # pylint: disable=line-too-long
        """ Given a list with the number of tokens per sentence and a list
        with the previous starting points of the sections, the function tries
        to balance the number of tokens that compose each section.
        Original concept: https://github.com/dmlls/jizt-tfg/blob/b566f22a1714408893ca7a590da8e9d1ff18068f/src/services/t5_large_text_encoder/text_encoding.py#L196

        Args:
            sentences_tokens (List[str]): A list with the number of tokens per sentence.
            prev_section_points (List[int]): A list with the starting points of each section
                in the sentences list.

        Returns:
            List[int]: A list with the optimized starting points of each section
                in the sentences list.
        """
        new_sect_points = prev_section_points[:]
        new_sect_points.append(len(sentences_tokens))

        while True:
            temp_sect_points = new_sect_points[:]

            # From the n - 1 section to 0.
            for i in range(len(new_sect_points) - 2, 0, -1):
                # The number of tokens of the previous section.
                sect_1_size = sum(
                    sentences_tokens[temp_sect_points[i-1]:temp_sect_points[i]])

                # The number of tokens of the current section.
                sect_2_size = sum(
                    sentences_tokens[temp_sect_points[i]:temp_sect_points[i+1]])

                # The number of tokens of the previous section if we move
                # the last sentence of the previous section to the current section.
                new_sect_1_size = sum(
                    sentences_tokens[temp_sect_points[i-1]:(temp_sect_points[i] - 1)])

                # The number of tokens of the current section if we move
                # the last sentence of the previous section to the current section.
                new_sect_2_size = sum(
                    sentences_tokens[(temp_sect_points[i] - 1):temp_sect_points[i+1]])

                # We calculate the maximum value of the differences between the previous
                # the current sections with the model limit. If this value is bigger than
                # the value we would get if we move the last sentence of the previous
                # section to the correct one, then we move the point who marks the start
                # of the actual section.
                if (max(self.__max_model_length - sect_1_size,
                        self.__max_model_length - sect_2_size) >
                        max(self.__max_model_length - new_sect_1_size,
                            self.__max_model_length - new_sect_2_size)):
                    temp_sect_points[i] -= 1

            # If the sections points haven't changed since the last iteration, we end the loop.
            if new_sect_points != temp_sect_points:
                new_sect_points = temp_sect_points
            else:
                break

        return new_sect_points[:-1]
