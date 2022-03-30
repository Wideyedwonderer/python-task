import BookService
import UserService
from models.book import Book
from utils import infinite_input


actions = [
    BookService.add_new_book,
    BookService.remove_book,
    BookService.is_book_available,
    BookService.checkout_book,
    BookService.return_book,
    BookService.subscribe_to_book,
    BookService.print_notifications_for_subscribed_books,
    UserService.add_user,
    UserService.remove_user,
    UserService.get_book_subscriber_ids,
    UserService.get_overdue_books_isbns,
    UserService.get_overdue_fine,
    UserService.get_total_fine_for_user,
    UserService.get_users_who_checked_out_book,
    ]
actions_names = list(map(lambda action: action.__name__, actions))
# action_arguments = list(map(lambda action: list(inspect.signature(action)), actions))
# print(action_arguments)

indexes = [i for i in range(len(actions))]
prompt = 'Please choose one of the following actions:\n'

for index in indexes:
    prompt += '(' + str(index) + ') ' + actions_names[index] + "\n"

def inf_action_prompt():
    chosen_action_index = int(infinite_input(prompt, list(map(lambda index: str(index), indexes))))
    action = actions[chosen_action_index]
  
    func_arg_count = action.__code__.co_argcount

    func_vars_names = list(action.__code__.co_varnames)
    func_arg_names = func_vars_names[0:func_arg_count]
    
    func_argument_values = []

    print(func_arg_names)
    for arg_name in func_arg_names:
        _prompt = "\nPlease provide " + arg_name
        func_argument_values.append(infinite_input(_prompt))
    try:
        res = action(*func_argument_values)
        print('\n \033[92m Success! \033[0m \n')
        if res != None:
          print(res)
          print('\n')
    except BaseException as err:
        print('\n\033[91m' + str(err)+ '\n \033[0m')
    inf_action_prompt()

inf_action_prompt()
