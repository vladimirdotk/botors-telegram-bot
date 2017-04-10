class Formatter:
    """
    Formatter
    """

    def format_notes(self, notes):
        """
        Formates notes
        :param list notes: 
        :return: 
        """
        formatted_notes = '*Notes*:\n\n'

        for note in notes:
            formatted_notes += 'Id: {}\n*{}*\n\n'.format(
                note.get('_id'), note.get('header')
            )

        return formatted_notes

    def format_created_note(self, note):
        """
        Formates created note
        :param dict note: 
        :return: 
        """
        return '*Note created*:\n\nId: {}'.format(note.get('_id'))

    def format_edited_note(self, note):
        """
        Formates edited note
        :param dict note: 
        :return: 
        """
        return '*Note edited*:\n\nId: {}\n*{}*\n`{}`'.format(
            note.get('_id'), note.get('header'), note.get('body')
        )
