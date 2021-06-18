from typing import Union, List

class Category:
    def __init__(self, name:str):
        # String name of category
        self.name = name
        # Ledger of deposits, withdrawals and transfers
        self.ledger = []

    def deposit(self, amt:Union[int,float], description:str=""):
        """Deposits funds in ledger.

        Args:
            amt (Union[int,float]): Amount to deposit
            description (str, optional): Description of deposit. Defaults to "".
        """
        # Append new deposit to ledger
        d = {"amount":amt, "description":description}
        self.ledger.append(d)

    def get_balance(self) -> Union[int,float]:
        """Find current balance of the ledger.

        Returns:
            Union[int,float]: The current balance of the ledger.
        """
        # sum all elements in ledger
        return sum([i['amount'] for i in self.ledger])

    def withdraw(self, amt:Union[int,float], description:str="") -> bool:
        # Identify if the amount to withdraw is less than or equal to total balance
        sufficient_funds = self.check_funds(amt)
        # If there are sufficient funds, attach to ledger as a debit
        if sufficient_funds:
            d = {"amount":-amt, "description":description}
            self.ledger.append(d)
            return True
        return False

    def transfer(self, amt:Union[int,float], category:Category) -> bool:
        """Transfer funds between two categories' ledgers.

        Args:
            amt (Union[int,float]): Amount to transfer.
            category (Category): The category to which the funds should be transferred.

        Returns:
            bool: True if the transfer was successful.
        """
        # If the balance is more than the transfer amount,
        # Withdraw from current ledger and deposit in another.
        if self.get_balance()>amt:
            self.withdraw(amt, f"Transfer to {category.name}")
            category.deposit(amt, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amt:Union[int,float]) -> bool:
        """Checks if the current balance of the ledger is larger than the requested amount.

        Args:
            amt (Union[int,float]): Amount to check against ledger balance.

        Returns:
            bool: True if current balance is larger than requested amount.
        """
        # Check if funds are sufficient for withdrawal/transfer
        current_balance = self.get_balance()
        if current_balance>=amt:
            return True
        return False

    def __str__(self) -> str:
        """Prints a user-friendly view of the ledger.

        Returns:
            str: The complete ledger, plus the current balance.
        """
        name_chars = len(self.name)
        asterisks = "*"*int((30-name_chars)/2)
        headline = asterisks+self.name+asterisks
        for i in self.ledger:
            if len(i['description'])>23:
                description = i['description'][:23]
            else:
                description = i['description']
            amount = "{:.2f}".format(i['amount'])
            if len(amount)>7:
                amount = amount[:7]
            amount_spaces = (30-len(description))-(len(amount))
            headline += f"\n{description}" + " "*amount_spaces + f"{amount}"
        total = "{:.2f}".format(self.get_balance())
        headline += f"\nTotal: {total}"
        return headline


def create_spend_chart(categories:List[Category]) -> str:
    """Creates a visual overview of spending distribution of categories.

    Args:
        categories (List[Category]): A list of instances of the Category class.

    Returns:
        str: A printable overview of the spending distribution.
    """
    # Create a dict object for only withdrawals
    withdrawals = dict()
    # Loop through categories and create new dict keys based on category names
    # Then create their values as the sum of the withdrawals and
    # round down to nearest 10.
    for i in categories:
        withdrawals[f"{i.name}"] = sum([abs(l['amount']) for l in i.ledger if l['amount']<0])
    percentage = {k:(v/(sum(withdrawals.values()))*100) for k,v in zip(withdrawals.keys(), withdrawals.values())}
    percentage = {k:v-(v%10) for k,v in percentage.items()}

    # Create result string title
    result = "Percentage spent by category\n"
    # Creates y-axis with numbers ranging from 100 to 0 in increments of 10.
    for i in range(100,-10,-10):
        result += " "*(3 - len(str(i))) + f"{i}|" + " "*((len(categories)*3)+1) +"\n"
    # Create x-axis whose length will depend on number of categories provided.
    result += "    "+"-"+"-"*(len(categories)*3)+"\n"

    # This block will reorder the category names so that they will
    # be written vertically below the x-axis.
    # First, identify the category names and the maximum length of those.
    # The maximum length is needed in order to add the right amount of spaces after 
    # the shorter category names.
    cat_names = [i for i in [cat.name for cat in categories]]
    max_name_length = max([len(i) for i in cat_names])
    # Create an empty list for the reordered letters
    reordered_letters = []
    # Loop through the category name indices and add them to the reordered letters
    # list sequentially (i.e. Category 1's first letter, Category 2's first letter, Category 1's second letter, Category 2's second letter, etc.).
    # If a category name is shorter than the index requested, append a space instead.
    for i in range(max_name_length):
        for c in cat_names:
            try:
                reordered_letters.append(c[i])
            except:
                reordered_letters.append(" ")
    result += "    "
    # The block below will set a counter for how many letters have been entered on a single line.
    # If it is the first letter of the line, it will be preceded by 4 spaces and then entered as {space}-letter-{space}
    # Other wise, the first four spaces will be supressed.
    entered_letters = 1
    for i in reordered_letters:
        if entered_letters<len(cat_names):
            if i==1:
                result += "    "
            result+=" "+i+" "
            entered_letters+=1
        else:
            result+=" "+i+"  "+"\n    "
            entered_letters=1
    # Create a dictionary to identify in which column index that categories
    # markers will be placed.
    index_dict = dict()
    # In this block: In each category name, loop through the letters in the name and the length of the name.
    # Starting at line 13 (where the x-axis labels begin), find in each line the indexes that match the category letters.
    # If all of the category letter indices are equal, assign that index to the dictionary matched with the category name.
    for cat in categories:
        for i,n in zip(cat.name, range(len(cat.name))):
            loc_list = []
            loc_list.append(result.split("\n")[13+n].index(cat.name[n]))
            if len([i for i in loc_list if i==loc_list[0]]) == len(loc_list):
                index = loc_list[0]
        index_dict[cat.name] = index

    # Split the result string by line
    result_split = result.split("\n")
    # Create a dictionary of the axis numbers and their indices
    axis_dict = {ix:num for ix,num in zip(range(1,12), range(100,-10,-10))}
    # For each category: loop through the axis indices.
    # If the axis_dict value for that index is less than or equal to the percentage value for that category
    # Replace the string so that the marker "o" is placed in the column index location.
    for cat in categories:
        for x in axis_dict:
            if axis_dict[x]<=percentage[cat.name]:
                result_split[x] = result_split[x][:index_dict[cat.name]] + "o" + result_split[x][index_dict[cat.name]+1:]

    # Recombine all of the new lines and return the final result
    return "\n".join(result_split[:-1])
