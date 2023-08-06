from .tag import TagDispatcher

class HeadingDispatcher(TagDispatcher):
    def __init__(self):
        super(HeadingDispatcher, self).__init__()

    @classmethod
    def append_head(cls, element, container):
        paragraph = cls.get_new_paragraph(container)
        return cls._append_heading(element.text, element.tag, paragraph)

    @classmethod
    def append_tail(cls, element, container):
        paragraph = cls.get_current_paragraph(container)
        return cls._append_heading(element.tail, element.tag, paragraph)

    @classmethod
    def _append_heading(cls, text, tag, container):
        """
        <hx> Creates a heading paragraph inside the document container
        """
        level = int(tag[1:])
        style = 'Title' if level == 0 else 'Heading%d' % level

        container.text = text
        container.style = style
        return container
