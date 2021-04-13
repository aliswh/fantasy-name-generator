# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import TextField,SubmitField
from wtforms.validators import NumberRange

import pandas as pd # data frames
import numpy as np # arrays
from keras.models import load_model
import math



longest_len = 0
num_names = 0
alph_len = 0

def define_var():
  ds = pd.read_csv('dataset.csv')
  newletters = []
  # get alphabet = all letters that appear in names
  for w in ds['Name']:
    for c in w:
      if c not in newletters:
        newletters.append(c)
  newletters = sorted(newletters)

  alphabet = dict((newletters[i],i) for i in range(0,len(newletters)))
  alphabet_index = dict((i,newletters[i]) for i in range(0,len(newletters)))
  list(alphabet.items())[:10] # show head of dict

  longest_len = len(max(ds['Name'], key=len)) # length of longest name = columns
  num_names = len(ds['Name']) # number of names in the dataset = rows
  alph_len = len(alphabet)

  X = np.zeros((num_names, longest_len, alph_len)) # 3-dimensional array of zeros (rows,columns,depth)
  Y = np.zeros((num_names, longest_len, alph_len))

  for i in range(num_names): # scan by row
    name_i = list(ds['Name'][i]) # get name
    for j in range(len(name_i)): # scan by column
      X[i, j, alphabet[name_i[j]]] = 1 # set to one according to alphabet dict
      if j < len(name_i)-1:
        Y[i, j, alphabet[name_i[j+1]]] = 1
  
  return longest_len, num_names, alph_len, alphabet, alphabet_index

def generator():
  name = [] # generated name
  x = np.zeros((1, longest_len, alph_len))
  x[0:,0:,3:28] = 0.1 # initialize weights to give more importance to some letters (standard alphabet)
  i = 0

  end = False
  while end==False:
    probability_distrubution = list(model.predict(x)[0,i])
    probability_distrubution = probability_distrubution / np.sum(probability_distrubution)
    index = np.random.choice(range(alph_len), p=probability_distrubution) # choose random letter from updated probability

    if i == longest_len-2: # if at second-last possible position, exit while
      character = '.'
      end = True
    else: 
      character = alphabet_index[index]
    name.append(character) # add new char to name

    x[0, i+1, index] = 1/((i+0.001)**0.1) # give less importance after each iteration, to have shorter names
    i += 1

    if character == '.':
      end = True
    
    if len(name)<2 or character=='\'' or character=='-' or character==' ': # continue if TODO
      end = False

  result = ''.join(name).capitalize().strip('.')
  return result

model = load_model('model/model.h5')
longest_len, num_names, alph_len, alphabet, alphabet_index = define_var()
  

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SomeKeyWillDo'

class FlowerForm(FlaskForm):
  namefield = TextField('')
  submit = SubmitField('Generate new name')

@app.route('/', methods=['GET', 'POST'])
def index():
  form = FlowerForm()
  if form.validate_on_submit():
    return redirect(url_for("prediction"))
  return render_template('main.html', form=form)

@app.route('/prediction')
def prediction():
    content = {}
    content['name']= float(session['namefield'])
    result = generator()
    return render_template('prediction.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

