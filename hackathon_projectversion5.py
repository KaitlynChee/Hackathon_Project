from sys import dllhandle
from tkinter.constants import X
import PySimpleGUI as sg
import tkinter.font as font
import random
import PySimpleGUI as psg
from PIL import Image

#window 1--defs for creating possible ranges
def chooseColor(finalDesc):
    RGB_range = random.choice(finalDesc)
    R_range = random.choice(range(RGB_range[0][0], RGB_range[0][1]+1))
    G_range = random.choice(range(RGB_range[1][0],RGB_range[1][1]+1))
    B_range = random.choice(range(RGB_range[2][0],RGB_range[2][1]+1))
    return [R_range, G_range, B_range]

def compRange(r1,r2):                       
    finalMin = max(r1[0],r2[0])
    finalMax = min(r1[1],r2[1])
    if finalMax >= finalMin:
        return [finalMin,finalMax]
    else: 
        return False
def compRGB(RGB1, RGB2):
    finalRGB = []
    for i in range(len(RGB1)):
        if compRange(RGB1[i],RGB2[i]) != False:
            finalRGB.append(compRange(RGB1[i],RGB2[i]))
        else:
            return False
    return finalRGB
def compDesc(d1,d2):
    finalDesc = []
    for i in range(len(d1)):
        for j in range(len(d2)):
            if compRGB(d1[i],d2[j]) != False:
                finalDesc.append(compRGB(d1[i],d2[j]))
    if len(finalDesc) == 0:
        return 'no intersection'
    else:
        return finalDesc
def findFinalDesc(descs):
    finalDesc = descs[0] 
    i = 1
    while i < len(descs):
        if finalDesc == "no intersection":
            return "no intersection!"
        finalDesc = compDesc(finalDesc,descs[i])
        i += 1
    return finalDesc

#definitions
descriptors_dictionary = {"bold": [[[230,255],[0,200],[0,200]], [[0,200],[230,255],[0,200]],[[0,200],[0,200],[230,255]]], "convenient" : [[[1,210],[255, 255],[0,254]]], "environmental":[[[1,90], [1,120], [255,255]],[[1,220], [255,255], [1,120]]], "fun":[[[255,255],[0,255],[0,200]],[[0,255],[255,255], [0,200]], [[0,200], [0,255], [255,255]]], "luxury": [[[0,0],[0,0],[0,0]],[[255,255],[255,255],[255,255]],[[230,230], [153,153], [0,0]], [[192,192],[192,192],[192,192]], [[205,205],[127,127],[50,50]]], "retro" : [[[196,196],[98,98],[16,16]],[[146,146],[214,214],[207,207]],[[0,0], [128,128],[153,153]],[[106,106],[128,128],[0,0]],[[128,128],[85,85],[0,0]],[[204,204],[153,153],[102,102]],[[239,239],[222,222],[205,205]],[[200,200],[255,255],[200,200]],[[205,205],[60,60],[80,80]],[[179,179],[132,132],[190,190]]], "youthful" : [[[179,230],[30,255],[30,255]],[[30,255], [179,230], [30,255]],[[30,255],[30,255],[179,230]]]}
descriptors = ["bold",  "convenient", "enviromental", "fun", "luxury", "retro", "youthful"]
number = [1, 2, 3]

#first window 
psg.theme("LightPurple")
layout = [
    [sg.Text('Welcome to starting block! \nHere to help you start your new business! Generate your first color palette. \n \nSelect 1-3 brand qualities:', font='Lucida', text_color = 'White')],
    [sg.Checkbox(text, 0, font='Lucida', text_color = 'White', key = text) for text in descriptors_dictionary.keys()],
    [sg.Text('Select how many colors you would like:', font='Lucida', text_color = 'White')],
    [sg.Radio(text, 2, font='Lucida', text_color = 'White') for text in number],
    [sg.Button('Go', font='Lucida')]
    ]

window = sg.Window('Hackathon Project', layout)

#first event loop
while True:             
    event, values = window.Read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "Go":
        selectedDescriptors = []
        for desc in values.keys():
            if values[desc] == True and desc != 0 and desc !=1 and desc != 2:
                selectedDescriptors.append(desc)
        descs = []
        for desc in selectedDescriptors:
            descs.append(descriptors_dictionary[desc])
        finalDesc = findFinalDesc(descs)
        if finalDesc=='no intersection':
            psg.theme('LightBlue1')
            layout3 = [
            [sg.Text('No available colors corresponding to all the selected descriptors', font='Lucida', text_color ="White")],
            [sg.Text('Please try again using different descriptors', font='Lucida', text_color ="White")]
            ]
            window = sg.Window("Color Paletes", layout3)
            
            while True:             
                event, values = window.Read()
                if event == sg.WINDOW_CLOSED:
                    break
                window.close()
        else:
#amount of colors selected
            colors = 0
            for desc in values.keys():
                if values[desc]==True:
                    if desc == 0:
                        colors = 0
                    elif desc == 1:
                        colors = 1
                    elif desc == 2:
                        colors = 2
            colorValues = []
            for i in range(3):
                palete = []
                for j in range(colors + 1):
                    palete.append(chooseColor(finalDesc))
                colorValues.append(palete)
            
            for p in colorValues:
                for c in p:
                    im = Image.new(mode= "RGBA",size = (500,500), color = (c[0],c[1],c[2],255))
                    im.save(str(c) + ".png")
    #third window
            psg.theme('LightBlue1')
            layout3 = [
                [sg.Text('Here are your custom color paletes!\n ', font = 'Lucida',text_color ='White')],
                [sg.Text('Palete #1', font='Lucida', text_color= 'White'), sg.Button('Download', font='Lucida', button_color=('black','white'),key = "b1")],
                [sg.Text(str(colorValues[0]), text_color='White')],
                [sg.Image(str(image)+".png",size = (40,40)) for image in colorValues[0]],
                [sg.Text('Palete #2', font='Lucida', text_color= 'White'), sg.Button('Download', font='Lucida', button_color=('black','white'), key = "b2")],
                [sg.Text(str(colorValues[1]), text_color='White')],
                [sg.Image(str(image)+".png",size = (40,40)) for image in colorValues[1]],
                [sg.Text('Palete #3', font='Lucida', text_color= 'White'), sg.Button('Download', font='Lucida', button_color=('black','white'), key = "b3")],
                [sg.Text(str(colorValues[2]), text_color='White')],
                [sg.Image(str(image)+".png",size = (40,40)) for image in colorValues[2]],
            ]
            window = sg.Window("Color Paletes", layout3)
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    break
                if event == "b1":
                    f=open("palete1.txt", "w")
                    f.write(str(colorValues[0]))
                    f.close()
                if event == "b2":
                    f= open("palete2.txt","w")
                    f.write(str(colorValues[1]))
                    f.close()
                if event == "b3":
                    f= open("palete2.txt","w")
                    f.write(str(colorValues[2]))
                    f.close()
            window.close()
    window.Close()
            
                    
                
            
            
        
