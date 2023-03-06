'''

A companion for Clue

- keep track of cards
- 2+ player modes
- deductions based on suggestions & accusations

'''

import tkinter as tk
from tkinter import ttk # for separators

ROOMS = ['ball', 'conservatory', 'billiard', 'library', 'study', 'hall', 'lounge', 'dining', 'kitchen']
SUSPECTS = ['plum', 'white', 'scarlet', 'green', 'mustard', 'peacock']
WEAPONS = ['rope', 'dagger', 'wrench', 'pistol', 'candlestick', 'pipe']

# constants for positioning
TABLE_FIRST_ROW = 1

class toggleButton(tk.Button):
  def __init__(self, tkParent, r, c, callback) -> None:
    super().__init__(tkParent)
    self.object = None
    self.matrixR = None
    self.matrixC = None
    self['height'] = 1
    self['width'] = 10
    self['relief'] = 'raised'
    self['bg'] = 'white'
    self['command'] = lambda: self.handleClick(callback)
    self.grid(row = r, column = c, padx = 0, pady = 0.5)

  def handleClick(self, callback):
    callback(self, self.matrixR, self.matrixC, self.object)

    if self['relief'] == 'raised':
      self['relief'] = 'sunken'
      self['bg'] = 'red'
    else:
      self['relief'] = 'raised'
      self['bg'] = 'white'

class Player:
  def __init__(self) -> None:
    self.name = None
    self.possibleCards = []
    self.resetCards()
  
  def setName(self, string: str) -> bool:
    self.name = string
    return True
  
  def resetCards(self):
    for suspect in SUSPECTS:
      self.possibleCards.append(suspect)
    for weapon in WEAPONS:
      self.possibleCards.append(weapon)
    for room in ROOMS:
      self.possibleCards.append(room)

class ButtonEntryFrame(tk.Frame):
  def __init__(self, parent, r, c, prompt, buttonText, callback ) -> None:
    # frame
    super().__init__(parent)
    self['background'] = 'light gray'
    self.grid(row = r, column = c)

    # label
    self.label = tk.Label(self, text = prompt)
    self.label.grid(row = 0, column = 0, padx = 5, pady = 5)

    # entry
    self.stringVar = tk.StringVar()
    self.entry = tk.Entry(self, textvariable = self.stringVar)
    self.entry.grid(row = 0, column = 1)

    # button
    self.actionButton = tk.Button(self, text = buttonText, command = lambda: self.executeCallback(callback, self.stringVar.get()))
    self.actionButton.grid(row = 0, column = 2)
  
  def executeCallback(self, callback, string): # doubt this is necessary
    if callback(string):
       self.actionButton['state'] = 'disabled'
       self.entry['state'] = 'disabled'

class TableFrame(tk.Frame):
  def __init__(self, tkParent, numberOfPlayers) -> None:
    super().__init__(tkParent)
    self['relief'] = 'sunken'
    self.grid(row = TABLE_FIRST_ROW, column = 0, padx = 5, pady = 5)

    self.numberOfPlayers = numberOfPlayers
    self.objectLabels = {}
    self.players = []
    self.matrix = []

    self.createObjects()
    self.createPlayers()
    self.createButtons()

  def createObjects(self):
    r = 1 # make space for names of players
    for suspect in SUSPECTS:
      label = tk.Label(self, text = suspect)
      self.objectLabels[suspect] = label
      label.grid(row = r, column = 0)
      r += 1
    # separator
    s = ttk.Separator(self, orient = tk.HORIZONTAL)
    s.grid(row = r, column = 0, columnspan = self.numberOfPlayers + 1, sticky = 'ew')
    r += 1
    #
    for weapon in WEAPONS:
      label = tk.Label(self, text = weapon)
      self.objectLabels[weapon] = label
      label.grid(row = r, column = 0)
      r += 1
    # separator
    s = ttk.Separator(self, orient = tk.HORIZONTAL)
    s.grid(row = r, column = 0, columnspan = self.numberOfPlayers + 1, sticky = 'ew')
    r += 1
    #
    for room in ROOMS:
      label = tk.Label(self, text = room)
      self.objectLabels[room] = label
      label.grid(row = r, column = 0)
      r += 1
  
  def createPlayers(self):
    c = 1 # make space for objects
    for p in range(self.numberOfPlayers):
      player = Player()
      self.players.append(player)
      ButtonEntryFrame(self, 0, c, f'P{p} ->', 'x', player.setName)
      c += 1

  def createButtons(self):
    r = 0
    for suspect in SUSPECTS:
      row = []
      c = 0
      for player in self.players:
        button = toggleButton(self, r + 1, c + 1, self.clickCallback)
        button.matrixR = r
        button.matrixC = c
        button.object = suspect
        row.append(button)
        c += 1
      self.matrix.append(row)
      r += 1

    for weapon in WEAPONS:
      row = []
      c = 0
      for player in self.players:
        #                      separator compensation
        button = toggleButton(self, r + 2, c + 1, self.clickCallback)
        button.matrixR = r
        button.matrixC = c
        button.object = weapon
        row.append(button)
        c += 1
      self.matrix.append(row)
      r += 1

    for room in ROOMS:
      row = []
      c = 0
      for player in self.players:
        #                      separator compensation
        button = toggleButton(self, r + 3, c + 1, self.clickCallback)
        button.matrixR = r
        button.matrixC = c
        button.object = room
        row.append(button)
        c += 1
      self.matrix.append(row)
      r += 1
  
  def clickCallback(self, lebutton, r, c, object):
    if self.objectLabels[object]['bg'] != 'red':
      self.objectLabels[object]['bg'] = 'red'
    else:
      self.objectLabels[object]['bg'] = 'white'

    if lebutton['relief'] == 'raised':
      # disable all buttons (except this) in this row
      for button in self.matrix[r]:
        if button == lebutton:
          continue
        button['state'] = 'disabled'
        button['bg'] = 'orange'
    else:
      # enable all buttons (except this) in this row
      for button in self.matrix[r]:
        if button == lebutton:
          continue
        button['state'] = 'active'
        button['bg'] = 'white'

class GameFrame(tk.Frame):
  def __init__(self, tkParent) -> None:
    super().__init__(tkParent)
    self.grid(row = 0, column = 0)
    self.numberOfPlayersEntry = ButtonEntryFrame(self, 0, 0, 'Number of players ->', 'Start', self.verifyNumberOfPlayers)
    self.table = None
  
  def verifyNumberOfPlayers(self, string: str) -> bool:
    try:
        numberOfPlayers = int(string)
    except ValueError as verr:
        print(verr)
        return False
    if numberOfPlayers < 2 or numberOfPlayers > 6:
      print("Invalid numberOfPlayers (must be 2-6)")
      return False
    
    self.createTable(numberOfPlayers)
    return True
  
  def createTable(self, numberOfPlayers):
    self.table = TableFrame(self, numberOfPlayers)

# main application window
class Main(tk.Tk):
  def __init__(self) -> None:
    super().__init__()
    self.title('Clue Companion')

    self.gameFrame = GameFrame(self)

    # start event loop
    self.mainloop()

# configure weigth for resizing
#root.rowconfigure(0, weight=1)
#root.columnconfigure(0, weight=1)

Main()