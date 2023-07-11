import os
import re
from typing import Callable


def get_index(func):
    """
    Get the index of the text.
    """

    def decorator(self, text: str, *args, **kwargs):
        if 'index' in kwargs.keys():  # do not overwrite file_contents if provided
            raise KeyError('do not use the index argument; it is provided automatically')
        if not isinstance(text, str):
            raise TypeError(f'Text must be str, got {type(text)}: {text} instead')
        kwargs['index'] = self._io.find(text)
        return func(self, text, *args, **kwargs)
    return decorator


class ConfigEditor:
    def __init__(self, cfg_file: str, comment_delimiter: str = '#'):
        self._cfg_file = cfg_file
        self._comment_delimiter = comment_delimiter.strip()

    def __enter__(self):
        if not os.path.isfile(self._cfg_file):
            print(self._cfg_file, 'does not exist, creating...')
            try:
                directory = os.path.dirname(self._cfg_file)
                os.mkdir(directory)
                print(directory, 'successfully created')
            except FileExistsError:
                pass
            open(self._cfg_file, 'w').close()
            print(self._cfg_file, 'successfully created')

        with open(self._cfg_file, 'r', encoding='utf-8') as f:
            self._io = f.read()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        with open(self._cfg_file, 'r+', encoding='utf-8') as f:
            if self._io != f.read():
                f.seek(0) # reset after call to read()
                f.write(self._io)
                f.truncate() # get rid of old text beyond the end of the new text
                print('Successfully edited', self._cfg_file)

    @get_index
    def add(self,
            text: str,
            under: str = '',
            start: bool = False,
            replace_matching: str = '=',
            allow_duplicates: bool = False,
            enclose: str = '',
            index: int = -1):
        """
        Add a line.
        The line will be added under a heading if under is set.
        If the heading does not exist it will be created.
        Use \\n for multiple lines.
        Prints and ends if the desired content already exists in the file.
        If the desired content already exists in the file but is commented out it will be uncommented.

        Args:
            text: the line(s) to add
            under: the line to add the content under as a regex
            start: add the line to the start of the file if `under` is not found
            replace_matching: check if a similar statement to the content exists before the provided string
            allow_duplicates: if `text` is detected but is not under `under`, create a new line under `under`
            enclose: append this string on a new line under `text` *only* if `under` does not exist
        """
        if self._is_comment(index):
            self.uncomment(text)
            return
        elif index != -1:
            if not (allow_duplicates and not (text in self._io[self._io.find(under):])):
                # line already exists
                return

        if replace_matching and not allow_duplicates:
            matching_content = text[:text.find(replace_matching)+1]
            if matching_content and matching_content in self._io:
                self.remove(matching_content)

        if start:
            insert_point = 0
        else:
            insert_point = len(self._io)

        if under:
            if (match := self._io.find(under)) != -1:
                insert_point = match + len(under) + 1
            else:
                print('Could not find heading', under)
                heading = under + '\n'
                self._insert(heading, insert_point)
                insert_point += len(heading)
                print('Made new heading:', under)

                if enclose:
                    self._insert(enclose+'\n', insert_point)

        self._insert(text+'\n', insert_point)
        print(f'Added line " {text} "')

    def add_lines(self, *lines, under: str = '', **options):
        """
        Applies add sequentially to strings passed with the previous string passed as the `under` argument.
        """
        for line in lines:
            self.add(line, under=under, **options)
            under = line

    @get_index
    def exists(self, text: str, include_comments: bool = False, index: int = -1) -> bool:
        """
        Tests if `text` exists in the file.
        """
        return index != -1 and ((not self._is_comment(index)) or include_comments)

    @get_index
    def replace(self, text: str, with_this: str, index: int):
        """
        Replace a line.
        Use \\n for multiple lines.
        Prints and ends if the line(s) to replace cannot be found.

        Args:
            text: the line(s) to replace
            with_this: the line to add the content under as a regex
        """
        if not text:
            print('Nothing to replace')
            return
        if index == -1:
            print('Could not find the line(s) " {text} " to replace')
            return
        self.remove(text)
        self._insert(with_this+'\n', index)
        print(f'Replaced line(s) " {text} " with " {with_this} "')

    @get_index
    def remove(self, text: str, index: int):
        """
        Remove the line(s) that contain(s) `text`
        """
        if not text:
            return
        if index == -1:
            return
        if (content_end := self._io.find('\n', index) + 1) == 0:
            content_end = len(self._io)

        print(f'Removed " {self._io[index:content_end]} "')
        self._cut(index, content_end)

    def for_each(self, regex: re.Pattern, function: Callable[[str], None]):
        """
        Run a function on all lines matching the regex.

        Supported functions:
            ConfigEditor.remove
            ConfigEditor.comment
            ConfigEditor.uncomment
        """
        print('searching for', regex)
        for m in regex.finditer(self._io):
            function(m.group(0))
            print('successfully did operation on', m.group(0))

    @get_index
    def comment(self, text: str, index: int):
        """
        Comment out the line `text` if it is not already a comment.
        """
        if not self._is_comment(index):
            self._insert(self._comment_delimiter + ' ', index)
            print(f'Commented " {text} "')

    @get_index
    def uncomment(self, text: str, index: int):
        """
        Uncomment the line `text` if it is a comment.
        """
        if self._is_comment(index):
            self._cut(self._comment_start(index), index)
            print(f'Uncommented " {text} "')

    def _insert(self, text: str, index: int):
        self._write(self._io[:index] + text + self._io[index:])

    def _cut(self, start, end):
        self._write(self._io[:start] + self._io[end:])

    def _write(self, text: str):
        self._io = text

    def _is_comment(self, index: int) -> bool:
        start = self._comment_start(index)
        substr = self._io[start:index]
        return substr.strip() == self._comment_delimiter

    def _comment_start(self, index: int) -> int:
        line_start = self._io.rfind('\n', 0, index)
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1
        return line_start
