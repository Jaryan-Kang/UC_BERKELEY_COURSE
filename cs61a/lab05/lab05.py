def insert_items(s, before, after):
    """Insert after into s after each occurrence of before and then return s."""
    index = 0
    while index < len(s):
        if s[index] == before:
            s.insert(index + 1, after)
            index += 1
        index += 1
    return s


def group_by(s, fn):
    """Return a dictionary of lists that together contain the elements of s."""
    grouped = {}
    for item in s:
        key = fn(item)
        if key in grouped:
            grouped[key].append(item)
        else:
            grouped[key] = [item]
    return grouped


def count_occurrences(t, n, x):
    """Return the number of times that x is equal to one of the first n elements of iterator t."""
    count = 0
    for _ in range(n):
        if next(t) == x:
            count += 1
    return count


def repeated(t, k):
    """Return the first value in iterator t that appears k times in a row."""
    count = 0
    prev_value = next(t)
    while True:
        current_value = next(t)
        if current_value == prev_value:
            count += 1
            if count == k - 1:
                return current_value
        else:
            count = 0
        prev_value = current_value


def sprout_leaves(t, leaves):
    """Sprout new leaves containing the labels in leaves at each leaf of the original tree t."""
    if is_leaf(t):
        return tree(label(t), [tree(leaf) for leaf in leaves])
    else:
        return tree(label(t), [sprout_leaves(branch, leaves) for branch in branches(t)])


def partial_reverse(s, start):
    """Reverse part of a list in-place, starting with start up to the end of the list."""
    end = len(s) - 1
    while start < end:
        s[start], s[end] = s[end], s[start]
        start += 1
        end -= 1


# Tree Data Abstraction

def tree(label, branches=[]):
    """Construct a tree with the given label value and a list of branches."""
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

# Remaining functions omitted for brevity
