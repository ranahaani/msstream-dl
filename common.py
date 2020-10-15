class Common:

    @staticmethod
    def log(self, message_type='message'):
        """
        Log (print) messages to stdout
        TODO: Log to file and use stderr for logging error messages
        Parameters:
        ==========
        > message (string): Message to log
        > message_type (string)(optional): Type of message ('error'/'warning'/'info'/[empty=unformatted])
        """
        if message_type == 'error':
            if 'ERROR' in self:
                self = self.replace('ERROR:', '\033[31mError:\033[0m')
                print('{0}'.format(self))
            else:
                print("\033[31mError:\033[0m {0}".format(self))
        elif message_type == 'info':
            print('\033[36m{0}\033[0m'.format(self))
        elif message_type == 'warning':
            print("\033[33mWarning:\033[0m {0}".format(self))
        else:
            print('{0}'.format(self))
