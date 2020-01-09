#264421996321-auq2cmaphedi5fkgb82c201jq9787ggv.apps.googleusercontent.com
#zdk8MSweYhcT-2KBXTQ4rk1o
import PySimpleGUI as sg
import psutil
import re
import pyautogui
import cal
import os.path
import pickle
import datetime


# ----------------  Create Window  ----------------
sg.ChangeLookAndFeel('Black')
frames=[]
for i in range(1,10):
    block_layout =[[sg.Text(text='calendar event {0}'.format(i),
                            key='calendar_test{0}'.format(i),
                           background_color='#57F548', text_color='black',
                            font=('Helvetica', 20), size=(20,10))],
        [sg.Button(button_text='test{0}'.format(i), button_color=('red',
                                                                  'blue'),
                   key='test{0}'.format(i))]]
    frames.append(sg.Frame(title=None,layout=block_layout,key='frame{0}'.format(i),
                          background_color='#57F548'))

layout = [[sg.Text('Calendar events', background_color='white',
                   text_color='black', font=('Helvetica', 20))],
          frames[:5],
          frames[5:],
          [sg.Exit(button_color=('white', 'firebrick4'), pad=((15, 0), 0))]]

window = sg.Window('Running Timer', layout, no_titlebar=True,
                   background_color='white',
                   auto_size_buttons=False, keep_on_top=True,
                   grab_anywhere=True, location=(0,0), size=pyautogui.size()).Finalize()
window.Maximize()

if os.path.exists('events.pickle'):
   with open('events.pickle', 'rb') as token:
    events = pickle.load(token)
else:
    events = cal.get_events()
    with open('events.pickle', 'wb') as token:
            pickle.dump(events, token)

print(type(events))
print(events)
it = 1
for i in events:
    if (it == 10):
        break;
    window['calendar_test{0}'.format(it)].Update(value="{0}\n\n{1}".format(i, events[i]))
    window['frame{0}'.format(it)].expand(expand_y=True)
    window['calendar_test{0}'.format(it)].expand(expand_y=True)
    it = it + 1

# ----------------  main loop  ----------------
while (True):
    # --------- Read and update window --------
    event, values = window.read(timeout=0)

    # --------- Do Button Operations --------
    if event is None or event == 'Exit':
        break
    test_pattern = re.compile('test[0-9]')
    if re.match(test_pattern, event):
        print('GOT A MATCH on {0}'.format(event))
        #window['calendar_{0}'.format(event)].update('deleted')
        window['frame{0}'.format(event[event.find('test')+4])].update(visible=False)
    try:
        interval = int(values['spin'])
    except:
        interval = 1


    # --------- Display timer in window --------


# Broke out of main loop. Close the window.
print(events)
window.close()
