from prompt_toolkit import prompt
import sys
from help.help import clear
from entities.purse import Purse

class ConsoleInterface:
    def __init__(self):
        self.storage = Purse.get_storage()

    def console_init(self):
        input_is_correct = True
        while True:
            if input_is_correct:
                print("Main menu:\n1.Create purse\n2.Get all purses\n3.Update purse\n4.Delete purse\n5.Exit")
            else:
                print("Your input was not correct, try again")
            answer = prompt('Enter your variant: ')
            input_is_correct = self.__main_menu_redirect(answer)

    def __main_menu_redirect(self, value: int) -> bool:
        if value == '1':
            clear()
            self.__create_purse()
        elif value == '2':
            clear()
            self.__get_purses()
        elif value == '3':
            clear()
            self.__update_purse()
        elif value == '4':
            clear()
            self.__delete_purse()
        elif value == '5':
            clear()
            self.storage.store_cache()
            self.__exit()
        else:
            return False
        return True

    def __update_purse(self):
        clear()
        purses = self.storage.get_all()
        if len(purses) == 0:
            print("No purses")
        else:
            counter = 1
            for purse in purses.values():
                print("id:%d. %s | %d. " % (counter, purse.ccy, purse.total))
                counter += 1
            input_is_correct = False
            while not input_is_correct:
                id = prompt('Enter id of purse for update:: ')
                if self.__number_is_valid(id) and 1 <= int(id) < counter:
                    upd_purse = list(self.storage.get_all().values())[int(id) - 1]
                    sum = prompt('Enter new sum for updating:: ')
                    if self.__number_is_valid(sum):
                        upd_purse.total = int(sum)
                        input_is_correct = self.__try_to_add_or_change_task("UAH", upd_purse)
                        if not input_is_correct:
                            print("Your input was not valid, try again")
                    else:
                        print("Your input was not valid, try again")
                else:
                    print("Your input was not valid, try again")

    def __get_purses(self):
        purses = self.storage.get_all()
        if len(purses) == 0:
            print("No purses")
        else:
            for purse in purses.values():
                print("%s | %d. | %s" % (purse.ccy, purse.total, purse.id))

    def __create_purse(self):
        input_is_correct = False
        while not input_is_correct:
            ccy = prompt('Enter ccy:: ')
            input_is_correct = self.__try_to_add_or_change_task(ccy, None)
            if not input_is_correct:
                print("Your input was not valid, try again")

    def __delete_purse(self):
        clear()
        purses = self.storage.get_all()
        if len(purses) == 0:
            print("No purses")
        else:
            counter = 1
            for purse in purses.values():
                print("id:%d. %s | %d. " % (counter, purse.ccy, purse.total))
                counter += 1
            input_is_correct = False
            while not input_is_correct:
                id = prompt('Enter id of purse for deleting:: ')
                if self.__number_is_valid(id) and 1 <= int(id) < counter:
                    del_purse = list(self.storage.get_all().values())[int(id) - 1]
                    self.storage.delete_by_id(del_purse.id)
                    input_is_correct = True

    def __try_to_add_or_change_task(self, ccy, purse):

        if purse is not None:
            self.storage.update_by_id(purse.id, {"ccy": purse.ccy, "total": purse.total})
        else:
            self.storage.insert(Purse({"ccy": ccy, "total": 1000}))
        return True

    @staticmethod
    def __exit():
        sys.exit()

    @staticmethod
    def __number_is_valid(number):
        try:
            int(number)
            return True
        except ValueError:
            return False
