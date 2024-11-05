passphrase = 'allegoryofthecave'

def midsem_survey(p):
    """
    You do not need to understand this code.
    >>> midsem_survey(passphrase)
    '3d9f1125b109b311959d068240016badb874603eab75302a445e1a50'
    """
    import hashlib
    return hashlib.sha224(p.encode('utf-8')).hexdigest()


class VendingMachine:
    """A vending machine that vends some product for some price."""

    def __init__(self, product, price):
        self.product = product
        self.price = price
        self.stock = 0
        self.balance = 0

    def restock(self, quantity):
        self.stock += quantity
        return f"Current {self.product} stock: {self.stock}"

    def add_funds(self, amount):
        if self.stock == 0:
            return f"Nothing left to vend. Please restock. Here is your ${amount}."
        self.balance += amount
        return f"Current balance: ${self.balance}"

    def vend(self):
        if self.stock == 0:
            return "Nothing left to vend. Please restock."
        if self.balance < self.price:
            return f"Please add ${self.price - self.balance} more funds."
        change = self.balance - self.price
        self.balance = 0
        self.stock -= 1
        if change == 0:
            return f"Here is your {self.product}."
        else:
            return f"Here is your {self.product} and ${change} change."


def store_digits(n):
    """Stores the digits of a positive number n in a linked list."""
    result = Link(n % 10)
    n //= 10
    while n > 0:
        result = Link(n % 10, result)
        n //= 10
    return result


def deep_map_mut(func, lnk):
    """Mutates a deep link lnk by replacing each item found with the
    result of calling func on the item."""
    current = lnk
    while current is not Link.empty:
        if isinstance(current.first, Link):
            deep_map_mut(func, current.first)
        else:
            current.first = func(current.first)
        current = current.rest


def two_list(vals, counts):
    """Returns a linked list according to the two lists that were passed in."""
    result = Link(vals[0])
    current = result
    for i in range(len(vals)):
        for j in range(counts[i] - 1):
            current.rest = Link(vals[i])
            current = current.rest
        if i < len(vals) - 1:
            current.rest = Link(vals[i + 1])
            current = current.rest
    return result



class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'

