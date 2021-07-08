from bs4 import BeautifulSoup


def xpath_soup(element):
    # # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
    # """
    # Generate xpath from BeautifulSoup4 element.
    # :param element: BeautifulSoup4 element.
    # :type element: bs4.element.Tag or bs4.element.NavigableString
    # :return: xpath as string
    # :rtype: str
    # Usage
    # -----
    # >>> import bs4
    # >>> html = (
    # ...     '<html><head><title>title</title></head>'
    # ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
    # ...     )
    # >>> soup = bs4.BeautifulSoup(html, 'html.parser')
    # >>> xpath_soup(soup.html.body.p.i)
    # '/html/body/p[1]/i'
    # >>> import bs4
    # >>> xml = '<doc><elm/><elm/></doc>'
    # >>> soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    # >>> xpath_soup(soup.doc.elm.next_sibling)
    # '/doc/elm[2]'
    # """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: BeautifulSoup.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
            )
        )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


from bs4.element import Comment


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True, recursive=True)
    visible_texts = filter(tag_visible, texts)
    return [xpath_soup(e) for e in visible_texts]
