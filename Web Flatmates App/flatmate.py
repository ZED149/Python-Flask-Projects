

# this file contains flatmate class

class Flatmate:
    """
    This class creates a flatmate object that contains its name and days_in_house
    """
    # constructor
    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house

    # pays()
    def pays(self, bill, flatmate2):
        """
        This function returns the amount to be paid by the caller flatmate.
        :param bill:
        :param flatmate2:
        :return:
        """
        total_days = self.days_in_house + flatmate2.days_in_house
        percentage = self.days_in_house / total_days
        return round(percentage * bill.amount)
