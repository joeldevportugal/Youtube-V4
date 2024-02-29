# importar as librarias ------------------------------------------------------------------------------------------------------------
from tkinter import *
from tkinter.ttk import Combobox, Progressbar, Style
from tkinter import filedialog
from pytube import YouTube
import threading
import time
from tkinter import messagebox
import os
#----------------------------------------------------------------------------------------------------------------------------------
# criar as Funçoes ----------------------------------------------------------------------------------------------------------------
# criar a função Limpar -----------------------------------------------------------------------------------------------------------
def limpar_campos():
    Eurl.delete(0, 'end')  # Limpa o conteúdo da Entry
    formato_var.set(None)  # Desmarca a seleção dos botões de rádio
    cmbMp3.set('Qualidade Mp3')  # Reseta a ComboBox de MP3
    cmbMp4.set('Qualidade Mp4')  # Reseta a ComboBox de MP4
    progress_text['text'] = "0% completo"  # Limpa o texto da barra de progresso
#----------------------------------------------------------------------------------------------------------------------------------
# criar a Função Mostrar Qualidade ------------------------------------------------------------------------------------------------
def mostrar_qualidades():
    url = Eurl.get()
    yt = YouTube(url)

    if formato_var.get() == 'mp3':
        # Qualidades MP3
        streams_mp3 = yt.streams.filter(only_audio=True)
        qualidades_mp3 = [f"{stream.abr}kbps" for stream in streams_mp3 if stream.abr is not None]
        cmbMp3['values'] = qualidades_mp3
        cmbMp4.set('Qualidade Mp4')  # Limpa o valor selecionado na ComboBox de MP4
        cmbMp4.set('')
    elif formato_var.get() == 'mp4':
        # Qualidades MP4
        streams_mp4 = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        qualidades_mp4 = [stream.resolution for stream in streams_mp4]
        cmbMp4['values'] = qualidades_mp4
        cmbMp3.set('Qualidade Mp3')  # Limpa o valor selecionado na ComboBox de MP3
        cmbMp3.set('')
#------------------------------------------------------------------------------------------------------------------------------------
# inicar o download -----------------------------------------------------------------------------------------------------------------
def iniciar_download():
    url = Eurl.get()
    formato = formato_var.get()
    if not url:
        messagebox.showerror("Erro", "Por favor, insira uma URL válida.")
        return
    if formato == 'mp3':
        download_thread = threading.Thread(target=download_mp3, args=(url,))
    elif formato == 'mp4':
        download_thread = threading.Thread(target=download_mp4, args=(url,))
    download_thread.start()
#------------------------------------------------------------------------------------------------------------------------------------
# Defenir O formato Mp3 ou Mp4 ------------------------------------------------------------------------------------------------------
def download_mp3(url, qualidade):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True, abr=qualidade.replace('kbps', '')).first()
    if stream:
        filepath = filedialog.asksaveasfilename(defaultextension=".mp3")  # Pede ao usuário o local de salvamento
        if filepath:
            stream.download(output_path=os.path.dirname(filepath), filename=os.path.basename(filepath))
            update_progress_bar()
def download_mp4(url):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True).first()
    if stream:
        filepath = filedialog.asksaveasfilename(defaultextension=".mp4")  # Pede ao usuário o local de salvamento
        if filepath:
            stream.download(output_path=os.path.dirname(filepath), filename=os.path.basename(filepath))
            update_progress_bar()
#-------------------------------------------------------------------------------------------------------------------------------------
# função progresso Bar ---------------------------------------------------------------------------------------------------------------
def update_progress_bar():
    for i in range(101):
        time.sleep(0.05)  # Atraso para simular o progresso do download
        Pavanco['value'] = i
        progress_text['text'] = f"{i}% completo"
        if i <= 50:
            Pavanco['style'] = "green.Horizontal.TProgressbar"
        else:
            Pavanco['style'] = "Blue.Horizontal.TProgressbar"
        Pavanco.update()
    messagebox.showinfo("Sucesso", "Download efetuado com sucesso!") 
#-------------------------------------------------------------------------------------------------------------------------------------
# criar a função fechar aplicação ----------------------------------------------------------------------------------------------------
def Fechar():
  resposta = messagebox.askyesno("Sair", "Deseja sair do programa? Sim/não")
  if resposta:
    janela.destroy() 
#-------------------------------------------------------------------------------------------------------------------------------------    
#-------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------
# Definir cores a usar ------------------------
co0 = '#FFFFFF'  # cor Braco para o rd
co1 = '#EEFAFC'  # cor fundo entry 
co2 = '#e9fdf0' # cor botões 
co3 = '#0000ff' # cor para Janela
# ------------------------------------------------------------------------------------------------------------------------------------
# Configurar a Janela ----------------------------------------------------------------------------------------------------------------
janela = Tk()
janela.geometry('800x220+100+100')
janela.title('Download  V4 Dev Joel 2024 Portugal ©')
janela.iconbitmap('C:\\Users\\HP\\Desktop\\Projectos\\Download V4\\icon.ico')
janela.resizable(0, 0)
janela.config(bg=co3)
# ------------------------------------------------------------------------------------------------------------------------------------
# Criar o frontend -------------------------------------------------------------------------------------------------------------------
# Criar a Entry ----------------------------------------------------------------------------------------------------------------------
Eurl = Entry(janela, width=85, font=('arial 12'), bg=co1)
Eurl.place(x=10, y=10)
# ------------------------------------------------------------------------------------------------------------------------------------
# Variável de controle para os Radiobuttons
formato_var = StringVar()
formato_var.set(None)  # Nenhum botão selecionado inicialmente

# Criar Rdmp3 e mp4 ------------------------------------------------------------------------------------------
rdmp3 = Radiobutton(janela, text=' formato mp3', font=('arial 12 bold'), bg=co3, fg=co0,variable=formato_var, value='mp3')
rdmp3.place(x=10, y=40)
rdmp4 = Radiobutton(janela, text=' formato mp4', font=('arial 12 bold'), bg=co3, fg=co0,variable=formato_var, value='mp4')
rdmp4.place(x=240, y=40)
# -------------------------------------------------------------------------------------------------------------
# Criar a cmb mp3 e mp4 ---------------------------------------------------------------------------------------
cmbMp3 = Combobox(janela, font=('arial 12'))
cmbMp3.place(x=10, y=80)
cmbMp3.set('Qualidade Mp3')
cmbMp4 = Combobox(janela, font=('arial 12'))
cmbMp4.place(x=240, y=80)
cmbMp4.set('Qualidade Mp4')
# -------------------------------------------------------------------------------------------------------------
# Criar Botões -----------------------------------------------------------------------------------------------
Bdown = Button(janela, text='Download', font=('arial 12'), bg=co2,relief=RAISED, overrelief=RIDGE, command=iniciar_download)
Bdown.place(x=10, y=120)
BLimpar = Button(janela, text='Limpar dados', font=('arial 12'), bg=co2,relief=RAISED, overrelief=RIDGE, command=limpar_campos)
BLimpar.place(x=100, y=120)
BMostrar = Button(janela, text='Mostrar', font=('arial 12'), bg=co2,relief=RAISED, overrelief=RIDGE, command=mostrar_qualidades)
BMostrar.place(x=215, y=120)
BFechar = Button(janela, text='Fechar Aplicação', font=('arial 12'), bg=co2,relief=RAISED, overrelief=RIDGE, command=Fechar)
BFechar.place(x=285, y=120)
# -------------------------------------------------------------------------------------------------------------
# Criar uma barra de progresso -------------------------------------------------------------------------------
style = Style()
style.theme_use('default')
style.configure("orange.Horizontal.TProgressbar", background='Orange')
Pavanco = Progressbar(janela, length=760, style="green.Horizontal.TProgressbar")
Pavanco.place(x=10, y=170)
# Cria um label para o texto e o posiciona sobre a barra de progresso
progress_text = Label(janela, text="0% completo", bg="lightgreen", font=('arial 12'), fg='blue')
progress_text.place(x=10, y=170, width=760, height=23)
# -------------------------------------------------------------------------------------------------------------
# iniciar a Janela --------------------------------------------------------------------------------------------
janela.mainloop()
#--------------------------------------------------------------------------------------------------------------