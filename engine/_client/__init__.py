def run_client(input_, output, encoding):
    from .controller import Controller
    ctrl = Controller(input_, output, encoding)
    ctrl.run()
