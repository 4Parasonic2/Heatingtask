import numpy as np
import time
import subprocess




# Measure the time taken to execute the command
start_time = time.time()
# Run the simulate.py script with a system argument 20
subprocess.run(["python3", "/zhome/99/4/213789/projectwork/simulate.py", "20"])
end_time = time.time()

execution_time = end_time - start_time
print(f"Time taken to execute the 1st command: {execution_time} seconds")

