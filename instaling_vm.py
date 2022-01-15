import subprocess
with open("requirements_scraper.txt", "r", newline="") as f:
    lines = f.readlines()
    for l in lines:
        l = l.replace("\n", "")
        subprocess.run("pip install {}".format(l).split(" "))

