import random

with open("python_sequence.txt", "w") as f:
    f.write("".join(str(random.randint(0, 1)) for _ in range(128)))
