import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def stackov():
  url = "https://stackoverflow.com/questions/tagged/python?sort=MostVotes&edited=true"
  page = requests.get(url).text
  soup = BeautifulSoup(page, 'html.parser')
  questions = soup.find('div', attrs = {'id' : 'questions'}).find_all('div', attrs = {'class' : 's-post-summary js-post-summary'})
  subjects = []
  views = []
  votes = []
  links = []
  for question in questions:
    subjects.append(question.find('a', attrs = {'class' : 's-link'}).text.replace('[duplicate]', '')) 
    views.append(question.find('div', attrs = {"class" : "s-post-summary--stats-item is-supernova"}).text.replace('\n', ' ').strip())
    votes.append(question.find('div', attrs = {"class" : "s-post-summary--stats-item s-post-summary--stats-item__emphasized"}).text.replace('\n', ' ').strip())
    links.append("https://stackoverflow.com" + question.find('a', attrs = {'class' : 's-link'})['href'])

  data = list(zip(subjects, views, votes, links))
  return render_template('python_hof.html', data = data)
  
if __name__ == "__main__":
  app.run(host='127.0.0.1', port=5002, debug = True)


