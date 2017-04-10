class Formatter:
    """
    Formatter
    """

    @staticmethod
    def format_notes(notes):
        """
        Formates notes
        :param list notes: 
        :return: 
        """
        formated_notes = '*Notes*:\n\n'

        for note in notes:
            formated_notes += 'Id: {}\n`{}`\n\n'.format(
                note.get('_id'), note.get('header')
            )

        return formated_notes
