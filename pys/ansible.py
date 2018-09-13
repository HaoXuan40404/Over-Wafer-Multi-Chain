class Ansible:
    '''
    ansible
    '''
    user = ''
    dir = ''

    def __repr__(self):
        return '[user] %s, [dir] %s' % (Ansible.user, Ansible.dir)

def set_user(user):
    Ansible.user = user

def set_dir(dir):
    Ansible.dir = dir 

def ansible_test():
    ae = Ansible()
    set_user('app')
    set_dir('dir')
    print(ae)

if __name__ == '__main__':
    ansible_test()