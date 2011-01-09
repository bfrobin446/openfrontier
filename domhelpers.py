
def getFirstChildElementWithTagName(parentNode, tagName):
    try:
        return next(child for child in parentNode.childNodes
                if child.nodeType == child.ELEMENT_NODE
                and child.tagName == tagName)
    except StopIteration:
        return None

def getChildElementsWithTagName(parentNode, tagName):
    return [child for child in parentNode.childNodes
            if child.nodeType == child.ELEMENT_NODE
            and child.tagName == tagName]

def getInnerText(node):
    if node.nodeType == node.TEXT_NODE or node.nodeType == node.CDATA_SECTION_NODE:
        return node.data
    elif node.nodeType == node.ELEMENT_NODE:
        return ''.join(getInnerText(n) for n in node.childNodes)
    else:
        return ''
