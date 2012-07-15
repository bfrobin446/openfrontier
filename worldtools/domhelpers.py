'''
Repeatedly-used operations on DOM nodes not available as standard methods
'''

def getFirstChildElementWithTagName(parentNode, tagName):
    '''
    Return first element with the specified ``tagName`` that is a direct child
    of ``parentNode``. If no such element is present, return ``None``.
    '''
    try:
        return next(child for child in parentNode.childNodes
                if child.nodeType == child.ELEMENT_NODE
                and child.tagName == tagName)
    except StopIteration:
        return None

def getChildElementsWithTagName(parentNode, tagName):
    '''
    Return all elements with the specified ``tagName`` that are direct children
    of ``parentNode``. If no such elements are present, return empty list.
    '''
    return [child for child in parentNode.childNodes
            if child.nodeType == child.ELEMENT_NODE
            and child.tagName == tagName]

def getInnerText(node):
    '''
    Return all character data contained in or under ``node``, without internal
    tags or CDATA markup.
    '''
    if (node.nodeType == node.TEXT_NODE
            or node.nodeType == node.CDATA_SECTION_NODE):
        return node.data
    elif node.nodeType == node.ELEMENT_NODE:
        return ''.join(getInnerText(n) for n in node.childNodes)
    else:
        return ''
