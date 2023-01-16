import asyncio
import aiohttp
import tkinter
import requests
import io
from tkinter import ttk
from PIL import Image, ImageTk
from bs4 import BeautifulSoup


imgs = []
num = 0
per = 0.00


async def do_req(session,img_url,list,tag):
    try:
        async with session.get(img_url) as resp:
            if resp.status == 200:
                res = await resp.read()
                if res:
                    img = Image.open(io.BytesIO(res))
                    #print(type(img))
                    tup = (tag.split("/")[-1],img)
                    imgs.append(tup)
                    list.insert(tkinter.END, tag.split("/")[-1])
    except:
        print("Invalid URL")


async def req(urls,list,progress):
    async with aiohttp.ClientSession() as session:
        i = 0
        tasks = []
        for tag in urls:
            #print(tag)
            progress.step(per)
            if not 'https://' in tag:
                tag = 'https:'+tag
            tasks.append(
                do_req(session,tag,list,tag)
            )
            i = i + 1
        await asyncio.gather(*tasks)
        
            
def asy(url,list,progress,cont):
    global num,per
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    img_tags = soup.find_all('img')
    print(type(img_tags))
    urls = []
    for img in img_tags:
        num += 1
        try:
            try:
                urls.append(img['data-src'])
            except:
                urls.append(img['src'])
        except:
            print("No SRC")
    print(urls)
    print(num)
    cont.set("Imagenes encontradas =" + str(num))
    per = 99.99/num
    asyncio.run(req(urls,list,progress))


def create_window():
    
    def buttonHandler(evt):
       w = evt.widget
       index = int(w.curselection()[0])
       im =  imgs[index][1]
    
       #image = im.resize((400,400), Image.ANTIALIAS)
       photo = ImageTk.PhotoImage(im)

       label = tkinter.Label(image=photo)
       label.image=photo
       label.grid(column=2,row=2)
       label.config(width=300,height=300)
    
    window = tkinter.Tk()
    window.title("Practica 1")
    window.geometry("600x700")

    url=tkinter.StringVar()
    tkinter.Label(text="URL a procesar").grid(pady=10,padx=10,row=0,column=0,)
    
    entry=tkinter.Entry(textvariable=url)
    entry.grid(pady=10,padx=10,column=1,row=0)

    list=tkinter.Listbox()
    list.bind('<<ListboxSelect>>', buttonHandler)
    list.grid(pady=10,padx=10,column=0,row=2)
    
    im=Image.open("default-placeholder.png")
    image = im.resize((400,400), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)

    label = tkinter.Label(image=photo)
    label.image=photo
    label.grid(column=2,row=2)
    label.config(width=250,height=250)

    progress = ttk.Progressbar()
    progress.grid(column=1,row=3)

    cont = tkinter.StringVar()
    cont.set("Imagenes encontradas = 0")
    l = tkinter.Label(textvariable=cont)
    l.grid(row=4,column=1)

    tkinter.Button(text="Buscar",command=lambda: asy(entry.get(),list,progress,cont)).grid(pady=10,padx=10,column=0,row=1,sticky="snwe")

    window.mainloop()
    

if __name__ == '__main__':
    create_window()