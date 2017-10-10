import subprocess

def callPlay(url):
    url = https2http(url)
    ####### TODO !!!!!!
    cp = subprocess.run(["mpg123", url])

def https2http(url):
    return url.replace("https://", "http://")

