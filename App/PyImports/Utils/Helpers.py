def dict2xml(d, root_node=None):
    wrap          = False if root_node is None or isinstance(d, list) else True
    root          = 'root' if root_node is None else root_node
    root_singular = root[:-1] if root[-1] == 's' else root
    xml           = ''
    attr          = ''
    children      = []

    if isinstance(d, dict):
        for key, value in dict.items(d):
            if isinstance(value, (dict, list)):
                children.append(dict2xml(value, key))
            elif key[0] == '@':
                attr = attr + ' ' + key[1::] + '="' + str(value) + '"'
            else:
                xml = '<' + key + ">" + str(value) + '</' + key + '>'
                children.append(xml)

    elif isinstance(d, list):
        for value in d:
            children.append(dict2xml(value, root_singular))

    else:
        raise TypeError(f"Type {type(d)} is not supported")

    end_tag = '>' if children else '/>'

    if wrap or isinstance(d, dict):
        xml = '<' + root + attr + end_tag

    if children:
        xml += "".join(children)

        if wrap or isinstance(d, dict):
            xml += '</' + root + '>'

    return xml
