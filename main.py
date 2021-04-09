import os
import sys

sys.path.insert(1, os.path.join('function'))

import render

if __name__ == "__main__":
    render.main_connected()
    myapp = render.Main()
    myapp.main()
