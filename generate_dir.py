import sys
import os
import pinout

path = os.path.abspath(sys.argv[1])

if not os.path.exists(path):
    sys.exit("ERROR: Path does not exist: " + path)

folder_name = os.path.split(path)[1].lower()

files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
         and f[0:len(folder_name)] == folder_name
         and f.endswith((".yaml"))
        ]

for f in files:
    chart = pinout.Package()
    chart.load_data(os.path.join(path, f))
    
    chart_path = os.path.join(path, f.removesuffix(".yaml") + ".svg")
    print(chart_path)
    chart.save(chart_path)
