if __name__ == '__main__':
    from engine.engine import Engine

    app = Engine()
    app.init()
    app.change_scene('SampleScene')
    app.run()
