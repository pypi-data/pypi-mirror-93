import re, string
class DataWrangler():

    def remove_pii(self, text: str, pii: list):
        """
        A list called pii_info is compiled as a regular expression pattern that is used to remove sensitive information. A cleaned string called no_pii is returned with the removed PII.
        """
        pii_info = pii
        pattern = re.compile("|".join(pii_info), re.IGNORECASE)
        no_pii = re.sub(pattern, '', text)
        return no_pii

    def insert_space(self, text: str, index: int):
        """
        Takes a string and index argument to add spacing in a string at a given index.
        """
        return text[0:index] + ' ' + text[index:]

    def check_spacing(self, text: str, word_start_index: int, word_end_index: int):
        """
        Checks for spacing in front and end of string by gettting the index of the found word and subtracting 1 for the front space and adding the length of the word to the index for the
        rear spacing. The insert_space method is used if a space should exist where there is none -- front or back.
        """
        # checks for front space
        if desc[word_start_index-1].isspace() is False:
            new_text = self.insert_space(text, word_start_index)
            # checks for rear space in addition to front string rear_space variable is incremented by one in nested if statement to accomodate the new space inserted up front
            if new_text[word_end_index + 1].isspace() is False:
                    return self.insert_space(new_text, word_end_index + 1)
            else:
                return new_text
        if len(text) >= word_end_index + 1 and text[word_end_index + 1].isspace() is False:
                return self.insert_space(text, word_end_index)
        else:
            return text  

    def remove_character_set(self, text: str, ok_pattern: list = list(string.ascii_letters + ' ')):
        """
        Pass string and list of characters as ok_pattern to be cleared when removing character set. Everything not in that character set will be removed from the string before being returned. To preserve
        string structure, a space is added inspace of the character removed. The ok_pattern argument is a list of characters that will stay in the text. The string.ascii_letters and space (' ') are the default 
        list of characters that are allowed.
        """
        new_string = ''
        for c in text:
            if c in ok_pattern:
                new_string += c
            if c not in ok_pattern:
                new_string += ' '
        #new_string = ''.join(c for c in text if c in whitelist)
        return new_string

    def remove_spacing(self, text: str):
        """
        Eliminates unnecessary spacing in string of words in description. Ensures that a only one space between words exist.
        """
        space_array = text.split(' ')
        removed_spacing_array = [word for word in space_array if len(word) > 0]
        removed_spacing_string = ''
        for i in removed_spacing_array:
            removed_spacing_string += i + ' '
        return removed_spacing_string.upper()

    def remove_www(self, text: str, internet_pattern: list = ['WWW', 'WWW.', '.COM', '.ORG']):
        """
        Removes anything internet related in string such as www or .com; takes a patter_list as argument for string pattern comparison and removal.
        """
        pattern = re.compile('|'.join(internet_pattern), re.IGNORECASE)
        new_text = re.sub(pattern, '', text)
        return new_text

    def split_file(self, filehandler, delimiter=',', row_limit=10000, output_name_template='output_%s.csv', output_path='.', keep_headers=True):
        """
        Splits file into the number of rows determined by the method argument (default is 10,000 rows). Default delimiter is comma but can be changed by passing a method argument.
        Output_name_template is the file naming convention passed with an incrementer number included in the file name. The default output is csv file. The default path argument
        is set to the current directory. The keep_headers argument outputs file headers into each new file split and the default value is True.
        """
        import csv
        reader = csv.reader(filehandler, delimiter=delimiter)
        current_piece = 1
        current_out_path = os.path.join(
             output_path,
             output_name_template  % current_piece
        )
        current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
        current_limit = row_limit
        if keep_headers:
            headers = next(reader)
            current_out_writer.writerow(headers)
        for i, row in enumerate(reader):
            if i + 1 > current_limit:
                current_piece += 1
                current_limit = row_limit * current_piece
                current_out_path = os.path.join(
                   output_path,
                   output_name_template  % current_piece
                )
                current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
                if keep_headers:
                    current_out_writer.writerow(headers)
            current_out_writer.writerow(row)