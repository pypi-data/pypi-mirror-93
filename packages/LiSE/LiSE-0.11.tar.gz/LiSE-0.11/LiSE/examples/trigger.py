

def uncovered(thing):
    for shrub_candidate in thing.location.contents():
        if (shrub_candidate.name[:5] == 'shrub'):
            return False
    thing.engine.info('kobold uncovered')
    return True

def breakcover(thing):
    if (thing.engine.random() < thing['sprint_chance']):
        thing.engine.info('kobold breaking cover')
        return True

def sametile(thing):
    try:
        return (thing['location'] == thing.character.thing['kobold']['location'])
    except KeyError:
        return False

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

def standing_still(thing):
    return (thing.next_location is None)

def absent(node):
    return (node.location != node.character.place['classroom'])

def in_classroom_after_class(node):
    phys = node.character
    return ((node.location == phys.place['classroom']) and (phys.stat['hour'] >= 15))

def party_time(character):
    phys = character.engine.character['physical']
    return (23 >= phys.stat['hour'] > 15)

def out_of_class(character):
    avatar = character.avatar['physical'].only
    classroom = avatar.character.place['classroom']
    return (avatar.location != classroom)

def in_class(node):
    classroom = node.engine.character['physical'].place['classroom']
    if hasattr(node, 'location'):
        assert (node == node.character.avatar['physical'].only)
        return (node.location == classroom)
    else:
        return (node.character.avatar['physical'].only.location == classroom)

def somewhat_drunk(node):
    return (node['drunk'] > 0)

def somewhat_late(node):
    return (node['slow'] > 0)
