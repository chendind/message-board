# -*- coding: utf-8 -*-
#!/usr/bin/env python
from app import create_app, db
from config import config
from flask_script import Manager, Shell
from flask_migrate import Migrate

app = create_app(config['default'])

@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()