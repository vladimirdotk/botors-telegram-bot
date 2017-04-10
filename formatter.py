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
        formatted_notes = '*Notes*:\n\n'

        for note in notes:
            formatted_notes += 'Id: {}\n`{}`\n\n'.format(
                note.get('_id'), note.get('header')
            )

        return formatted_notes

    @staticmethod
    def format_created_note(note):
        """
        Formates created note
        :param dict note: 
        :return: 
        """
        return '*Note created*:\nId: {}'.format(note.get('_id'))
