

def not_traveling(thing):
    if (thing.next_location is not None):
        thing.engine.info('kobold already travelling to {}'.format(thing.next_location))
        return False
    else:
        return True

def kobold_alive(thing):
    return ('kobold' in thing.character.thing)

def aware(thing):
    from math import hypot
    try:
        bold = thing.character.thing['kobold']
    except KeyError:
        return False
    (dx, dy) = bold['location']
    (ox, oy) = thing['location']
    xdist = abs((dx - ox))
    ydist = abs((dy - oy))
    dist = hypot(xdist, ydist)
    return (dist <= thing['sight_radius'])

def unmerciful(thing):
    return thing.get('kill', False)

def kobold_not_here(thing):
    return ('kobold' not in thing.location.content)

def class_in_session(node):
    return (8 <= node.engine.character['physical'].stat['hour'] < 15)

def be_timely(node):
    for user in node.users.values():
        if (user.name not in ('physical', 'student_body')):
            return ((not user.stat['lazy']) or node.engine.coinflip())

def is_drunkard(character):
    return character.stat['drunkard']

def pay_attention(node):
    return (node['drunk'] == node['slow'] == 0)

def in_class(node):
    classroom = node.engine.character['physical'].place['classroom']
    if hasattr(node, 'location'):
        assert (node == node.character.avatar['physical'].only)
        return (node.location == classroom)
    else:
        return (node.character.avatar['physical'].only.location == classroom)
