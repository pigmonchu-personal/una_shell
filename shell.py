import itertools


def get_user_input():
    for i in itertools.count():
        try:
            yield i, input('In [{}]: '.format(i))
        except KeyboardInterrupt:
            print()
            pass
        except EOFError:
            print()
            break

def exec_function(user_input):
    '''
    if user_input is an expression:
        return eval
    else:
        return exec
    '''
    
    try:
        compile(user_input, '<stdin>', 'eval')
    except SyntaxError:
        return exec
    return eval

def exec_user_input(i, user_input, user_globals):
    
    user_globals = user_globals.copy()
    
    try: 
        retval = exec_function(user_input)(
            user_input, user_globals
        )

        if retval is not None:
            print('Out [{}]: {}'.format(i, retval))
    except Exception as e:
        print("{}: {}".format(e.__class__.__name__, e))
    
    return user_globals

def selected_user_globals(user_globals):
    return (
        (key, user_globals[key])
        for key in sorted(user_globals)
        if not key.startswith('__') or not key.endswith('__')
    )

def save_user_globals(user_globals, path='user_globals.txt'):
    with open(path, 'w') as fd:
        for key, val in selected_user_globals(user_globals):
            fd.write("{} = {} ({})\n".format(
                key, val, val.__class__.__name__
            ))

def main():
    user_globals = {}

    for i, user_input in get_user_input():
        user_globals = exec_user_input(
            i, user_input, user_globals
        )
        save_user_globals(user_globals)
    
if __name__ == '__main__':
    main()
        