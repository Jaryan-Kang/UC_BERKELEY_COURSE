class Transaction:
    def __init__(self, id, before, after):
        self.id = id
        self.before = before
        self.after = after

    def changed(self):
        """Return whether the transaction resulted in a changed balance."""
        return self.before != self.after

    def report(self):
        """Return a string describing the transaction."""
        msg = 'no change'
        if self.changed():
            if self.before > self.after:
                msg = f'decreased {self.before}->{self.after}'
            else:
                msg = f'increased {self.before}->{self.after}'
        return f"{self.id}: {msg}"

class Account:
    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder
        self.transactions = []

    def deposit(self, amount):
        """Increase the account balance by amount, add the deposit
        to the transaction history, and return the new balance.
        """
        before = self.balance
        self.balance += amount
        self.transactions.append(Transaction(len(self.transactions), before, self.balance))
        return self.balance

    def withdraw(self, amount):
        """Decrease the account balance by amount, add the withdraw
        to the transaction history, and return the new balance.
        """
        if amount > self.balance:
            return 'Insufficient funds'
        before = self.balance
        self.balance -= amount
        self.transactions.append(Transaction(len(self.transactions), before, self.balance))
        return self.balance





class Email:
    """An email has the following instance attributes:

        msg (str): the contents of the message
        sender (Client): the client that sent the email
        recipient_name (str): the name of the recipient (another client)
    """
    def __init__(self, msg, sender, recipient_name):
        self.msg = msg
        self.sender = sender
        self.recipient_name = recipient_name

class Server:
    def __init__(self):
        self.clients = {}

    def send(self, email):
        """Append the email to the inbox of the client it is addressed to."""
        recipient = self.clients.get(email.recipient_name)
        if recipient:
            recipient.inbox.append(email)

    def register_client(self, client):
        """Add a client to the dictionary of clients."""
        self.clients[client.name] = client

class Client:
    def __init__(self, server, name):
        self.inbox = []
        self.server = server
        self.name = name
        server.register_client(self)

    def compose(self, message, recipient_name):
        """Send an email with the given message to the recipient."""
        email = Email(message, self, recipient_name)
        self.server.send(email)



def make_change(amount, coins):
    if amount == 0:
        return []
    if not coins or min(coins) > amount:
        return None
    smallest = min(coins)
    rest = remove_one(coins, smallest)
    without_coin = make_change(amount, rest)
    with_coin = make_change(amount - smallest, coins)
    if with_coin is None:
        return without_coin
    return [smallest] + with_coin

def remove_one(coins, coin):
    copy = dict(coins)
    copy[coin] -= 1
    if copy[coin] == 0:
        del copy[coin]
    return copy


class ChangeMachine:
    def __init__(self, pennies):
        self.coins = {1: pennies}

    def change(self, coin):
        """Return change for coin, removing the result from self.coins."""
        result = make_change(coin, self.coins)
        if result is not None:
            for c in result:
                self.coins[c] -= 1
                if self.coins[c] == 0:
                    del self.coins[c]
        return result
