import time

animation = "|/-\\"
idx = 0
while True:
    print animation[idx % len(animation)] + "\r",
    idx += 1
    time.sleep(0.1)