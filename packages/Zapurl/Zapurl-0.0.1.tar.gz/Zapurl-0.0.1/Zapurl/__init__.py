import requests

def short(url):
  shortener = 'http://zapurl.unaux.com/create.php/'
  urlin = {'urlin': url}

  file = requests.post(shortener, data = urlin)
  file = file.text
  print(file[604:637])

