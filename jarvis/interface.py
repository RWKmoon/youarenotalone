import tkinter as tk
import random
import math
import psutil
import time
from spotify_control import musica_info
from PIL import Image, ImageTk
import requests
from io import BytesIO

width = 1300
height = 850
radius = 220

musica_spotify = "Nada tocando"
texto_voz = "..."
estado_voz = "idle"
spotify_data = None
album_img = None
spotify_timer = 0
spotify_interval = 2

ultima_musica = None
album_angle = 0

def atualizar_texto_voz(texto):
    global texto_voz
    texto_voz = texto

def estado_microfone(status):
    global estado_voz
    estado_voz = status

def iniciar_interface():

    root = tk.Tk()
    root.title("JARVIS AI SYSTEM")
    root.configure(bg="black")
    root.attributes("-fullscreen", True)

    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    canvas = tk.Canvas(root,width=width,height=height,bg="black",highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    root.update()
    
    points=[]
    satellites=[]
    particles=[]
    stars=[]

    for i in range(220):

        theta=random.uniform(0,2*math.pi)
        phi=random.uniform(0,math.pi)

        x=radius*math.sin(phi)*math.cos(theta)
        y=radius*math.sin(phi)*math.sin(theta)
        z=radius*math.cos(phi)

        points.append([x,y,z])

    for i in range(6):
        satellites.append(random.uniform(0,360))

    for i in range(140):
        particles.append([
            random.randint(0,width),
            random.randint(0,height),
            random.uniform(0.5,2)
        ])

    for i in range(100):
        stars.append([
            random.randint(0,width),
            random.randint(0,height)
        ])

    cpu_history=[0]*80

    angle=0
    radar=0
    pulse=0

    def rotateY(x,z,a):

        cosA=math.cos(a)
        sinA=math.sin(a)

        x2=x*cosA-z*sinA
        z2=x*sinA+z*cosA

        return x2,z2

    def draw():
        global spotify_data, album_img, musica_spotify, spotify_timer, ultima_musica
        nonlocal angle,radar,pulse

        tempo_atual = 0
        tempo_total = 1

        agora = time.time()

        if agora - spotify_timer > spotify_interval:

            spotify_timer = agora

            try:
                spotify_data = musica_info()

                if spotify_data:

                    musica_atual_nome = spotify_data["titulo"] + spotify_data["artista"]

                    musica_spotify = f'{spotify_data["titulo"]} - {spotify_data["artista"]}'

                    if musica_atual_nome != ultima_musica:

                        ultima_musica = musica_atual_nome

                        response = requests.get(spotify_data["capa"])

                        img = Image.open(BytesIO(response.content))
                        img = img.resize((120,120))

                        album_img = ImageTk.PhotoImage(img)

            except:
                pass

        canvas.delete("all")

        cx = width * 0.35
        cy = height / 2

        projected=[]

        for s in stars:
            canvas.create_oval(s[0],s[1],s[0]+1,s[1]+1,fill="#ae4aff",outline="")

        pulse+=0.05
        pulse_radius=radius+math.sin(pulse)*10

        canvas.create_oval(
            cx-pulse_radius,
            cy-pulse_radius,
            cx+pulse_radius,
            cy+pulse_radius,
            outline="#8c00ff"
        )

        for p in points:

            x,y,z=p
            x,z=rotateY(x,z,angle)

            distance=600
            scale=distance/(distance+z)

            px=cx+x*scale
            py=cy+y*scale

            projected.append((px,py))

            canvas.create_oval(px-2,py-2,px+2,py+2,fill="#ae4aff",outline="")

        for i in range(len(projected)):
            for j in range(i+1,len(projected)):

                x1,y1=projected[i]
                x2,y2=projected[j]

                dist=math.hypot(x1-x2,y1-y2)

                if dist<45:
                    canvas.create_line(x1,y1,x2,y2,fill="#8c00ff")

        for r in range(1,4):

            canvas.create_oval(
                cx-radius*r*0.6,
                cy-radius*r*0.25,
                cx+radius*r*0.6,
                cy+radius*r*0.25,
                outline="#ae4aff"
            )

        radar+=2

        sx=cx+math.cos(math.radians(radar))*radius
        sy=cy+math.sin(math.radians(radar))*radius

        canvas.create_line(cx,cy,sx,sy,fill="#ae4aff",width=2)

        for i in range(len(satellites)):

            satellites[i]+=0.7
            a=math.radians(satellites[i])

            sx=cx+math.cos(a)*(radius*1.4)
            sy=cy+math.sin(a)*(radius*0.5)

            canvas.create_oval(sx-4,sy-4,sx+4,sy+4,fill="#ffffff")
            canvas.create_line(cx,cy,sx,sy,fill="#ae4aff")

        for p in particles:

            x,y,s=p

            y+=0.3
            if y>height:
                y=0

            p[1]=y

            canvas.create_oval(x,y,x+s,y+s,fill="#8c00ff",outline="")

        cpu=psutil.cpu_percent()
        ram=psutil.virtual_memory().percent
        disk=psutil.disk_usage('/').percent

        cpu_history.append(cpu)
        cpu_history.pop(0)

        hud_x = width - 220

        canvas.create_text(hud_x,70,text="JARVIS SYSTEM",fill="#ae4aff",font=("Consolas",20))

        canvas.create_text(hud_x,140,text=f"CPU {cpu}%",fill="#ae4aff",font=("Consolas",14))
        canvas.create_rectangle(hud_x-90,160,hud_x-90+cpu*1.5,180,fill="#8c00ff")

        canvas.create_text(hud_x,210,text=f"RAM {ram}%",fill="#ae4aff",font=("Consolas",14))
        canvas.create_rectangle(hud_x-90,230,hud_x-90+ram*1.5,250,fill="#8c00ff")

        canvas.create_text(hud_x,280,text=f"DISK {disk}%",fill="#ae4aff",font=("Consolas",14))
        canvas.create_rectangle(hud_x-90,300,hud_x-90+disk*1.5,320,fill="#8c00ff")

        graph_x=hud_x-120
        graph_y=380

        for i in range(len(cpu_history)-1):

            x1=graph_x+i*3
            y1=graph_y-cpu_history[i]

            x2=graph_x+(i+1)*3
            y2=graph_y-cpu_history[i+1]

            canvas.create_line(x1,y1,x2,y2,fill="#ae4aff")

        canvas.create_text(hud_x,420,text="CPU GRAPH",fill="#ae4aff",font=("Consolas",12))

        canvas.create_text(hud_x,480,text="AI STATUS: ONLINE",fill="#ae4aff",font=("Consolas",14))
        canvas.create_text(hud_x,510,text="VOICE: ACTIVE",fill="#ae4aff",font=("Consolas",14))
        canvas.create_text(hud_x,540,text="NETWORK: MONITORING",fill="#ae4aff",font=("Consolas",14))

        if spotify_data:

            canvas.create_text(width-220,600,text="SPOTIFY",fill="#ae4aff",font=("Consolas",14))

            canvas.create_text(width-220,630,text=spotify_data["titulo"],fill="#ffffff",font=("Consolas",12),anchor="w")

            canvas.create_text(width-220,650,text=spotify_data["artista"],fill="#ae4aff",font=("Consolas",11),anchor="w")

            if album_img:
                canvas.create_image(width-120,630,image=album_img)

            progresso = spotify_data["progresso"]
            duracao = spotify_data["duracao"]

            if duracao == 0:
                duracao = 1

            barra = (progresso / duracao) * 180

            canvas.create_rectangle(width-300,700,width-120,710,outline="#ae4aff")

            canvas.create_rectangle(
                    width-300,
                    700,
                    width-300 + barra,
                    710,
                    fill="#8c00ff"
            )

            tempo_atual = int(progresso/1000)
            tempo_total = int(duracao/1000)

        m1 = tempo_atual // 60
        s1 = tempo_atual % 60

        m2 = tempo_total // 60
        s2 = tempo_total % 60

        tempo_txt = f"{m1:02}:{s1:02} / {m2:02}:{s2:02}"

        canvas.create_text(
            width-210,
            725,
            text=tempo_txt,
            fill="#ae4aff",
            font=("Consolas",10)
        )

        t=time.strftime("%H:%M:%S")
        canvas.create_text(width-120,height-40,text=t,fill="#ae4aff",font=("Consolas",16))

        canvas.create_text(
            width/2,
            height-80,
            text=f"VOICE: {texto_voz}",
            fill="#ae4aff",
            font=("Consolas",14)
        )

        if estado_voz == "listening":

            pulsar = 10 + abs(math.sin(angle*3))*10

            canvas.create_oval(
                width/2-pulsar,
                height-120-pulsar,
                width/2+pulsar,
                height-120+pulsar,
                outline="#ae4aff",
                width=2
            )

            canvas.create_text(
                width/2,
                height-120,
                text="LISTENING",
                fill="#ae4aff",
                font=("Consolas",12)
            )

        canvas.create_text(width/2,height-40,text="JARVIS READY",fill="#ae4aff",font=("Consolas",16))

        angle+=0.01

        root.after(30,draw)

    draw()
    root.mainloop()