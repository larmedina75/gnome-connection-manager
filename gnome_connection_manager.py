#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Python modle simple_connection_manager.py
# 
# Simple Connection Manager by Luis Armando Medina Avitia (lamedina@gmail.com)
#
# based on Gnome Connection Manager by Renzo Bertuzzi (kuthulu@gmail.com) - CHILE
# Last change: 20191119
#
#
#TODO
# - ayuda
# - drag'n drop hosts entre grupos
# - sftp
# - master password (al iniciar la aplicacion)
# - guardar estado de consolas abiertas (y estado de split)
# - revisar buscador, a veces no encuentra las palabras
# - sortcut para moverse entre notebooks
# - quitar los "accelerator" del archivo .glade (o dejarlos opcionales)
# - soporte picocom (o minicom, o pyserial, ser2net) para comunicación serial
# - Permitir modificar combinacion para cerrar aplicacion CTRL+Q
# - Icono en system tray
# - Quitar shortcut ALT+F para archivo 
# - Permitir deshabilitar shortcuts
# - soporte proxy socks/http para ssh
# - cluster mode: would be nice to have a drop-down list on the cluster button and once selected \"the text to send to hosts box\" should be activated on the right of the cluster button. The box should stay on the toolbar and not over the terminal window
# - hide chars** in cluster mode (un checkbox para mostrar/ocultar entrada)
# - seleccionar varios hosts y conectarse
# - seleccionar varios hosts y editarlos
# - permitir establecer colores a nivel de grupos
# - permitir cambiar nombre de grupo
# - overwrite colors (like putty)
# - Cambiar charset en consola o en propiedades del host
# - One "nice to have" would be the ability for GCM to use my existing PuTTY sessions instead of entering everything a second time. External script for that that parses ~/putty/session files
# - Enter passwords in commands and hide them, #P=password (Angelo Corsaro). TextView doesnt support masking text, it needs a different implementation. Pending.
# - Persist history of cluster commands. is it really necessary?
# - Option to disable shortcuts
#
#Changelog:
# v1.3.1 - 
# v1.3.0 - Python 3 code rewrite, fix bugs and fist run.
#        - gi class names rewrite to translate from python2 to python3
#
# v1.1.0 - Bugfix: public key field was not saved (thanks to Benoît Georgelin for reporting the bug)
#        - Bugfix: bug in AES library resulted in blank passwords randomly being replaced by some characters (thanks to Boyan Peychev for reporting the bug)
#        - Bugfix: drag and release tab on the same notebook caused tab to be closed
#        - Bugfix: Estado de nodos expandidos/contraidos se revertia a un estado anterior al editar por segunda vez un host
#        - Bugfix: Cluster window had to be resized to show the text area in some setups
#        - Bugfix: Blank lines in commands were removed when restarting application (thanks to Nicholas O'Neill for reporting the bug)
#        - Se agrega traducción a koreano (thanks to Jong Hoon Lee)
#        - Better indentation in server panel
#        - Disabled the horizontal scroll bar in the console        
#        - Added option to open local console on application startup (thanks to Boaman Surebun for the implementation)
#        - Se agrega opción para copiar todo el buffer al porta-papeles
#        - Se usa la consola por defecto del usuario en vez de bash
#        - Se exponen algunos shortcuts
#        - Added menu with servers list
#
# v1.0.0 - Bugfix: last group was collapsed when adding/editing a new host. All collapsed nodes are preserved now. (thanks to Kevin Brennan for reporting the bug)
#        - Bugfix: importing servers in another computer cleared all the passwords. (thanks to Simon Pitt for reporting the bug)
#        - Bugfix: buttons to choose colors did not reflect the selected color (thanks to Sverre Rakkenes for reporting the bug)
#        - Se implementa AES-256 para encriptar claves
#        - Se agrega opcion para pasar parametros adicionales a la linea de comando (ssh/telnet)
#        - Se agrega opcion para auto cerrar tab (nunca, siempre, solo si no hay errores) cuando se finaliza la sesion
#        - Se agrega menu con opcion para ocultar toolbar y panel de servidores
#        - Se agrega soporte para compression ssh (gracias a Boaman Surebun por la implementacion)
#        - Se agrega configuracion en host para sequencia de teclas Backspace y Delete
#
# v0.9.8 - Bugfix: find_back shortcut was not working
#        - Bugfix: double click on tabs or arrows in the tab bar opened a new local window
#        - Se quita F10 como atajo para el menu
#        - Se agrega texto de licencia en acerca de
#        - Historial de comandos en cluster
#        - Se agrega descripcion y tooltips sobre hosts
#        - delay entre los comandos que se envian al inicio (por cada linea, usar una linea tipo comentario con el delay??)
#        - Se agrega redireccionamiento dynamico de puertos
#
# v0.9.7 - Bugfix: error message "Error connecting to server: global name 'bolor' is not defined" when opening a host with custom colors (thanks to talos)
#
# v0.9.6 - Bugfix: error al duplicar un host en un subgrupo
#        - Se agrega opcion para generar log de las sesiones
#        - Si no existe el idioma, ingles por defecto
#        - Se agrega opcion para habilitar Agent-forwarding
#        - Se agrega soporte para private key files
#
# v0.9.5 - Se elimina mensaje "The package is of bad quality" al instalar en ubuntu 11.04 (lintian check)
#        - Bugfix: el modo cluster no muestra los titulos correctos de las consolas cuando han sido renombradas
#        - Se agrega opción de clonar consola
#        - Archivo de configuración ahora se guarda al realizar cambios (antes se guardaba al salir de la aplicacion)
#        - Se agrega opción de tener subgrupos, al editar un host se debe usar el formato grupo/subgrupo/subgrupo para el nombre de grupo
#
# v0.9.4 - Bugfix: Dejar el foco siempre en la nueva consola
#        - Bugfix: Shortcut para console_previous se revertia a ctrl+shift+left 
#        - Se agrega traducción a italiano (gracias a Vincenzo Reale)
#        - Bugfix: Telnet no funcionaba al usarlo sin usuario
#
# v0.9.3 - Bugfix: No funcionaba el boton "Local" luego de cerrar todas las consolas
#        - Bugfix: se quita atajo CTRL+QUIT para salir de la aplicacion.
#        - Se agrega traducción a ruso (gracias a Denis Fokin)
#        - Se agrega traducción a portugues (gracias a Ericson Alexandre S.)
#        - Se agrega menu contextual "copiar y pegar"
#        - Se agrega shortcut para reconectar 
#        - Revisar si expect esta instalado al iniciar
#        - Permitir conexiones locales al guardar un host (ssh, telnet, local)
#
# v0.9.2 - Bugfix: En algunos casos no se guardaban los passwords
#        - Bugfix: Al conectarse a traves de una sesion remota (nomachine, X11) y abrir gcm se limpiaban los passwords
#        - Se agrega traducción a polaco (gracias a Pawel)
#
# v0.9.1 - Bugfix: Se corrigen algunos textos en frances
#        - Bugfix: Se corrige bug al importar servidores
#        - Bugfix: opcion de reconectar desaparece para las demás consolas luego de reconectar a una consola
#        - Se agrega opcion de cerrar consola con boton central del mouse sin pedir confirmacion
#
# v0.9.0 - Se agrega opcion de copiar texto seleccionado automaticamente al porta papeles
#        - Se agrega menu para duplicar host
#        - Se agrega modo cluster (permite enviar mismo comando a varios hosts a la vez)
#        - Se agrega menu para reabrir una sesion cerrada
#        - menu contextual en consola para enviar los comandos predefinidos
#
# v0.8.0 - Bugfix: ancho/alto incorrecto al dividir consola horizontal/vertical
#        - Se agrega opcion para conservar tamaño de ventana entre ejecuciones
#        - Se agrega opcion para resetear y resetear-limpiar consola (menu contextual y shortcut)
#        - Soporte para autenticacion sin password/public key(se debe dejar el password en blanco)
#        - X11 forwading para ssh
#        - cambiar font de consola
#        - Permitir ocultar boton para donar
#
# v0.7.1 - Bugfix: al cerrar consola con shortcut se mantenia abierta la sesion ssh
#        - Bugfix: importar servers arrojaba mensaje "Archivo invalido"
#
# v0.7.0 - Se agrega menu contextual "copiar direccion" del host
#        - Se agrega opcion de keep-alive por host
#        - Se agrega colores configurables por host
#        - Se agrega opción de renombrar tabs de consola
#        - Se agrega traducción a francés (gracias a William M.)
#        - Se agrega shortcut para cerrar consola
#
# v0.6.1 - Se agrega shortcuts para cambiar entre consolas (izq, der, y 01 a 09)
#        - Correción de bug: no se podia editar un shortcut predefinido
#
# v0.6.0 - Se agrega opción para guardar buffer en archivo
#        - Se agrega buscador
#        - Boton para abrir consola local
#        - ejecutar comando luego del login
#        - guardar estado (abiertos/cerrados) de folders y posicion del panel
#        - importar/exportar lista de servidores
#        - menu contextual en grupos y servidores (expandir/contraer todo, editar host, agregar host)
#        - shortcuts para comandos predefinidos (copia, pegar, etc) y para ejecutar comandos
#        - comprobar actualizaciones
#        - Corrección de bug: autologin no funcionaba para algunos servidores telnet
#
# v0.5.0 - Corrección de bug que mostraba mal las consolas ssh en algunos casos (no se ocupaba todo el espacio de la consola)
#        - Corrección de bug que cerraba dos consolas al tener la pantalla dividida y cerrar consola de la derecha
#        - Se agrega opción de menu contextual con boton derecho
#        - Se agrega opción de confirmar al cerrar una consola
#        - Se muestra mensaje en pantalla cuando cambia la key de un host para ssh
#        - Boton donar

from __future__ import with_statement
import os
import operator
import sys
import base64
import time
import tempfile
import shlex
import traceback

#try:
#    import gtk
#    import GObject
#except:
#    #print >> sys.stderr, "pygtk required"
#    print("pygtk required", file=sys.stderr)
#    sys.exit(1)

#import gtk
#import GObject
  
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk
from gi.repository import Vte, GLib, Gio, Gdk, GdkPixbuf
from gi.repository import GObject

#try:
#    import Vte
#except:
#    error = Gtk.MessageDialog (None, Gtk.DIALOG_MODAL, Gtk.MESSAGE_ERROR, Gtk.BUTTONS_OK,
#      'You must install libVte for python')
#    error.run()
#    sys.exit (1)

#Ver si expect esta instalado
try:
    e = os.system("expect >/dev/null 2>&1 -v")
except:
    e = -1
if e != 0:
    error = Gtk.MessageDialog (parent=None, flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, text='You must install expect')
    error.run()
    sys.exit (1)

#Gtk.gdk.threads_init()
Gdk.threads_init()

from SimpleGladeApp import SimpleGladeApp
from SimpleGladeApp import bindtextdomain

import configparser
from gi.repository import Pango as pango
#import pango
import pyAES

app_name = "Gnome Connection Manager"
app_version = "1.3.0"
app_web = "http://www.kuthulu.com/gcm"
app_fileversion = "1"

BASE_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))

SSH_BIN = 'ssh'
TEL_BIN = 'telnet'
SHELL   = os.environ["SHELL"]

SSH_COMMAND = BASE_PATH + "/ssh.expect"
CONFIG_FILE = os.getenv("HOME") + "/.gcm/gcm.conf"
KEY_FILE = os.getenv("HOME") + "/.gcm/.gcm.key"

if not os.path.exists(os.getenv("HOME") + "/.gcm"):
    os.makedirs(os.getenv("HOME") + "/.gcm")

domain_name="gcm-lang"

HSPLIT = 0
VSPLIT = 1

_COPY              = ["copy"]
_PASTE             = ["paste"]
_COPY_ALL          = ["copy_all"]
_SAVE              = ["save"]
_FIND              = ["find"]
_CLEAR             = ["reset"]
_FIND_NEXT         = ["find_next"]
_FIND_BACK         = ["find_back"]
_CONSOLE_PREV      = ["console_previous"]
_CONSOLE_NEXT      = ["console_next"]
_CONSOLE_1         = ["console_1"]
_CONSOLE_2         = ["console_2"]
_CONSOLE_3         = ["console_3"]
_CONSOLE_4         = ["console_4"]
_CONSOLE_5         = ["console_5"]
_CONSOLE_6         = ["console_6"]
_CONSOLE_7         = ["console_7"]
_CONSOLE_8         = ["console_8"]
_CONSOLE_9         = ["console_9"]
_CONSOLE_CLOSE     = ["console_close"]
_CONSOLE_RECONNECT = ["console_reconnect"]
_CONNECT           = ["connect"]

ICON_PATH = BASE_PATH + "/icon.png"

glade_dir = ""
locale_dir = BASE_PATH + "/lang"

bindtextdomain(domain_name, locale_dir)

groups={}
shortcuts={}

enc_passwd=''

#Variables de configuracion
class conf():
    WORD_SEPARATORS="-A-Za-z0-9,./?%&#:_=+@~"
    BUFFER_LINES=2000
    STARTUP_LOCAL=True
    CONFIRM_ON_EXIT=True
    FONT_COLOR = ""
    BACK_COLOR = ""
    TRANSPARENCY = 0
    PASTE_ON_RIGHT_CLICK = 1
    CONFIRM_ON_CLOSE_TAB = 0
    AUTO_CLOSE_TAB = 0
    COLLAPSED_FOLDERS = ""
    LEFT_PANEL_WIDTH = 100
    CHECK_UPDATES=True
    WINDOW_WIDTH = -1
    WINDOW_HEIGHT = -1
    FONT = ""
    HIDE_DONATE = False
    AUTO_COPY_SELECTION = 0
    LOG_PATH = os.path.expanduser("~")
    SHOW_TOOLBAR = True
    SHOW_PANEL = True
    VERSION = 0

def msgbox(text, parent=None):
    msgBox = Gtk.MessageDialog(parent=parent, 
                               flags=Gtk.DialogFlags.MODAL, 
                               message_type=Gtk.MessageType.ERROR, 
                               buttons=Gtk.ButtonsType.OK, 
                               text=text+"dddd")
    msgBox.set_icon_from_file(ICON_PATH)
    msgBox.run()    
    msgBox.destroy()

def msgconfirm(text):
    msgBox = Gtk.MessageDialog(parent=None, 
                               flags=Gtk.DialogFlags.MODAL, 
                               message_type=Gtk.MessageType.QUESTION, 
                               buttons=Gtk.ButtonsType.OK_CANCEL, 
                               text=text)
    msgBox.set_icon_from_file(ICON_PATH)
    response = msgBox.run()    
    msgBox.destroy()
    return response


def inputbox(title, text, default='', password=False):
    msgBox = EntryDialog(title, text, default, mask=password)
    msgBox.set_icon_from_file(ICON_PATH)
    if msgBox.run() == Gtk.RESPONSE_OK:
        response = msgBox.value
    else:
        response = None
    msgBox.destroy()
    return response

def show_font_dialog(parent, title, button):
    if not hasattr(parent, 'dlgFont'):
        parent.dlgFont = None
        
    if parent.dlgFont == None:
        parent.dlgFont = Gtk.FontSelectionDialog(title)
    fontsel = parent.dlgFont.fontsel
    fontsel.set_font_name(button.selected_font.to_string())    

    response = parent.dlgFont.run()

    if response == Gtk.RESPONSE_OK:        
        button.selected_font = pango.FontDescription(fontsel.get_font_name())        
        button.set_label(button.selected_font.to_string())
        button.get_child().modify_font(button.selected_font)
    parent.dlgFont.hide()
    
def show_open_dialog(parent, title, action):        
    dlg = Gtk.FileChooserDialog(title=title, parent=parent, action=action)
    dlg.add_button(Gtk.STOCK_CANCEL, Gtk.RESPONSE_CANCEL)
    
    dlg.add_button(Gtk.STOCK_SAVE if action==Gtk.FILE_CHOOSER_ACTION_SAVE else Gtk.STOCK_OPEN, Gtk.RESPONSE_OK)        
    dlg.set_do_overwrite_confirmation(True)        
    if not hasattr(parent,'lastPath'):
        parent.lastPath = os.path.expanduser("~")
    dlg.set_current_folder( parent.lastPath )
    
    if dlg.run() == Gtk.RESPONSE_OK:
        filename = dlg.get_filename()
        parent.lastPath = os.path.dirname(filename)
    else:
        filename = None
    dlg.destroy()
    return filename
            
def get_key_name(event):
    name = ""
    if event.state & 4:
        name = name + "CTRL+"
    if event.state & 1:
        name = name + "SHIFT+"
    if event.state & 8:
        name = name + "ALT+"
    if event.state & 67108864:
        name = name + "SUPER+"
    return name + Gtk.gdk.keyval_name(event.keyval).upper()
     
def get_username():
    return os.getenv('USER') or os.getenv('LOGNAME') or os.getenv('USERNAME')

def get_password():
    return get_username() + enc_passwd
    
def load_encryption_key():
    global enc_passwd
    try:
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE) as f:
                enc_passwd = f.read()
        else:
            enc_passwd = ''
    except:
        msgbox("Error trying to open key_file")
        enc_passwd = ''

def initialise_encyption_key():
    global enc_passwd
    import random
    x = int(str(random.random())[2:])
    y = int(str(random.random())[2:])
    enc_passwd = "%x" % (x*y)
    try:
        with os.fdopen(os.open(KEY_FILE, os.O_WRONLY | os.O_CREAT, 0o600), 'w') as f:
            f.write(enc_passwd)
    except:
        msgbox("Error initialising key_file")

## funciones para encryptar passwords - no son muy seguras, pero impiden que los pass se guarden en texto plano
def xor(pw, str1):
    c = 0
    liste = []
    for k in xrange(len(str1)):
        if c > len(pw)-1:
            c = 0
        fi = ord(pw[c])
        c += 1
        se = ord(str1[k])
        fin = operator.xor(fi, se)
        liste += [chr(fin)]
    return liste
        
def encrypt_old(passw, string):
    try:
        ret = xor(passw, string)    
        s = base64.b64encode("".join(ret))
    except:
        s = ""
    return s
 
def decrypt_old(passw, string):
    try:
        ret = xor(passw, base64.b64decode(string))
        s = "".join(ret)
    except:
        s = ""
    return s
    
def encrypt(passw, string):
    try:
        s = pyAES.encrypt(string, passw)
    except:
        s = ""
    return s
 
def decrypt(passw, string):
    try:
        s = decrypt_old(passw, string) if conf.VERSION == 0 else pyAES.decrypt(string, passw)
    except:
        s = ""
    return s

class Wmain(SimpleGladeApp):

    def __init__(self, path="gnome-connection-manager.glade",
                 root="wMain",
                 domain=domain_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

        global wMain
        wMain = self                
        
        load_encryption_key()
        
        self.initLeftPane()     
        
        self.createMenu()
        
        if conf.VERSION == 0:
            initialise_encyption_key()
        
        settings = Gtk.Settings.get_default()
        settings.props.gtk_menu_bar_accel = None

        self.real_transparency = False
        if conf.TRANSPARENCY>0:
            #Revisar si hay soporte para transparencia
            screen = self.get_widget("wMain").get_screen()
            colormap = screen.get_rgba_colormap()
            if colormap != None and screen.is_composited():
                self.get_widget("wMain").set_colormap(colormap)
                self.real_transparency = True
        
        if conf.WINDOW_WIDTH != -1 and conf.WINDOW_HEIGHT != -1:
            self.get_widget("wMain").resize(conf.WINDOW_WIDTH, conf.WINDOW_HEIGHT)
        else:
            self.get_widget("wMain").maximize()        
        self.get_widget("wMain").show()
        #Just added children in glade to eliminate GTK warning, remove all children
        for x in self.nbConsole.get_children():
            self.nbConsole.remove(x)
        self.nbConsole.set_scrollable(True)
        self.nbConsole.set_group_name('default')
        self.nbConsole.connect('page_removed', self.on_page_removed)        
        self.nbConsole.connect("page-added", self.on_page_added)                                        
        
                
        self.hpMain.previous_position = 150
        
        #if conf.LEFT_PANEL_WIDTH!=0:
        #    self.set_panel_visible(conf.SHOW_PANEL)
        #self.set_toolbar_visible(conf.SHOW_TOOLBAR)
        
        #a veces no se posiciona correctamente con 400 ms, asi que se repite el llamado 
        GObject.timeout_add(400, lambda : self.hpMain.set_position(conf.LEFT_PANEL_WIDTH))
        GObject.timeout_add(900, lambda : self.hpMain.set_position(conf.LEFT_PANEL_WIDTH))

        if conf.HIDE_DONATE:
            self.get_widget("btnDonate").hide_all()
        
        if conf.CHECK_UPDATES:
            GObject.timeout_add(2000, lambda: self.check_updates())
        
        #Por cada parametro de la linea de comandos buscar el host y agregar un tab
        for arg in sys.argv[1:]:
            i = arg.rfind("/")
            if i!=-1:
                group = arg[:i]
                name = arg[i+1:]                 
                if group!='' and name!='' and groups.has_key(group):
                    for h in groups[group]:                                
                        if h.name==name:
                            self.addTab(self.nbConsole, h)
                            break                
        
        self.get_widget('txtSearch').modify_text(Gtk.StateType.NORMAL, Gdk.Color(0.66, 0.66, 0.66)) # 'darkgray

        
        if conf.STARTUP_LOCAL:
            self.addTab(self.nbConsole,'local')

        
    #-- Wmain.new {
    def new(self):        
        self.hpMain = self.get_widget("hpMain")
        self.nbConsole = self.get_widget("nbConsole")
        self.treeServers = self.get_widget("treeServers")
        self.menuServers = self.get_widget("menuServers")
        #self.menuCustomCommands = self.get_widget("menuCustomCommands")
        self.current = None
        self.count = 0        
    #-- Wmain.new }glade

    #-- Wmain custom methods {           
    #   Write your own methods here
        
    def check_updates(self):
        checker = CheckUpdates(self)        
        checker.start()
            
    def on_terminal_click(self, widget, event, *args):      
        if event.type == Gtk.gdk.BUTTON_PRESS and event.button == 3:
            if conf.PASTE_ON_RIGHT_CLICK:
                widget.paste_clipboard()
            else:
                self.popupMenu.mnuCopy.set_sensitive(widget.get_has_selection()) 
                self.popupMenu.mnuLog.set_active( hasattr(widget, "log_handler_id") and widget.log_handler_id != 0 )
                self.popupMenu.terminal = widget
                self.popupMenu.popup( None, None, None, event.button, event.time)
            return True
    
    def on_terminal_keypress(self, widget, event, *args):
        if shortcuts.has_key    (get_key_name(event)):
            cmd = shortcuts[get_key_name(event)]
            if type(cmd) == list:
                #comandos predefinidos
                if cmd == _COPY:
                    self.terminal_copy(widget)
                elif cmd == _PASTE:
                    self.terminal_paste(widget)
                elif cmd == _COPY_ALL:
                    self.terminal_copy_all(widget)
                elif cmd == _SAVE:
                    self.show_save_buffer(widget)
                elif cmd == _FIND:
                    self.get_widget('txtSearch').select_region(0, -1)
                    self.get_widget('txtSearch').grab_focus()
                elif cmd == _FIND_NEXT:
                    if hasattr(self, 'search'):
                        self.find_word()
                elif cmd == _CLEAR:
                   widget.reset(True, True)
                elif cmd == _FIND_BACK:
                    if hasattr(self, 'search'):
                        self.find_word(backwards=True)
                elif cmd == _CONSOLE_PREV:
                    widget.get_parent().get_parent().prev_page()
                elif cmd == _CONSOLE_NEXT:
                    widget.get_parent().get_parent().next_page()
                elif cmd == _CONSOLE_CLOSE:
                    wid = widget.get_parent()                    
                    page = widget.get_parent().get_parent().page_num(wid)                    
                    if page != -1:
                        widget.get_parent().get_parent().remove_page(page)
                        wid.destroy()
                elif cmd == _CONSOLE_RECONNECT:                    
                    if not hasattr(widget, "command"):
                        widget.fork_command(SHELL)
                    else:
                        widget.fork_command(widget.command[0], widget.command[1])
                        while Gtk.events_pending():
                            Gtk.main_iteration(False)                                
                            
                        #esperar 2 seg antes de enviar el pass para dar tiempo a que se levante expect y prevenir que se muestre el pass
                        if widget.command[2]!=None and widget.command[2]!='':
                            GObject.timeout_add(2000, self.send_data, widget, widget.command[2])                    
                    widget.get_parent().get_parent().get_tab_label(widget.get_parent()).mark_tab_as_active()
                    return True
                elif cmd == _CONNECT:
                    self.on_btnConnect_clicked(None)
                elif cmd[0][0:8] == "console_":
                    page = int(cmd[0][8:]) - 1                   
                    widget.get_parent().get_parent().set_current_page(page)                
            else:
                #comandos del usuario
                widget.feed_child(cmd)
                
            return True
        return False
    
    def on_terminal_selection(self, widget, *args):
        if conf.AUTO_COPY_SELECTION:
            self.terminal_copy(widget)
        return True
        
    def find_word(self, backwards=False):
        pos=-1        
        if backwards:
            lst = range(0, self.search['index'])
            lst.reverse()
            lst.extend(reversed(range(self.search['index'], len(self.search['lines']))))
        else:
            lst = range(self.search['index'], len(self.search['lines']))
            lst.extend(range(0, self.search['index']))
        for i in lst:
            pos = self.search['lines'][i].find(self.search['word'])
            if pos != -1:                
                self.search['index'] = i if backwards else i + 1
                #print 'found at line %d column %d, index=%d' % (i, pos, self.search['index'])
                GObject.timeout_add(0, lambda: self.search['terminal'].get_adjustment().set_value(i))
                self.search['terminal'].queue_draw()
                break
        if pos==-1:
            self.search['index'] = len(self.search['lines']) if backwards else 0
    
    
    def init_search(self):        
        if hasattr(self, 'search') and self.get_widget('txtSearch').get_text() == self.search['word'] and self.current == self.search['terminal']:                        
            return  True
            
        terminal = self.find_active_terminal(self.hpMain)
        if terminal == None:
            terminal = self.current
        else:
            self.current = terminal
        if terminal==None:            
            return False
            
        self.search = {}
        self.search['lines'] = terminal.get_text_range(0, 0, terminal.get_property('scrollback-lines'), terminal.get_column_count(), lambda *args: True, None, None ).rstrip().splitlines()
        self.search['index'] = len(self.search['lines'])
        self.search['terminal'] = terminal
        self.search['word'] = self.get_widget('txtSearch').get_text()
        return True
    
    def on_popupmenu(self, widget, item, *args):        
        if item == 'V': #PASTE
            self.terminal_paste(self.popupMenu.terminal)
            return True
        elif item == 'C': #COPY
            self.terminal_copy(self.popupMenu.terminal)
            return True
        elif item == 'CV': #COPY and PASTE
            self.terminal_copy_paste(self.popupMenu.terminal)
            return True            
        elif item == 'A': #SELECT ALL
            self.terminal_select_all(self.popupMenu.terminal)
            return True
        elif item == 'CA': #COPY ALL
            self.terminal_copy_all(self.popupMenu.terminal)
            return True
        elif item == 'X': #CLOSE CONSOLE
            widget = self.popupMenu.terminal.get_parent()
            notebook = widget.get_parent()
            page=notebook.page_num(widget)         
            notebook.remove_page(page)
            return True
        elif item == 'CP': #CUSTOM COMMANDS
            self.popupMenu.terminal.feed_child(args[0])            
        elif item == 'S': #SAVE BUFFER
            self.show_save_buffer(self.popupMenu.terminal)
            return True
        elif item == 'H': #COPY HOST ADDRESS TO CLIPBOARD
            if self.treeServers.get_selection().get_selected()[1]!=None and not self.treeModel.iter_has_child(self.treeServers.get_selection().get_selected()[1]):
                host = self.treeModel.get_value(self.treeServers.get_selection().get_selected()[1],1)                
                cb = Gtk.Clipboard()
                cb.set_text(host.host)
                cb.store()
            return True
        elif item == 'D': #DUPLICATE HOST
            if self.treeServers.get_selection().get_selected()[1]!=None and not self.treeModel.iter_has_child(self.treeServers.get_selection().get_selected()[1]):                
                selected = self.treeServers.get_selection().get_selected()[1]            
                group = self.get_group(selected)
                host = self.treeModel.get_value(selected, 1)
                newname = '%s (copy)' % (host.name)
                newhost = host.clone()
                for h in groups[group]:
                    if h.name == newname:
                        newname = '%s (copy)' % (newname)
                newhost.name = newname
                groups[group].append( newhost )
                self.updateTree()
                self.writeConfig()
            return True            
        elif item == 'R': #RENAME TAB
            text = inputbox(_('Renombrar consola'), _('Ingrese nuevo nombre'), self.popupMenuTab.label.get_text().strip())
            if text != None and text != '':
                self.popupMenuTab.label.set_text("  %s  " % (text))            
            return True
        elif item == 'RS' or item == 'RS2': #RESET CONSOLE              
            if (item == 'RS'):
                tab = self.popupMenuTab.label.get_parent().get_parent()
                term = tab.widget.get_child()
            else:
                term = self.popupMenu.terminal
            term.reset(True, False)
            return True
        elif item == 'RC' or item == 'RC2': #RESET AND CLEAR CONSOLE
            if (item == 'RC'):
                tab = self.popupMenuTab.label.get_parent().get_parent()
                term = tab.widget.get_child()
            else:
                term = self.popupMenu.terminal
            term.reset(True, True)
            return True
        elif item == 'RO': #REOPEN SESION
            tab = self.popupMenuTab.label.get_parent().get_parent()
            term = tab.widget.get_child()
            if not hasattr(term, "command"):
                term.fork_command(SHELL)
            else:
                term.fork_command(term.command[0], term.command[1])
                while Gtk.events_pending():
                    Gtk.main_iteration(False)                                
                    
                #esperar 2 seg antes de enviar el pass para dar tiempo a que se levante expect y prevenir que se muestre el pass
                if term.command[2]!=None and term.command[2]!='':
                    GObject.timeout_add(2000, self.send_data, term, term.command[2])
            tab.mark_tab_as_active()
            return True
        elif item == 'CC' or item == 'CC2': #CLONE CONSOLE
            if item == 'CC':
                tab = self.popupMenuTab.label.get_parent().get_parent()
                term = tab.widget.get_child()
                ntbk = tab.get_parent()
            else:
                term = self.popupMenu.terminal
                ntbk = term.get_parent().get_parent() 
                tab = ntbk.get_tab_label(term.get_parent())               
            if not hasattr(term, "host"):
                self.addTab(ntbk, tab.get_text())
            else:
                host = term.host.clone()
                host.name = tab.get_text()
                host.log = hasattr(term, "log_handler_id") and term.log_handler_id != 0
                self.addTab(ntbk, host)
            return True
        elif item == 'L' or item == 'L2': #ENABLE/DISABLE LOG
            if item == 'L':
                tab = self.popupMenuTab.label.get_parent().get_parent()
                term = tab.widget.get_child()
            else:
                term = self.popupMenu.terminal
            if not self.set_terminal_logger(term, widget.get_active()):
                widget.set_active(False)
            return True
                
    def createMenu(self):
        self.popupMenu = Gtk.Menu()
        self.popupMenu.mnuCopy = menuItem = Gtk.ImageMenuItem(_("Copiar"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_COPY, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_COPY, Gtk.IconSize.MENU))
        self.popupMenu.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'C')
        menuItem.show()
        
        self.popupMenu.mnuPaste = menuItem = Gtk.ImageMenuItem(_("Pegar"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_PASTE, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_PASTE, Gtk.IconSize.MENU))
        self.popupMenu.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'V')
        menuItem.show()
        
        self.popupMenu.mnuCopyPaste = menuItem = Gtk.ImageMenuItem(_("Copiar y Pegar"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_INDEX, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_INDEX, Gtk.IconSize.MENU))
        self.popupMenu.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'CV')
        menuItem.show()
        
        self.popupMenu.mnuSelect = menuItem = Gtk.ImageMenuItem(_("Seleccionar todo"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_SELECT_ALL, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_SELECT_ALL, Gtk.IconSize.MENU))
        self.popupMenu.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'A')
        menuItem.show()
        
        self.popupMenu.mnuCopyAll = menuItem = Gtk.ImageMenuItem(_("Copiar todo"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_SELECT_ALL, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_SELECT_ALL, Gtk.IconSize.MENU))
        self.popupMenu.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'CA')
        menuItem.show()
        
        self.popupMenu.mnuSelect = menuItem = Gtk.ImageMenuItem(_("Guardar buffer en archivo"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_SAVE, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_SAVE, Gtk.IconSize.MENU))
        self.popupMenu.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'S')
        menuItem.show()
        
        menuItem = Gtk.MenuItem()
        self.popupMenu.append(menuItem)
        menuItem.show()
        
        self.popupMenu.mnuReset = menuItem = Gtk.ImageMenuItem(_("Reiniciar consola"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_NEW, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_NEW, Gtk.IconSize.MENU))
        self.popupMenu.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'RS2')
        menuItem.show()
        
        self.popupMenu.mnuClear = menuItem = Gtk.ImageMenuItem(_("Reiniciar y Limpiar consola"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_CLEAR, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_CLEAR, Gtk.IconSize.MENU))
        self.popupMenu.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'RC2')
        menuItem.show()
        
        self.popupMenu.mnuClone = menuItem = Gtk.ImageMenuItem(_("Clonar consola"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_COPY, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_COPY, Gtk.IconSize.MENU))
        self.popupMenu.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'CC2')
        menuItem.show()

        self.popupMenu.mnuLog = menuItem = Gtk.CheckMenuItem(_("Habilitar log"))
        self.popupMenu.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'L2')
        menuItem.show()
        
        self.popupMenu.mnuClose = menuItem = Gtk.ImageMenuItem(_("Cerrar consola"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_CLOSE, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU))
        self.popupMenu.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'X')
        menuItem.show()
        
        menuItem = Gtk.MenuItem()
        self.popupMenu.append(menuItem)
        menuItem.show()
        
        #Menu de comandos personalizados
        self.popupMenu.mnuCommands = Gtk.Menu()
        
        self.popupMenu.mnuCmds = menuItem = Gtk.ImageMenuItem(_("Comandos personalizados"))
        menuItem.set_submenu(self.popupMenu.mnuCommands)
        self.popupMenu.append(menuItem)
        menuItem.show()
        self.populateCommandsMenu()
                
        #Menu contextual para panel de servidores
        self.popupMenuFolder = Gtk.Menu()
        
        self.popupMenuFolder.mnuConnect = menuItem = Gtk.ImageMenuItem(_("Conectar"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_EXECUTE, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_EXECUTE, Gtk.IconSize.MENU))
        self.popupMenuFolder.append(menuItem)
        menuItem.connect("activate", self.on_btnConnect_clicked)
        menuItem.show()

        self.popupMenuFolder.mnuCopyAddress = menuItem = Gtk.ImageMenuItem(_("Copiar Direccion"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_COPY, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_COPY, Gtk.IconSize.MENU))
        self.popupMenuFolder.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'H')
        menuItem.show()
        
        self.popupMenuFolder.mnuAdd = menuItem = Gtk.ImageMenuItem(_("Agregar Host"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_ADD, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_ADD, Gtk.IconSize.MENU))
        self.popupMenuFolder.append(menuItem)
        menuItem.connect("activate", self.on_btnAdd_clicked)
        menuItem.show()
        
        self.popupMenuFolder.mnuEdit = menuItem = Gtk.ImageMenuItem(_("Editar"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_EDIT, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_EDIT, Gtk.IconSize.MENU))
        self.popupMenuFolder.append(menuItem)
        menuItem.connect("activate", self.on_bntEdit_clicked)
        menuItem.show()
        
        self.popupMenuFolder.mnuDel = menuItem = Gtk.ImageMenuItem(_("Eliminar"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_DELETE, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_DELETE, Gtk.IconSize.MENU))
        self.popupMenuFolder.append(menuItem)
        menuItem.connect("activate", self.on_btnDel_clicked)
        menuItem.show()
        
        self.popupMenuFolder.mnuDup = menuItem = Gtk.ImageMenuItem(_("Duplicar Host"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_DND_MULTIPLE, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_DND_MULTIPLE, Gtk.IconSize.MENU))
        self.popupMenuFolder.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'D')
        menuItem.show()
        
        menuItem = Gtk.MenuItem()
        self.popupMenuFolder.append(menuItem)
        menuItem.show()
        
        self.popupMenuFolder.mnuExpand = menuItem = Gtk.ImageMenuItem(_("Expandir todo"))        
        self.popupMenuFolder.append(menuItem)
        menuItem.connect("activate", lambda *args: self.treeServers.expand_all())
        menuItem.show()
        
        self.popupMenuFolder.mnuCollapse = menuItem = Gtk.ImageMenuItem(_("Contraer todo"))
        self.popupMenuFolder.append(menuItem)
        menuItem.connect("activate", lambda *args: self.treeServers.collapse_all())
        menuItem.show()
        
        
        #Menu contextual para tabs
        self.popupMenuTab = Gtk.Menu()
        
        self.popupMenuTab.mnuRename = menuItem = Gtk.ImageMenuItem(_("Renombrar consola"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_EDIT, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_EDIT, Gtk.IconSize.MENU))
        self.popupMenuTab.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'R')
        menuItem.show()
        
        self.popupMenuTab.mnuReset = menuItem = Gtk.ImageMenuItem(_("Reiniciar consola"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_NEW, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_NEW, Gtk.IconSize.MENU))
        self.popupMenuTab.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'RS')
        menuItem.show()
        
        self.popupMenuTab.mnuClear = menuItem = Gtk.ImageMenuItem(_("Reiniciar y Limpiar consola"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_CLEAR, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_CLEAR, Gtk.IconSize.MENU))
        self.popupMenuTab.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'RC')
        menuItem.show()
        
        self.popupMenuTab.mnuReopen = menuItem = Gtk.ImageMenuItem(_("Reconectar al host"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_CONNECT, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_CONNECT, Gtk.IconSize.MENU))
        self.popupMenuTab.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'RO')                
        #menuItem.show()
        
        self.popupMenuTab.mnuClone = menuItem = Gtk.ImageMenuItem(_("Clonar consola"))
        #menuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_COPY, Gtk.ICON_SIZE_MENU))
        menuItem.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_COPY, Gtk.IconSize.MENU))
        self.popupMenuTab.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'CC')
        menuItem.show()

        self.popupMenuTab.mnuLog = menuItem = Gtk.CheckMenuItem(_("Habilitar log"))
        self.popupMenuTab.append(menuItem)
        menuItem.connect("activate", self.on_popupmenu, 'L')
        menuItem.show()
        
    def createMenuItem(self, shortcut, label):
        menuItem = Gtk.MenuItem('')
        menuItem.get_child().set_markup("<span color='blue'  size='x-small'>[%s]</span> %s" % (shortcut, label))
        menuItem.show()
        return menuItem
                
    def populateCommandsMenu(self):
        #self.popupMenu.mnuCommands.remove_all()

        #for custom in self.menuCustomCommands: 
        #   custom.remove()

        for x in shortcuts:
            if type(shortcuts[x]) != list:
                menuItem = self.createMenuItem(x, shortcuts[x][0:30])
                self.popupMenu.mnuCommands.append(menuItem)
                menuItem.connect("activate", self.on_popupmenu, 'CP', shortcuts[x])
                
                menuItem = self.createMenuItem(x, shortcuts[x][0:30])
                self.menuCustomCommands.append(menuItem)
                menuItem.connect("activate", self.on_menuCustomCommands_activate, shortcuts[x])
                
    def on_menuCustomCommands_activate(self, widget, command):
        terminal = self.find_active_terminal(self.hpMain)
        if terminal:
            terminal.feed_child(command)
    
    def terminal_copy(self, terminal):
        terminal.copy_clipboard()

    def terminal_paste(self, terminal):
        terminal.paste_clipboard()
    
    def terminal_copy_paste(self, terminal):
        terminal.copy_clipboard()
        terminal.paste_clipboard()
          
    def terminal_select_all(self, terminal):
        terminal.select_all()

    def terminal_copy_all(self, terminal):
        terminal.select_all()
        terminal.copy_clipboard()
        terminal.select_none()
                    
    def on_menuCopy_activate(self, widget):
        terminal = self.find_active_terminal(self.hpMain)
        if terminal:
            self.terminal_copy(terminal)
    
    def on_menuPaste_activate(self, widget):
        terminal = self.find_active_terminal(self.hpMain)
        if terminal:
            self.terminal_paste(terminal)
        
    def on_menuCopyPaste_activate(self, widget):
        terminal = self.find_active_terminal(self.hpMain)
        if terminal:
            self.terminal_copy_paste(terminal)
            
    def on_menuSelectAll_activate(self, widget):
        terminal = self.find_active_terminal(self.hpMain)
        if terminal:
            self.terminal_select_all(terminal)
            
    def on_menuCopyAll_activate(self, widget):
        terminal = self.find_active_terminal(self.hpMain)
        if terminal:
            self.terminal_copy_all(terminal)
    
    def on_contents_changed(self, terminal):
        col,row = terminal.get_cursor_position()        
        if terminal.last_logged_row != row:
            text = terminal.get_text_range(terminal.last_logged_row, terminal.last_logged_col, row, col, lambda *args: True, None, None)
            terminal.last_logged_row = row  
            terminal.last_logged_col = col            
            terminal.log.write(text[:-1])

    def set_terminal_logger(self, terminal, enable_logging=True):        
        if enable_logging:
            terminal.last_logged_col, terminal.last_logged_row = terminal.get_cursor_position()
            if hasattr(terminal, "log_handler_id"):
                if terminal.log_handler_id == 0:
                    terminal.log_handler_id = terminal.connect('contents-changed', self.on_contents_changed)
                return True
            terminal.log_handler_id = terminal.connect('contents-changed', self.on_contents_changed)
            p = terminal.get_parent()        
            title = p.get_parent().get_tab_label(p).get_text().strip()
            prefix = "%s/%s-%s" % (os.path.expanduser(conf.LOG_PATH), title, time.strftime("%Y%m%d"))
            filename = ''
            for i in range(1,1000):
                if not os.path.exists("%s-%03i.log" % (prefix,i)):
                    filename = "%s-%03i.log" % (prefix,i)
                    break
            filename == "%s-%03i.log" % (prefix,1)
            try:
                terminal.log = open(filename, 'w', 0)
                terminal.log.write("Session '%s' opened at %s\n%s\n" % (title, time.strftime("%Y-%m-%d %H:%M:%S"), "-"*80))
            except:
                msgbox("%s\n%s" % (_("No se puede abrir el archivo de log para escritura"), filename))
                terminal.disconnect(terminal.log_handler_id)
                del terminal.log_handler_id
                return False
        else:
            if hasattr(terminal, "log_handler_id") and terminal.log_handler_id != 0:
                terminal.disconnect(terminal.log_handler_id)
                terminal.log_handler_id = 0
        return True

    def addTab(self, notebook, host):
        try:
            v = Vte.Terminal()
            #v.set_word_chars(conf.WORD_SEPARATORS)
            v.spawn_sync(
                Vte.PtyFlags.DEFAULT,
                os.environ['HOME'],
                ["/bin/sh"],
                [],
                GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                None,
                None,
                )
            v.set_scrollback_lines(conf.BUFFER_LINES)
            #if v.get_emulation() != os.getenv("TERM"):
            #    os.environ['TERM'] = v.get_emulation()
            
            if isinstance(host, str):
                host = Host('', host) 
            
            fcolor = host.font_color
            bcolor = host.back_color
            if fcolor == '' or fcolor == None or bcolor == '' or bcolor == None:
                fcolor = conf.FONT_COLOR
                bcolor = conf.BACK_COLOR
                
            if len(fcolor)>0 and len(bcolor)>0:
                v.set_colors(Gtk.gdk.Color(fcolor), Gtk.gdk.Color(bcolor), [])

            if len(conf.FONT)==0:
                conf.FONT = 'monospace'
            else:
                v.set_font(pango.FontDescription(conf.FONT))
            
            scrollPane = Gtk.ScrolledWindow()            
            scrollPane.connect('button_press_event', lambda *args: True)
            scrollPane.set_property('hscrollbar-policy', Gtk.PolicyType.NEVER)
            tab = NotebookTabLabel("  %s  " % (host.name), self.nbConsole, scrollPane, self.popupMenuTab )
            
            v.connect("child-exited", lambda widget: tab.mark_tab_as_closed())
            v.connect('focus', self.on_tab_focus)
            v.connect('button_press_event', self.on_terminal_click)
            v.connect('key_press_event', self.on_terminal_keypress)            
            v.connect('selection-changed', self.on_terminal_selection)
            
            if conf.TRANSPARENCY > 0:                 
                if not self.real_transparency:
                    v.set_background_transparent(True)
                    v.set_background_saturation(conf.TRANSPARENCY / 100.0)
                    if len(bcolor)>0:
                        v.set_background_tint_color(Gtk.gdk.Color(bcolor))
                else:
                    v.set_opacity(int( (100 - conf.TRANSPARENCY) / 100.0 * 65535) )
            
            v.set_backspace_binding(host.backspace_key)
            v.set_delete_binding(host.delete_key)
            
            scrollPane.show()
            scrollPane.add(v)                        
            v.show()            
                        
            notebook.append_page(scrollPane, tab_label=tab)
            notebook.set_current_page(self.nbConsole.page_num(scrollPane))  
            notebook.set_tab_reorderable(scrollPane, True)
            notebook.set_tab_detachable(scrollPane, True)            
            self.wMain.set_focus(v)
            self.on_tab_focus(v)
            self.set_terminal_logger(v, host.log)

            GObject.timeout_add(200, lambda : self.wMain.set_focus(v))
            
            #Dar tiempo a la interfaz para que muestre el terminal
            while Gtk.events_pending():
                Gtk.main_iteration()
            
            if host.host == '' or host.host == None:
                v.spawn_sync(
                    Vte.PtyFlags.DEFAULT,
                    os.environ['HOME'],
                    ["/bin/sh"],
                    [],
                    GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                    None,
                    None,
                    )
            else:
                cmd = SSH_COMMAND
                password = host.password
                if host.type == 'ssh':
                    if len(host.user)==0:
                        host.user = get_username()
                    if host.password == '':
                        cmd = SSH_BIN
                        args = [ SSH_BIN, '-l', host.user, '-p', host.port]
                    else:
                        args = [SSH_COMMAND, host.type, '-l', host.user, '-p', host.port]                                       
                    if host.keep_alive!='0' and host.keep_alive!='':
                        args.append('-o')
                        args.append('ServerAliveInterval=%s' % (host.keep_alive))
                    for t in host.tunnel:
                        if t!="":
                            if t.endswith(":*:*"):
                                args.append("-D")
                                args.append(t[:-4])
                            else:
                                args.append("-L")
                                args.append(t)
                    if host.x11:
                        args.append("-X")
                    if host.agent:
                        args.append("-A")
                    if host.compression:
                        args.append("-C")
                        if host.compressionLevel!='':
                            args.append('-o')
                            args.append('CompressionLevel=%s' % (host.compressionLevel))
                    if host.private_key != None and host.private_key != '':
                        args.append("-i")
                        args.append(host.private_key)
                    if host.extra_params != None and host.extra_params != '':
                        args += shlex.split(host.extra_params)
                    args.append(host.host)
                else:
                    if host.user=='' or host.password=='':
                        password=''
                        cmd = TEL_BIN
                        args = [TEL_BIN]
                    else:
                        args = [SSH_COMMAND, host.type, '-l', host.user]
                    if host.extra_params != None and host.extra_params != '':
                        args += shlex.split(host.extra_params)
                    args += [host.host, host.port]
                v.command = (cmd, args, password)
                v.fork_command(cmd, args)
                while Gtk.events_pending():
                    Gtk.main_iteration(False)                                
                
                #esperar 2 seg antes de enviar el pass para dar tiempo a que se levante expect y prevenir que se muestre el pass
                if password!=None and password!='':
                    GObject.timeout_add(2000, self.send_data, v, password)
            
            #esperar 3 seg antes de enviar comandos
            if host.commands!=None and host.commands!='':
                basetime = 700 if len(host.host)==0 else 3000
                lines = []
                for line in host.commands.splitlines():
                    if line.startswith("##D=") and line[4:].isdigit():
                        if len(lines):
                            GObject.timeout_add(basetime, self.send_data, v, "\r".join(lines))
                            lines = []
                        basetime += int(line[4:])
                    else:
                        lines.append(line)
                if len(lines):
                    GObject.timeout_add(basetime, self.send_data, v, "\r".join(lines))
            v.queue_draw()
            
            #guardar datos de consola para clonar consola
            v.host = host
        except:
            tace_text = traceback.format_exc()
            msgbox("%s: %s : %s" % (_("Error al conectar con servidor"), sys.exc_info()[1], tace_text))
            
    def send_data(self, terminal, data):
        terminal.feed_child('%s\r' % (data))        
        return False
        
    def initLeftPane(self):
        global groups       

        self.treeModel = Gtk.TreeStore(GObject.TYPE_STRING, GObject.TYPE_PYOBJECT, GdkPixbuf.Pixbuf)
        self.treeServers.set_model(self.treeModel)

        self.treeServers.set_level_indentation(5)
        #Force the alternating row colors, by default it's off with one column
        self.treeServers.set_property('rules-hint', True)
        Gtk.rc_parse_string( """
                style "custom-treestyle"{
                    GtkTreeView::allow-rules = 1
                }
                widget "*treeServers*" style "custom-treestyle"
            """)
        column = Gtk.TreeViewColumn()
        column.set_title('Servers')
        self.treeServers.append_column( column )

        renderer = Gtk.CellRendererPixbuf()
        column.pack_start(renderer, expand=False)
        column.add_attribute(renderer, 'pixbuf', 2)

        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, expand=True)
        column.add_attribute(renderer, 'text', 0)
        
        self.treeServers.set_has_tooltip(True)
        self.treeServers.connect('query-tooltip', self.on_treeServers_tooltip)
        self.loadConfig()
        self.updateTree()
               
    def on_treeServers_tooltip(self, widget, x, y, keyboard, tooltip):
        x,y = widget.convert_widget_to_bin_window_coords(x, y)
        pos = widget.get_path_at_pos(x, y)
        if pos:
            host = list(widget.get_model()[pos[0]])[1]
            if host:
                text = "<span><b>%s</b>\n%s:%s@%s\n</span><span size='smaller'>%s</span>" % (host.name, host.type, host.user, host.host, host.description)
                tooltip.set_markup(text)
                return True
        return False
        
    def loadConfig(self):
        global groups
        
        cp= configparser.RawConfigParser(  )
        cp.read( CONFIG_FILE )
        
        #Leer configuracion general
        try:
            conf.WORD_SEPARATORS = cp.get("options", "word-separators")
            conf.BUFFER_LINES = cp.getint("options", "buffer-lines")
            conf.CONFIRM_ON_EXIT = cp.getboolean("options", "confirm-exit")
            conf.FONT_COLOR = cp.get("options", "font-color")
            conf.BACK_COLOR = cp.get("options", "back-color")
            conf.TRANSPARENCY = cp.getint("options", "transparency")
            conf.PASTE_ON_RIGHT_CLICK = cp.getboolean("options", "paste-right-click")
            conf.CONFIRM_ON_CLOSE_TAB = cp.getboolean("options", "confirm-close-tab")
            conf.CHECK_UPDATES = cp.getboolean("options", "check-updates")
            conf.COLLAPSED_FOLDERS = cp.get("window", "collapsed-folders")
            conf.LEFT_PANEL_WIDTH = cp.getint("window", "left-panel-width")
            conf.WINDOW_WIDTH = cp.getint("window", "window-width")
            conf.WINDOW_HEIGHT = cp.getint("window", "window-height")
            conf.FONT = cp.get("options", "font")
            conf.HIDE_DONATE = cp.getboolean("options", "donate")
            conf.AUTO_COPY_SELECTION = cp.getboolean("options", "auto-copy-selection")
            conf.LOG_PATH = cp.get("options", "log-path")
            conf.VERSION = cp.get("options", "version")
            conf.AUTO_CLOSE_TAB = cp.getint("options", "auto-close-tab")
            conf.SHOW_PANEL = cp.getboolean("window", "show-panel")
            conf.SHOW_TOOLBAR = cp.getboolean("window", "show-toolbar")
            conf.STARTUP_LOCAL = cp.getboolean("options","startup-local")
        except:
            print("{}: {}".format( _("Entrada invalida en archivo de configuracion"), sys.exc_info()[1] ))
        
        #Leer shorcuts        
        scuts = {}
        try:
            scuts[cp.get("shortcuts", "copy")] = _COPY
        except:
            scuts["CTRL+SHIFT+C"] = _COPY
        try:
            scuts[cp.get("shortcuts", "paste")] = _PASTE
        except:
            scuts["CTRL+SHIFT+V"] = _PASTE
        try:
            scuts[cp.get("shortcuts", "copy_all")] = _COPY_ALL
        except:
            scuts["CTRL+SHIFT+A"] = _COPY_ALL
        try:
            scuts[cp.get("shortcuts", "save")] = _SAVE
        except:
            scuts["CTRL+S"] = _SAVE
        try:
            scuts[cp.get("shortcuts", "find")] = _FIND
        except:
            scuts["CTRL+F"] = _FIND
        try:
            scuts[cp.get("shortcuts", "find_next")] = _FIND_NEXT
        except:
            scuts["F3"] = _FIND_NEXT
        try:
            scuts[cp.get("shortcuts", "find_back")] = _FIND_BACK
        except:
            scuts["SHIFT+F3"] = _FIND_BACK
        
        try:
            scuts[cp.get("shortcuts", "console_previous")] = _CONSOLE_PREV
        except:
            scuts["CTRL+SHIFT+LEFT"] = _CONSOLE_PREV
        
        try:
            scuts[cp.get("shortcuts", "console_next")] = _CONSOLE_NEXT
        except:
            scuts["CTRL+SHIFT+RIGHT"] = _CONSOLE_NEXT

        try:
            scuts[cp.get("shortcuts", "console_close")] = _CONSOLE_CLOSE
        except:
            scuts["CTRL+W"] = _CONSOLE_CLOSE
        
        try:
            scuts[cp.get("shortcuts", "console_reconnect")] = _CONSOLE_RECONNECT
        except:
            scuts["CTRL+N"] = _CONSOLE_RECONNECT
          
        try:
            scuts[cp.get("shortcuts", "connect")] = _CONNECT
        except:
            scuts["CTRL+RETURN"] = _CONNECT
            
        ##kaman
        try:
            scuts[cp.get("shortcuts", "reset")] = _CLEAR
        except:
            scuts["CTRL+K"] = _CLEAR

        #shortcuts para cambiar consola1-consola9
        for x in range(1,10):
            try:
                scuts[cp.get("shortcuts", "console_%d" % (x) )] = eval("_CONSOLE_%d" % (x))                
            except:
                scuts["F%d" % (x)] = eval("_CONSOLE_%d" % (x))                
        try:
            i = 1            
            while True:
                scuts[cp.get("shortcuts", "shortcut%d" % (i))] = cp.get("shortcuts", "command%d" % (i)).replace('\\n','\n')
                i = i + 1
        except:
            pass
        global shortcuts
        shortcuts = scuts
        
        #Leer lista de hosts        
        groups={}
        for section in cp.sections():
            if not section.startswith("host "):
                continue
            host = cp.options(section)
            try:
                host = HostUtils.load_host_from_ini(cp, section)
                
                if not groups.has_key(host.group):                    
                    groups[host.group]=[]
                
                groups[host.group].append( host )
            except:                
                print("{}: {}".format( (_("Entrada invalida en archivo de configuracion"), sys.exc_info()[1]) ))

    def is_node_collapsed(self, model, path, iter, nodes):
        if self.treeModel.get_value(iter, 1)==None and not self.treeServers.row_expanded(path):
             nodes.append(self.treeModel.get_string_from_iter(iter))

    def get_collapsed_nodes(self):
        nodes=[]
        self.treeModel.foreach(self.is_node_collapsed, nodes)
        return nodes
        
    def set_collapsed_nodes(self):
        self.treeServers.expand_all()
        #if self.treeModel.get_iter_root():
        #    for node in conf.COLLAPSED_FOLDERS.split(","): 
        #        if node!='':
        #            self.treeServers.collapse_row(node)
        
    def updateTree(self):
        for grupo in dict(groups):
            if len(groups[grupo])==0:
                del groups[grupo]
        
        if conf.COLLAPSED_FOLDERS == None:
            conf.COLLAPSED_FOLDERS = ','.join(self.get_collapsed_nodes())
        
        self.menuServers.foreach(self.menuServers.remove)
        self.treeModel.clear()
        
        iconHost = self.treeServers.render_icon("gtk-network", size=Gtk.IconSize.BUTTON, detail=None)
        iconDir = self.treeServers.render_icon("gtk-directory", size=Gtk.IconSize.BUTTON, detail=None)             
        
        grupos = groups.keys()
        #grupos.sort(lambda x,y: cmp(y,x))
        sorted(grupos)

        for grupo in grupos:
            group = None
            path = ""
            menuNode = self.menuServers
                  
            for folder in grupo.split("/"):
                path = path + '/' + folder
                row = self.get_folder(self.treeModel, '', path)
                if row == None:
                    group = self.treeModel.prepend(group, [folder, None, iconDir])
                else:
                    group = row.iter
                
                menu = self.get_folder_menu(self.menuServers, '', path)
                if menu == None:
                    menu = Gtk.ImageMenuItem(folder)
                    #menu.set_image(Gtk.image_new_from_stock(Gtk.STOCK_DIRECTORY, Gtk.ICON_SIZE_MENU))
                    menuNode.prepend(menu)
                    menuNode = Gtk.Menu()
                    menu.set_submenu(menuNode)
                    menu.show()
                else:
                    menuNode = menu
                
            groups[grupo].sort(key=operator.attrgetter('name'))
            for host in groups[grupo]:
                self.treeModel.append(group, [host.name, host, iconHost])
                mnuItem = Gtk.ImageMenuItem(host.name)
                mnuItem.set_image(Gtk.image_new_from_stock(Gtk.STOCK_NETWORK, Gtk.ICON_SIZE_MENU))
                mnuItem.show()
                mnuItem.connect("activate", lambda arg, nb, h: self.addTab(nb, h), self.nbConsole, host) 
                menuNode.append(mnuItem)
                
        self.set_collapsed_nodes()
        conf.COLLAPSED_FOLDERS = None
        
    def get_folder(self, obj, folder, path): 
        if not obj: 
            return None        
        for row in obj:
            if path == folder+'/'+row[0]:
                return row
            i = self.get_folder(row.iterchildren(), folder+'/'+row[0], path)
            if i:
                return i
        
    def get_folder_menu(self, obj, folder, path):
        if not obj or not (isinstance(obj,Gtk.Menu) or isinstance(obj,Gtk.MenuItem)):
            return None
        for item in obj.get_children():
            if path == folder+'/'+item.get_label():
                return item.get_submenu()
            i = self.get_folder_menu(item.get_submenu(), folder+'/'+item.get_label(), path)
            if i:
                return i
                
    def writeConfig(self): 
        global groups
        
        cp= ConfigParser.RawConfigParser( )
        cp.read( CONFIG_FILE + ".tmp" )
        
        cp.add_section("options")
        cp.set("options", "word-separators", conf.WORD_SEPARATORS)        
        cp.set("options", "buffer-lines", conf.BUFFER_LINES)
        cp.set("options", "startup-local", conf.STARTUP_LOCAL)
        cp.set("options", "confirm-exit", conf.CONFIRM_ON_EXIT)
        cp.set("options", "font-color", conf.FONT_COLOR)
        cp.set("options", "back-color", conf.BACK_COLOR)
        cp.set("options", "transparency", conf.TRANSPARENCY)        
        cp.set("options", "paste-right-click", conf.PASTE_ON_RIGHT_CLICK)
        cp.set("options", "confirm-close-tab", conf.CONFIRM_ON_CLOSE_TAB)
        cp.set("options", "check-updates", conf.CHECK_UPDATES)
        cp.set("options", "font", conf.FONT)
        cp.set("options", "donate", conf.HIDE_DONATE)
        cp.set("options", "auto-copy-selection", conf.AUTO_COPY_SELECTION)
        cp.set("options", "log-path", conf.LOG_PATH)
        cp.set("options", "version", app_fileversion)
        cp.set("options", "auto-close-tab", conf.AUTO_CLOSE_TAB)

        collapsed_folders = ','.join(self.get_collapsed_nodes())         
        cp.add_section("window")
        cp.set("window", "collapsed-folders", collapsed_folders)
        cp.set("window", "left-panel-width", self.hpMain.get_position())
        cp.set("window", "window-width", conf.WINDOW_WIDTH)
        cp.set("window", "window-height", conf.WINDOW_HEIGHT)
        cp.set("window", "show-panel", conf.SHOW_PANEL)
        cp.set("window", "show-toolbar", conf.SHOW_TOOLBAR)
        
        i=1
        for grupo in groups:
            for host in groups[grupo]:
                section = "host " + str(i)
                cp.add_section(section)
                HostUtils.save_host_to_ini(cp, section, host)
                i+=1
        
        cp.add_section("shortcuts")
        i=1
        for s in shortcuts:            
            if type(shortcuts[s]) == list:
                cp.set("shortcuts", shortcuts[s][0], s)
            else:
                cp.set("shortcuts", "shortcut%d" % (i), s)
                cp.set("shortcuts", "command%d" % (i), shortcuts[s].replace('\n','\\n'))
                i=i+1
                
        f = open(CONFIG_FILE + ".tmp", "w")
        cp.write(f)
        f.close()
        os.rename(CONFIG_FILE + ".tmp", CONFIG_FILE)
        
    def on_tab_focus(self, widget, *args): 
        if isinstance(widget, Vte.Terminal):
            self.current = widget
        
    def split_notebook(self, direction):        
        csp = self.current.get_parent() if self.current!=None else None
        cnb = csp.get_parent() if csp!=None else None
        
        #Separar solo si hay mas de 2 tabs en el notebook actual
        if csp!=None and cnb.get_n_pages()>1:
            #Crear un hpaned, en el hijo 0 dejar el notebook y en el hijo 1 el nuevo notebook
            #El nuevo hpaned dejarlo como hijo del actual parent
            hp = Gtk.HPaned() if direction==HSPLIT else Gtk.VPaned()
            nb = Gtk.Notebook()
            nb.set_group_id(11)
            nb.connect('button_press_event', self.on_double_click, None)
            nb.connect('page_removed', self.on_page_removed)
            nb.connect("page-added", self.on_page_added)
            nb.set_property("scrollable", True)
            cp  = cnb.get_parent()

            if direction==HSPLIT:
                cnb.set_size_request(cnb.allocation.width/2, cnb.allocation.height)
            else:                
                cnb.set_size_request(cnb.allocation.width, cnb.allocation.height/2)
            #cnb.set_size_request(cnb.allocation.width/2, cnb.allocation.height/2)
            
            cp.remove(cnb)
            cp.add(hp)
            hp.add1(cnb)                        
            
            text = cnb.get_tab_label(csp).get_text()
            
            csp.reparent(nb)
            csp = nb.get_nth_page(0)
                        
            tab = NotebookTabLabel(text, nb, csp, self.popupMenuTab)
            nb.set_tab_label(csp, tab_label=tab)
            nb.set_tab_reorderable(csp, True)
            nb.set_tab_detachable(csp, True)
                        
            hp.add2(nb)
            nb.show()
            hp.show()
            hp.queue_draw()
            self.current = cnb.get_nth_page(cnb.get_current_page()).get_children()[0]

    def find_notebook(self, widget, exclude=None):
        if widget!=exclude and isinstance(widget, Gtk.Notebook):
            return widget
        else:
            if not hasattr(widget, "get_children"):
                return None
            for w in widget.get_children():
                wid = self.find_notebook(w, exclude)
                if wid!=exclude and isinstance(wid, Gtk.Notebook):
                    return wid
            return None

    def find_active_terminal(self, widget):        
        if isinstance(widget, Vte.Terminal) and widget.is_focus():
            return widget
        else:
            if not hasattr(widget, "get_children"):
                return None
                             
            for w in widget.get_children():
                wid = self.find_active_terminal(w)                    
                if isinstance(wid, Vte.Terminal) and wid.is_focus():
                    return wid
            return None

    def check_notebook_pages(self, widget):
        if widget.get_n_pages()==0:
            #eliminar el notebook solo si queda otro notebook y no quedan tabs en el actual            
            paned = widget.get_parent()            
            if paned==None or paned==self.hpMain:
                return
            container = paned.get_parent()
            save = paned.get_child2() if paned.get_child1()==widget else paned.get_child1()    
            container.remove(paned)
            paned.remove(save)
            container.add(save)
            if widget == self.nbConsole:                
                if isinstance(save, Gtk.Notebook):
                    self.nbConsole = save
                else:
                    self.nbConsole = self.find_notebook(save)

    def on_page_removed(self, widget, *args):
        self.count-=1
        if hasattr(widget, "is_closed") and widget.is_closed:
            #tab has been closed
            self.check_notebook_pages(widget)
        else:
            #tab has been moved to another notebook
            #save a reference to this notebook, on_page_added check if the notebook must be removed
            self.check_notebook = widget
            
    def on_page_added(self, widget, *args):
        self.count+=1
        if hasattr(self, "check_notebook"):
            self.check_notebook_pages(self.check_notebook)
            delattr(self, "check_notebook")
        
    def show_save_buffer(self, terminal):        
        dlg = Gtk.FileChooserDialog(title=_("Guardar como"), parent=self.wMain, action=Gtk.FILE_CHOOSER_ACTION_SAVE)
        dlg.add_button(Gtk.STOCK_CANCEL, Gtk.RESPONSE_CANCEL)
        dlg.add_button(Gtk.STOCK_SAVE, Gtk.RESPONSE_OK)        
        dlg.set_do_overwrite_confirmation(True)
        dlg.set_current_name( os.path.basename("gcm-buffer-%s.txt" % (time.strftime("%Y%m%d%H%M%S")) ))
        if not hasattr(self,'lastPath'):
            self.lastPath = os.path.expanduser("~")
        dlg.set_current_folder( self.lastPath )
        
        if dlg.run() == Gtk.RESPONSE_OK:
            filename = dlg.get_filename()
            self.lastPath = os.path.dirname(filename)            
    
            try:              
                buff = terminal.get_text_range(0, 0, terminal.get_property('scrollback-lines')-1, terminal.get_column_count()-1, lambda *args: True, None, None ).strip()                
                f = open(filename, "w")
                f.write(buff)
                f.close()
            except:                
                dlg.destroy()
                msgbox("%s: %s" % (_("No se puede abrir archivo para escritura"), filename) )
                return
            
        dlg.destroy()
    
    def set_panel_visible(self, visibility):
        if visibility:
            GObject.timeout_add(200, lambda : self.hpMain.set_position(self.hpMain.previous_position if self.hpMain.previous_position>10 else 150))
        else:       
            self.hpMain.previous_position = self.hpMain.get_position()
            GObject.timeout_add(200, lambda : self.hpMain.set_position(0))
        self.get_widget("show_panel").set_active(visibility)
        conf.SHOW_PANEL = visibility
    
    def set_toolbar_visible(self, visibility):
        #self.get_widget("toolbar1").set_visible(visibility)
        if visibility:
            self.get_widget("toolbar1").show()
        else:
            self.get_widget("toolbar1").hide()
        self.get_widget("show_toolbar").set_active(visibility)
        conf.SHOW_TOOLBAR = visibility
        
    #-- Wmain custom methods }

    #-- Wmain.on_wMain_destroy {
    def on_wMain_destroy(self, widget, *args):                
        #self.writeConfig()
        Gtk.main_quit()
    #-- Wmain.on_wMain_destroy }

    #-- Wmain.on_wMain_delete_event {
    def on_wMain_delete_event(self, widget, *args):
        (conf.WINDOW_WIDTH, conf.WINDOW_HEIGHT) = self.get_widget("wMain").get_size()
        if conf.CONFIRM_ON_EXIT and self.count>0 and msgconfirm("%s %d %s" % (_("Hay"), self.count, _("consolas abiertas, confirma que desea salir?")) ) != Gtk.ResponseType.OK:
            return True
    #-- Wmain.on_wMain_delete_event }

    #-- Wmain.on_guardar_como1_activate {
    def on_guardar_como1_activate(self, widget, *args):        
        term = self.find_active_terminal(self.hpMain)
        if term == None:
            term = self.current
        if term != None:
            self.show_save_buffer(term)
        
    #-- Wmain.on_guardar_como1_activate }

    #-- Wmain.on_importar_servidores1_activate {
    def on_importar_servidores1_activate(self, widget, *args):
        filename = show_open_dialog(parent=self.wMain, title=_("Abrir"), action=Gtk.FILE_CHOOSER_ACTION_OPEN)
        if filename != None:            
            password = inputbox(_('Importar Servidores'), _('Ingrese clave: '), password=True)
            if password == None:
                return                                                
            
            #abrir archivo con lista de servers y cargarlos en el arbol
            try:
                cp= ConfigParser.RawConfigParser( )
                cp.read( filename )
            
                #validar el pass
                s = decrypt(password, cp.get("gcm", "gcm"))
                if (s != password[::-1]):
                    msgbox(_("Clave invalida"))
                    return
            
                if msgconfirm(_(u'Se sobreescribirá la lista de servidores, continuar?')) != Gtk.RESPONSE_OK:
                    return
                    
                grupos={}
                for section in cp.sections():
                    if not section.startswith("host "):
                        continue                    
                    host = HostUtils.load_host_from_ini(cp, section, password)
        
                    if not grupos.has_key(host.group):                    
                        grupos[host.group]=[]  
        
                    grupos[host.group].append( host )
            except:                
                msgbox(_("Archivo invalido"))
                return
            #sobreescribir lista de hosts
            global groups
            groups=grupos
            
            self.updateTree()
    #-- Wmain.on_importar_servidores1_activate }

    #-- Wmain.on_exportar_servidores1_activate {
    def on_exportar_servidores1_activate(self, widget, *args):
        filename = show_open_dialog(parent=self.wMain, title=_("Guardar como"), action=Gtk.FILE_CHOOSER_ACTION_SAVE)
        if filename != None:
            password = inputbox(_('Exportar Servidores'), _('Ingrese clave: '), password=True)
            if password == None:
                return
                
            try:
                cp= ConfigParser.RawConfigParser( )
                cp.read( filename + ".tmp" )
                i=1
                cp.add_section("gcm")
                cp.set("gcm", "gcm", encrypt(password, password[::-1]))
                global groups
                for grupo in groups:
                    for host in groups[grupo]:
                        section = "host " + str(i)
                        cp.add_section(section)
                        HostUtils.save_host_to_ini(cp, section, host, password)                        
                        i+=1
                f = open(filename + ".tmp", "w")
                cp.write(f)
                f.close()
                os.rename(filename + ".tmp", filename)
            except:
                msgbox(_("Archivo invalido"))
    #-- Wmain.on_exportar_servidores1_activate }

    #-- Wmain.on_salir1_activate {
    def on_salir1_activate(self, widget, *args):
        #(conf.WINDOW_WIDTH, conf.WINDOW_HEIGHT) = self.get_widget("wMain").get_size()
        #self.writeConfig()
        Gtk.main_quit()
    #-- Wmain.on_salir1_activate }

    #-- Wmain.on_show_toolbar_activate {
    def on_show_toolbar_toggled(self, widget, *args):
        self.set_toolbar_visible(widget.get_active())
    #-- Wmain.on_show_toolbar_activate }

    #-- Wmain.on_show_panel_activate {
    def on_show_panel_toggled(self, widget, *args):
        self.set_panel_visible(widget.get_active())
    #-- Wmain.on_show_panel_activate }
    
    #-- Wmain.on_acerca_de1_activate {
    def on_acerca_de1_activate(self, widget, *args):
        w_about = Wabout()              
    #-- Wmain.on_acerca_de1_activate }

    #-- Wmain.on_double_click {
    def on_double_click(self, widget, event, *args):
        if event.type in [Gtk.gdk._2BUTTON_PRESS, Gtk.gdk._3BUTTON_PRESS] and event.button == 1:
            if isinstance(widget, Gtk.Notebook):
                pos = event.x + widget.get_allocation().x
                size = widget.get_tab_label(widget.get_nth_page(widget.get_n_pages()-1)).get_allocation()
                if pos <= size.x + size.width + 2 * widget.get_property("tab-vborder") + 8 or event.x >= widget.get_allocation().width - widget.style_get_property("scroll-arrow-hlength"):
                    return True
            self.addTab(widget if isinstance(widget, Gtk.Notebook) else self.nbConsole, 'local')
            return True
    #-- Wmain.on_double_click }

    #-- Wmain.on_btnLocal_clicked {
    def on_btnLocal_clicked(self, widget, *args):        
        if self.current != None and self.current.get_parent()!=None and isinstance(self.current.get_parent().get_parent(), Gtk.Notebook):
            ntbk = self.current.get_parent().get_parent()
        else:
            ntbk = self.nbConsole
        self.addTab(ntbk, 'local')
    #-- Wmain.on_btnLocal_clicked }

    #-- Wmain.on_btnConnect_clicked {
    def on_btnConnect_clicked(self, widget, *args):
        if self.treeServers.get_selection().get_selected()[1]!=None:
            if not self.treeModel.iter_has_child(self.treeServers.get_selection().get_selected()[1]):
                self.on_tvServers_row_activated(self.treeServers)
            else:
                selected = self.treeServers.get_selection().get_selected()[1] 
                group = self.treeModel.get_value(selected,0)       
                parent_group = self.get_group(selected)
                if parent_group != '':
                    group = parent_group + '/' + group
                    
                for g in groups:
                    if g == group or g.startswith(group+'/'):
                        for host in groups[g]:                    
                            self.addTab(self.nbConsole, host)
    #-- Wmain.on_btnConnect_clicked }

    #-- Wmain.on_btnAdd_clicked {
    def on_btnAdd_clicked(self, widget, *args):
        group=""
        if self.treeServers.get_selection().get_selected()[1]!=None:
            selected = self.treeServers.get_selection().get_selected()[1]            
            group = self.get_group(selected)
            if self.treeModel.iter_has_child(self.treeServers.get_selection().get_selected()[1]):
                selected = self.treeServers.get_selection().get_selected()[1] 
                group = self.treeModel.get_value(selected,0)
                parent_group = self.get_group(selected)
                if parent_group != '':
                    group = parent_group + '/' + group                    
        wHost = Whost()
        wHost.init(group)
        self.updateTree()
    #-- Wmain.on_btnAdd_clicked }

    def get_group(self, i):
        if self.treeModel.iter_parent(i):
            p = self.get_group(self.treeModel.iter_parent(i))
            return (p+'/' if p!='' else '') + self.treeModel.get_value(self.treeModel.iter_parent(i),0)
        else:
            return ''
            
    #-- Wmain.on_bntEdit_clicked {
    def on_bntEdit_clicked(self, widget, *args):
        if self.treeServers.get_selection().get_selected()[1]!=None and not self.treeModel.iter_has_child(self.treeServers.get_selection().get_selected()[1]):
            selected = self.treeServers.get_selection().get_selected()[1]
            host = self.treeModel.get_value(selected,1)
            wHost = Whost()
            wHost.init(host.group, host)
            #self.updateTree()            
    #-- Wmain.on_bntEdit_clicked }

    #-- Wmain.on_btnDel_clicked {
    def on_btnDel_clicked(self, widget, *args):
        if self.treeServers.get_selection().get_selected()[1]!=None:
            if not self.treeModel.iter_has_child(self.treeServers.get_selection().get_selected()[1]):
                #Eliminar solo el nodo
                name = self.treeModel.get_value(self.treeServers.get_selection().get_selected()[1],0)
                if msgconfirm("%s [%s]?" % (_("Confirma que desea eliminar el host"), name) ) == Gtk.RESPONSE_OK:
                    host = self.treeModel.get_value(self.treeServers.get_selection().get_selected()[1],1)
                    groups[host.group].remove(host)
                    self.updateTree()
            else:                
                #Eliminar todo el grupo                
                group = self.get_group(self.treeModel.iter_children(self.treeServers.get_selection().get_selected()[1]))
                if msgconfirm("%s [%s]?" % (_("Confirma que desea eliminar todos los hosts del grupo"), group) ) == Gtk.RESPONSE_OK:                                
                    try:
                        del groups[group]
                    except:
                        pass
                    for h in dict(groups):
                        if h.startswith(group+'/'):
                            del groups[h]
                    self.updateTree()
        self.writeConfig()                    
    #-- Wmain.on_btnDel_clicked }

    #-- Wmain.on_btnHSplit_clicked {
    def on_btnHSplit_clicked(self, widget, *args):
        self.split_notebook(HSPLIT)
    #-- Wmain.on_btnHSplit_clicked }

    #-- Wmain.on_btnVSplit_clicked {
    def on_btnVSplit_clicked(self, widget, *args):
        self.split_notebook(VSPLIT)
    #-- Wmain.on_btnVSplit_clicked }

    #-- Wmain.on_btnUnsplit_clicked {
    def on_btnUnsplit_clicked(self, widget, *args):
        wid = self.find_notebook(self.hpMain, self.nbConsole)
        while wid!=None:
            #Mover los tabs al notebook principal           
            while wid.get_n_pages()!=0:
                csp = wid.get_nth_page(0)
                text = wid.get_tab_label(csp).get_text()
                csp.reparent(self.nbConsole)
                csp = self.nbConsole.get_nth_page(self.nbConsole.get_n_pages()-1)
                tab = NotebookTabLabel(text, self.nbConsole, csp, self.popupMenuTab )
                self.nbConsole.set_tab_label(csp, tab_label=tab)                       
                self.nbConsole.set_tab_reorderable(csp, True)
                self.nbConsole.set_tab_detachable(csp, True)
            wid = self.find_notebook(self.hpMain, self.nbConsole)
    #-- Wmain.on_btnUnsplit_clicked }

    #-- Wmain.on_btnConfig_clicked {
    def on_btnConfig_clicked(self, widget, *args):
        wConfig = Wconfig()        
    #-- Wmain.on_btnConfig_clicked }

    #-- Wmain.on_btnDonate_clicked {
    def on_btnDonate_clicked(self, widget, *args):
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
            f.write('<html> \
                     <body onload="document.forms[0].submit()"> \
                     <form action="https://www.paypal.com/cgi-bin/webscr" method="post"> \
                     <input type="hidden" name="cmd" value="_s-xclick"> \
                     <input type="hidden" name="hosted_button_id" value="10257762"> \
                     </form> \
                     </body> \
                     </html>')
            
            if os.name == "nt":
                os.filestart(f.name)
            elif os.name == "posix":
                os.system("/usr/bin/xdg-open %s" % (f.name))
            
    #-- Wmain.on_btnDonate_clicked }
    
    #-- Wmain.on_txtSearch_focus {
    def on_txtSearch_focus(self, widget, *args):
        if widget.get_text() == _('buscar...'):
            widget.modify_text(Gtk.STATE_NORMAL, Gtk.gdk.Color('black'))
            widget.set_text('')
    #-- Wmain.on_txtSearch_focus }

    #-- Wmain.on_txtSearch_focus_out_event {
    def on_txtSearch_focus_out_event(self, widget, *args):
        if widget.get_text() == '':
            widget.modify_text(Gtk.STATE_NORMAL, Gtk.gdk.Color('darkgray'))
            widget.set_text(_('buscar...'))
    #-- Wmain.on_txtSearch_focus_out_event }

    #-- Wmain.on_btnSearchBack_clicked {
    def on_btnSearchBack_clicked(self, widget, *args):
        if self.init_search():       
            self.find_word(backwards=True)
    #-- Wmain.on_btnSearchBack_clicked }

    #-- Wmain.on_btnSearch_clicked {
    def on_btnSearch_clicked(self, widget, *args):        
        if self.init_search():               
            self.find_word()
    #-- Wmain.on_btnSearch_clicked }

    #-- Wmain.on_btnCluster_clicked {
    def on_btnCluster_clicked(self, widget, *args):
        if hasattr(self, 'wCluster'):
            if not self.wCluster.get_property("visible"):
                self.wCluster.destroy()        
                create = True
        else:
            create = True
            
        if not create:
            return True
        
        #obtener lista de consolas abiertas
        consoles = []
        global wMain
        obj = wMain.hpMain        
        s = []
        s.append(obj)
        while len(s) > 0:
            obj = s.pop()
            #agregar hijos de p a s 
            if hasattr(obj, "get_children"):
                for w in obj.get_children():
                    if isinstance(w, Gtk.Notebook) or hasattr(w, "get_children"):
                        s.append(w)
            
            if isinstance(obj, Gtk.Notebook):
                n = obj.get_n_pages()
                for i in range(0,n):
                    terminal = obj.get_nth_page(i).get_child()                    
                    title = obj.get_tab_label(obj.get_nth_page(i)).get_text()
                    consoles.append( (title, terminal) )                
        
        if len(consoles)==0:
            msgbox(_("No hay consolas abiertas"))
            return True
            
        self.wCluster = Wcluster(terms=consoles).get_widget('wCluster')                   
    #-- Wmain.on_btnCluster_clicked }

    #-- Wmain.on_hpMain_button_press_event {
    def on_hpMain_button_press_event(self, widget, event, *args):        
        if event.type in [Gtk.gdk._2BUTTON_PRESS]:            
            p = self.hpMain.get_position()
            self.set_panel_visible(p==0) 
    #-- Wmain.on_hpMain_button_press_event }

    #-- Wmain.on_tvServers_row_activated {
    def on_tvServers_row_activated(self, widget, *args):                
        if not self.treeModel.iter_has_child(widget.get_selection().get_selected()[1]):  
            selected = widget.get_selection().get_selected()[1]
            host = self.treeModel.get_value(selected,1)
            self.addTab(self.nbConsole, host)
    #-- Wmain.on_tvServers_row_activated }

    #-- Wmain.on_tvServers_button_press_event {
    def on_tvServers_button_press_event(self, widget, event, *args):
        if event.type == Gtk.gdk.BUTTON_PRESS and event.button == 3:
            x = int(event.x)
            y = int(event.y)            
            pthinfo = self.treeServers.get_path_at_pos(x, y)
            if pthinfo is None:
                self.popupMenuFolder.mnuDel.hide()
                self.popupMenuFolder.mnuEdit.hide()
                self.popupMenuFolder.mnuCopyAddress.hide()
                self.popupMenuFolder.mnuDup.hide()
            else:
                path, col, cellx, celly = pthinfo                                
                if self.treeModel.iter_children(self.treeModel.get_iter(path)):                                    
                    self.popupMenuFolder.mnuEdit.hide()
                    self.popupMenuFolder.mnuCopyAddress.hide()
                    self.popupMenuFolder.mnuDup.hide()
                else:
                    self.popupMenuFolder.mnuEdit.show()
                    self.popupMenuFolder.mnuCopyAddress.show()
                    self.popupMenuFolder.mnuDup.show()
                self.popupMenuFolder.mnuDel.show()
                self.treeServers.grab_focus()
                self.treeServers.set_cursor( path, col, 0)
            self.popupMenuFolder.popup( None, None, None, event.button, event.time)
            return True
    #-- Wmain.on_tvServers_button_press_event }

class Host():
    def __init__(self, *args):
        try:
            self.i = 0
            self.group = self.get_arg(args, None)
            self.name =  self.get_arg(args, None)
            self.description =  self.get_arg(args, None)            
            self.host =  self.get_arg(args, None)
            self.user =   self.get_arg(args, None)
            self.password = self.get_arg(args, None)
            self.private_key = self.get_arg(args, None)
            self.port = self.get_arg(args, 22)
            self.tunnel = self.get_arg(args, '').split(",")
            self.type = self.get_arg(args, 'ssh')
            self.commands = self.get_arg(args, None)
            self.keep_alive = self.get_arg(args, 0)
            self.font_color = self.get_arg(args, '')
            self.back_color = self.get_arg(args, '')
            self.x11 = self.get_arg(args, False)
            self.agent = self.get_arg(args, False)
            self.compression = self.get_arg(args,False)
            self.compressionLevel = self.get_arg(args,'')
            self.extra_params = self.get_arg(args, '')
            self.log = self.get_arg(args, False)
            self.backspace_key = self.get_arg(args, int(Vte.EraseBinding.AUTO))
            self.delete_key = self.get_arg(args, int(Vte.EraseBinding.AUTO))
        except:
            pass
       

    def get_arg(self, args, default):
        arg = args[self.i] if len(args)>self.i else default
        self.i +=1
        return arg

    def __repr__(self):
        return "group=[%s],\t name=[%s],\t host=[%s],\t type=[%s]" % (self.group, self.name, self.host, self.type)

    def tunnel_as_string(self):
        return ",".join(self.tunnel)

    def clone(self):
        return Host(self.group, self.name, self.description, self.host, self.user, self.password, self.private_key, self.port, self.tunnel_as_string(), self.type, self.commands, self.keep_alive, self.font_color, self.back_color, self.x11, self.agent, self.compression, self.compressionLevel, self.extra_params, self.log, self.backspace_key, self.delete_key)

class HostUtils:
    @staticmethod
    def get_val(cp, section, name, default):
        try:
            return cp.get(section, name) if type(default)!=type(True) else cp.getboolean(section, name)
        except:
            return default
    
    @staticmethod
    def load_host_from_ini(cp, section, pwd=''):
        if pwd=='':
            pwd = get_password()
        group = cp.get(section, "group")
        name = cp.get(section, "name")
        host = cp.get(section, "host")
        user = cp.get(section, "user")
        password = decrypt(pwd, cp.get(section, "pass"))
        description = HostUtils.get_val(cp, section, "description", "")
        private_key = HostUtils.get_val(cp, section, "private_key", "")
        port = HostUtils.get_val(cp, section, "port", "22")
        tunnel = HostUtils.get_val(cp, section, "tunnel", "")
        ctype = HostUtils.get_val(cp, section, "type", "ssh")
        commands = HostUtils.get_val(cp, section, "commands", "").replace('\x00', '\n')
        keepalive = HostUtils.get_val(cp, section, "keepalive", "")
        fcolor = HostUtils.get_val(cp, section, "font-color", "")
        bcolor = HostUtils.get_val(cp, section, "back-color", "")
        x11 = HostUtils.get_val(cp, section, "x11", False)
        agent = HostUtils.get_val(cp, section, "agent", False)
        compression = HostUtils.get_val(cp, section, "compression", False)
        compressionLevel = HostUtils.get_val(cp, section, "compression-level", "")
        extra_params = HostUtils.get_val(cp, section, "extra_params", "")
        log = HostUtils.get_val(cp, section, "log", False)
        backspace_key = int(HostUtils.get_val(cp, section, "backspace-key", int(Vte.ERASE_AUTO)))
        delete_key = int(HostUtils.get_val(cp, section, "delete-key", int(Vte.ERASE_AUTO)))
        h = Host(group, name, description, host, user, password, private_key, port, tunnel, ctype, commands, keepalive, fcolor, bcolor, x11, agent, compression, compressionLevel,  extra_params, log, backspace_key, delete_key)
        return h

    @staticmethod
    def save_host_to_ini(cp, section, host, pwd=''):
        if pwd=='':
            pwd = get_password()
        cp.set(section, "group", host.group)
        cp.set(section, "name", host.name)
        cp.set(section, "description", host.description)
        cp.set(section, "host", host.host)
        cp.set(section, "user", host.user)
        cp.set(section, "pass", encrypt(pwd, host.password))
        cp.set(section, "private_key", host.private_key)
        cp.set(section, "port", host.port)
        cp.set(section, "tunnel", host.tunnel_as_string())
        cp.set(section, "type", host.type)
        cp.set(section, "commands", host.commands.replace('\n', '\x00'))
        cp.set(section, "keepalive", host.keep_alive)
        cp.set(section, "font-color", host.font_color)
        cp.set(section, "back-color", host.back_color)
        cp.set(section, "x11", host.x11)
        cp.set(section, "agent", host.agent)
        cp.set(section, "compression", host.compression)
        cp.set(section, "compression-level", host.compressionLevel)
        cp.set(section, "extra_params", host.extra_params)
        cp.set(section, "log", host.log)
        cp.set(section, "backspace-key", host.backspace_key)
        cp.set(section, "delete-key", host.delete_key)

class Whost(SimpleGladeApp):

    def __init__(self, path="gnome-connection-manager.glade",
                 root="wHost",
                 domain=domain_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)
        
        self.treeModel = Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING, GObject.TYPE_STRING, GObject.TYPE_STRING)
        self.treeTunel.set_model(self.treeModel)
        column = Gtk.TreeViewColumn(_("Local"), Gtk.CellRendererText(), text=0)
        self.treeTunel.append_column( column )        
        column = Gtk.TreeViewColumn(_("Host"), Gtk.CellRendererText(), text=1)
        self.treeTunel.append_column( column )        
        column = Gtk.TreeViewColumn(_("Remoto"), Gtk.CellRendererText(), text=2)
        self.treeTunel.append_column( column )        


    #-- Whost.new {
    def new(self):
        global groups
        
        self.cmbGroup = self.get_widget("cmbGroup")
        self.txtName = self.get_widget("txtName")
        self.txtDescription = self.get_widget("txtDescription")
        self.txtHost = self.get_widget("txtHost")
        self.cmbType = self.get_widget("cmbType")
        self.txtUser = self.get_widget("txtUser")
        self.txtPass = self.get_widget("txtPassword")
        self.txtPrivateKey = self.get_widget("txtPrivateKey")
        self.btnBrowse = self.get_widget("btnBrowse")
        self.txtPort = self.get_widget("txtPort")
        self.cmbGroup.get_model().clear()
        for group in groups:
            self.cmbGroup.get_model().append([group])
        self.isNew = True
        
        self.chkDynamic = self.get_widget("chkDynamic")
        self.txtLocalPort = self.get_widget("txtLocalPort")
        self.txtRemoteHost = self.get_widget("txtRemoteHost")
        self.txtRemotePort = self.get_widget("txtRemotePort")
        self.treeTunel = self.get_widget("treeTunel")
        self.txtComamnds = self.get_widget("txtCommands")
        self.chkComamnds = self.get_widget("chkCommands")
        buf = self.txtComamnds.get_buffer()
        buf.create_tag('DELAY1', style=pango.STYLE_ITALIC, foreground='darkgray')
        buf.create_tag('DELAY2', style=pango.STYLE_ITALIC, foreground='cadetblue')
        buf.connect("changed", self.update_texttags)
        self.chkKeepAlive = self.get_widget("chkKeepAlive")
        self.txtKeepAlive = self.get_widget("txtKeepAlive")
        self.btnFColor = self.get_widget("btnFColor")
        self.btnBColor = self.get_widget("btnBColor")
        self.chkX11 = self.get_widget("chkX11")
        self.chkAgent = self.get_widget("chkAgent")
        self.chkCompression = self.get_widget("chkCompression")
        self.txtCompressionLevel = self.get_widget("txtCompressionLevel")
        self.txtExtraParams = self.get_widget("txtExtraParams")
        self.chkLogging = self.get_widget("chkLogging")
        self.cmbBackspace = self.get_widget("cmbBackspace")
        self.cmbDelete = self.get_widget("cmbDelete")
        self.cmbType.set_active(0)
        self.cmbBackspace.set_active(0)
        self.cmbDelete.set_active(0)
    #-- Whost.new }

    #-- Whost custom methods {
    def init(self, group, host=None):
        self.cmbGroup.get_child().set_text(group)
        if host == None:
            self.isNew = True
            return
        
        self.isNew = False
        self.oldGroup = group
        self.txtName.set_text(host.name)
        self.oldName = host.name
        self.txtDescription.set_text(host.description)
        self.txtHost.set_text(host.host)                
        i =  self.cmbType.get_model().get_iter_first()
        while i!=None:                    
            if (host.type == self.cmbType.get_model()[i][0]):
                self.cmbType.set_active_iter(i)
                break
            else:
                i = self.cmbType.get_model().iter_next(i)
        self.txtUser.set_text(host.user)
        self.txtPass.set_text(host.password)
        self.txtPrivateKey.set_text(host.private_key)
        self.txtPort.set_text(host.port)
        for t in host.tunnel:
            if t!="":
                tun = t.split(":")
                tun.append(t)
                self.treeModel.append(  tun )
        self.txtCommands.set_sensitive(False)
        self.chkCommands.set_active(False)
        if host.commands!='' and host.commands!=None:
            self.txtCommands.get_buffer().set_text(host.commands)
            self.txtCommands.set_sensitive(True)
            self.chkCommands.set_active(True)
        use_keep_alive = host.keep_alive!='' and host.keep_alive!='0' and host.keep_alive!=None
        self.txtKeepAlive.set_sensitive(use_keep_alive)
        self.chkKeepAlive.set_active(use_keep_alive)
        self.txtKeepAlive.set_text(host.keep_alive)
        if host.font_color!='' and host.font_color!=None and host.back_color!='' and host.back_color!=None:
            self.get_widget("chkDefaultColors").set_active(False)
            self.btnFColor.set_sensitive(True)
            self.btnBColor.set_sensitive(True)
            fcolor=host.font_color
            bcolor=host.back_color
        else:
            self.get_widget("chkDefaultColors").set_active(True)
            self.btnFColor.set_sensitive(False)
            self.btnBColor.set_sensitive(False)
            fcolor="#FFFFFF"
            bcolor="#000000"
 
        self.btnFColor.set_color(Gtk.gdk.Color(fcolor))
        self.btnBColor.set_color(Gtk.gdk.Color(bcolor))
        
        m = self.btnFColor.get_colormap() 
        color = m.alloc_color("red")
        style = self.btnFColor.get_style().copy()
        style.bg[Gtk.STATE_NORMAL] = color
        self.btnFColor.set_style(style)
        self.btnFColor.queue_draw()
        
        self.btnFColor.selected_color=fcolor
        self.btnBColor.selected_color=bcolor
        self.chkX11.set_active(host.x11)   
        self.chkAgent.set_active(host.agent)
        self.chkCompression.set_active(host.compression)
        self.txtCompressionLevel.set_text(host.compressionLevel)
        self.txtExtraParams.set_text(host.extra_params)
        self.chkLogging.set_active(host.log)
        self.cmbBackspace.set_active(host.backspace_key)
        self.cmbDelete.set_active(host.delete_key)
        self.update_texttags()
        
    def update_texttags(self, *args):
        buf = self.txtCommands.get_buffer()
        text_iter = buf.get_start_iter()
        buf.remove_all_tags(text_iter, buf.get_end_iter())
        while True:
            found = text_iter.forward_search("##D=",0, None)
            if not found: 
                break
            start, end = found
            n = end.copy()
            end.forward_line()
            if buf.get_text(n, end).rstrip().isdigit():
                buf.apply_tag_by_name("DELAY1", start, n)
                buf.apply_tag_by_name("DELAY2", n, end)
            text_iter = end
            
    #-- Whost custom methods }

    #-- Whost.on_cancelbutton1_clicked {
    def on_cancelbutton1_clicked(self, widget, *args):
        self.get_widget("wHost").destroy()
    #-- Whost.on_cancelbutton1_clicked }


    #-- Whost.on_okbutton1_clicked {
    def on_okbutton1_clicked(self, widget, *args):
        group = self.cmbGroup.get_active_text().strip()
        name = self.txtName.get_text().strip()
        description = self.txtDescription.get_text().strip()
        host = self.txtHost.get_text().strip()
        ctype = self.cmbType.get_active_text().strip()
        user = self.txtUser.get_text().strip()
        password = self.txtPass.get_text().strip()
        private_key = self.txtPrivateKey.get_text().strip()
        port = self.txtPort.get_text().strip()
        buf = self.txtCommands.get_buffer()
        commands = buf.get_text(buf.get_start_iter(), buf.get_end_iter()).strip() if self.chkCommands.get_active() else ""
        keepalive = self.txtKeepAlive.get_text().strip()
        if self.get_widget("chkDefaultColors").get_active():
            fcolor=""
            bcolor=""
        else:
            fcolor = self.btnFColor.selected_color
            bcolor = self.btnBColor.selected_color
        
        x11 = self.chkX11.get_active()
        agent = self.chkAgent.get_active()
        compression = self.chkCompression.get_active()
        compressionLevel = self.txtCompressionLevel.get_text().strip()
        extra_params = self.txtExtraParams.get_text()
        log = self.chkLogging.get_active()
        backspace_key = self.cmbBackspace.get_active()
        delete_key = self.cmbDelete.get_active()
        
        if ctype == "":
            ctype = "ssh"
        tunnel=""
        
        if ctype=="ssh":
            for x in self.treeModel:
                tunnel = '%s,%s' % (x[3], tunnel)
            tunnel=tunnel[:-1]
        
        #Validar datos
        if group=="" or name=="" or (host=="" and ctype!='local'):
            msgbox(_("Los campos grupo, nombre y host son obligatorios"))
            return
        
        if not (port and port.isdigit() and 1 <= int(port) <= 65535):
            msgbox(_("Puerto invalido"))
            return
        
        host = Host(group, name, description, host, user, password, private_key, port, tunnel, ctype, commands, keepalive, fcolor, bcolor, x11, agent, compression, compressionLevel,  extra_params, log, backspace_key, delete_key)
                    
        try:
            #Guardar                
            if not groups.has_key(group):
                groups[group]=[]   
            
            if self.isNew:
                for h in groups[group]:
                    if h.name == name:
                        msgbox("%s [%s] %s [%s]" % (_("El nombre"), name, _("ya existe para el grupo"), group))
                        return
                #agregar host a grupo
                groups[group].append( host )
            else:
                if self.oldGroup!=group:
                    #revisar que no este el nombre en el nuevo grupo
                    if not groups.has_key(group):
                        groups[group] = [ host ]
                    else:
                        for h in groups[group]:
                            if h.name == name:
                                msgbox("%s [%s] %s [%s]" % (_("El nombre"), name, _("ya existe para el grupo"), group))
                                return
                        groups[group].append( host )
                        for h in groups[self.oldGroup]:
                            if h.name == self.oldName:
                                groups[self.oldGroup].remove(h)
                                break
                else:
                    if self.oldName!=name:                        
                        for h in groups[self.oldGroup]:
                            if h.name == name:
                                msgbox("%s [%s] %s [%s]" % (_("El nombre"), name, _("ya existe para el grupo"), group))
                                return
                        for h in groups[self.oldGroup]:
                            if h.name == self.oldName:
                                index = groups[self.oldGroup].index(h)
                                groups[self.oldGroup][ index ] = host
                                break
                    else:
                        for h in groups[self.oldGroup]:
                            if h.name == self.oldName:
                                index = groups[self.oldGroup].index(h)
                                groups[self.oldGroup][ index ] = host
                                break
        except:
            msgbox("%s [%s]" % (_("Error al guardar el host. Descripcion"), sys.exc_info()[1]))            
        
        global wMain
        wMain.updateTree()
        wMain.writeConfig()
        
        self.get_widget("wHost").destroy()
    #-- Whost.on_okbutton1_clicked }

    #-- Whost.on_cmbType_changed {
    def on_cmbType_changed(self, widget, *args):
        is_local = widget.get_active_text()=="local"
        self.txtUser.set_sensitive(not is_local)
        self.txtPassword.set_sensitive(not is_local)
        self.txtPort.set_sensitive(not is_local)
        self.txtHost.set_sensitive(not is_local)
        self.txtExtraParams.set_sensitive(not is_local)
        
        if widget.get_active_text()=="ssh":
            self.get_widget("table2").show_all()
            self.txtKeepAlive.set_sensitive(True)
            self.chkKeepAlive.set_sensitive(True)
            self.chkX11.set_sensitive(True)
            self.chkAgent.set_sensitive(True)
            self.chkCompression.set_sensitive(True)
            self.txtCompressionLevel.set_sensitive(self.chkCompression.get_active())
            self.txtPrivateKey.set_sensitive(True)
            self.btnBrowse.set_sensitive(True)
            port = "22"
        else:
            self.get_widget("table2").hide_all()
            self.txtKeepAlive.set_text('0')
            self.txtKeepAlive.set_sensitive(False)
            self.chkKeepAlive.set_sensitive(False)
            self.chkX11.set_sensitive(False)
            self.chkAgent.set_sensitive(False)
            self.chkCompression.set_sensitive(False)
            self.txtCompressionLevel.set_sensitive(False)
            self.txtPrivateKey.set_sensitive(False)
            self.btnBrowse.set_sensitive(False)
            port = "23"
            if is_local:
                self.txtUser.set_text('')
                self.txtPassword.set_text('')
                self.txtPort.set_text('')
                self.txtHost.set_text('')
        self.txtPort.set_text(port)
    #-- Whost.on_cmbType_changed }

    #-- Whost.on_chkKeepAlive_toggled {
    def on_chkKeepAlive_toggled(self, widget, *args):
        if (widget.get_active()):
            self.txtKeepAlive.set_text('120')
        else:
            self.txtKeepAlive.set_text('0')
        self.txtKeepAlive.set_sensitive(widget.get_active())
    #-- Whost.on_chkKeepAlive_toggled }

    #-- Whost.on_chkCompression_toggled {
    def on_chkCompression_toggled(self, widget, *args):
        self.txtCompressionLevel.set_text('')
        self.txtCompressionLevel.set_sensitive(widget.get_active())
    #-- Whost.on_chkCompression_toggled }
    

    #-- Whost.on_chkDynamic_toggled {
    def on_chkDynamic_toggled(self, widget, *args):
        self.txtRemoteHost.set_sensitive(not widget.get_active())
        self.txtRemotePort.set_sensitive(not widget.get_active())
    #-- Whost.on_chkDynamic_toggled }
    
    #-- Whost.on_btnAdd_clicked {
    def on_btnAdd_clicked(self, widget, *args):                
        local = self.txtLocalPort.get_text().strip()
        host = self.txtRemoteHost.get_text().strip()        
        remote = self.txtRemotePort.get_text().strip()
        
        if self.chkDynamic.get_active():
            host = '*'
            remote = '*'
        
        #Validar datos del tunel
        if host == "":
            msgbox(_("Debe ingresar host remoto"))
            return
            
        for x in self.treeModel:
            if x[0] == local:
                msgbox(_("Puerto local ya fue asignado"))
                return
                        
        tunel = self.treeModel.append( [local, host, remote, '%s:%s:%s' % (local, host, remote) ] )
    #-- Whost.on_btnAdd_clicked }

    #-- Whost.on_btnDel_clicked {
    def on_btnDel_clicked(self, widget, *args):
        if self.treeTunel.get_selection().get_selected()[1]!=None:
            self.treeModel.remove(self.treeTunel.get_selection().get_selected()[1])
    #-- Whost.on_btnDel_clicked }

    #-- Whost.on_chkCommands_toggled {
    def on_chkCommands_toggled(self, widget, *args):
        self.txtCommands.set_sensitive(widget.get_active())
    #-- Whost.on_chkCommands_toggled }

    #-- Whost.on_btnBColor_clicked {
    def on_btnBColor_clicked(self, widget, *args):
        widget.selected_color = widget.get_color().to_string()
    #-- Whost.on_btnBColor_clicked }

    #-- Whost.on_chkDefaultColors_toggled {
    def on_chkDefaultColors_toggled(self, widget, *args):
        self.btnFColor.set_sensitive(not widget.get_active())
        self.btnBColor.set_sensitive(not widget.get_active())
    #-- Whost.on_chkDefaultColors_toggled }

    #-- Whost.on_btnFColor_clicked {
    def on_btnFColor_clicked(self, widget, *args):
        widget.selected_color = widget.get_color().to_string()
    #-- Whost.on_btnFColor_clicked }

    #-- Whost.on_btnBrowse_clicked {
    def on_btnBrowse_clicked(self, widget, *args):
        global wMain
        filename = show_open_dialog(parent=wMain.wMain, title=_("Abrir"), action=Gtk.FILE_CHOOSER_ACTION_OPEN)
        if filename != None:
            self.txtPrivateKey.set_text(filename)
    #-- Whost.on_btnBrowse_clicked }

class Wabout(SimpleGladeApp):

    def __init__(self, path="gnome-connection-manager.glade",
                 root="wAbout",
                 domain=domain_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)
        self.wAbout.set_icon_from_file(ICON_PATH)
    #-- Wabout.new {
    def new(self):       
        self.wAbout.set_name(app_name)
        self.wAbout.set_version(app_version)
        self.wAbout.set_website(app_web)    
    #-- Wabout.new }

    #-- Wabout custom methods {
    #   Write your own methods here
    #-- Wabout custom methods }

    #-- Wabout.on_wAbout_close {
    def on_wAbout_close(self, widget, *args):
        self.wAbout.destroy()
    #-- Wabout.on_wAbout_close }


class Wconfig(SimpleGladeApp):

    def __init__(self, path="gnome-connection-manager.glade",
                 root="wConfig",
                 domain=domain_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

    #-- Wconfig.new {
    def new(self):
        #Agregar controles
        self.tblGeneral = self.get_widget("tblGeneral")
        self.btnFColor = self.get_widget("btnFColor")
        self.btnBColor = self.get_widget("btnBColor")
        self.btnFont = self.get_widget("btnFont")
        self.lblFont = self.get_widget("lblFont")
        self.treeCmd = self.get_widget("treeCommands")
        self.treeCustom = self.get_widget("treeCustom")
        self.dlgColor = None
        self.capture_keys = False
        
        self.tblGeneral.rows = 0
        self.addParam(_("Separador de Palabras"), "conf.WORD_SEPARATORS", str)
        self.addParam(_(u"Tamaño del buffer"), "conf.BUFFER_LINES", int, 1, 1000000)
        self.addParam(_("Transparencia"), "conf.TRANSPARENCY", int, 0, 100)
        self.addParam(_("Ruta de logs"), "conf.LOG_PATH", str)
        self.addParam(_("Abrir consola local al inicio"), "conf.STARTUP_LOCAL", bool)
        self.addParam(_(u"Pegar con botón derecho"), "conf.PASTE_ON_RIGHT_CLICK", bool)
        self.addParam(_(u"Copiar selección al portapapeles"), "conf.AUTO_COPY_SELECTION", bool)
        self.addParam(_("Confirmar al cerrar una consola"), "conf.CONFIRM_ON_CLOSE_TAB", bool)
        self.addParam(_("Cerrar consola"), "conf.AUTO_CLOSE_TAB", list, [_("Nunca"), _("Siempre"), _(u"Sólo si no hay errores")])
        self.addParam(_("Confirmar al salir"), "conf.CONFIRM_ON_EXIT", bool)  
        self.addParam(_("Comprobar actualizaciones"), "conf.CHECK_UPDATES", bool)
        self.addParam(_(u"Ocultar botón donar"), "conf.HIDE_DONATE", bool)
        
        if len(conf.FONT_COLOR)==0:
            self.get_widget("chkDefaultColors").set_active(True)
            self.btnFColor.set_sensitive(False)
            self.btnBColor.set_sensitive(False)
            fcolor="#FFFFFF"
            bcolor="#000000"
        else:
            self.get_widget("chkDefaultColors").set_active(False)
            self.btnFColor.set_sensitive(True)
            self.btnBColor.set_sensitive(True)
            fcolor=conf.FONT_COLOR
            bcolor=conf.BACK_COLOR            
 
        self.btnFColor.set_color(Gtk.gdk.Color(fcolor))
        self.btnBColor.set_color(Gtk.gdk.Color(bcolor))
        self.btnFColor.selected_color=fcolor
        self.btnBColor.selected_color=bcolor
        
        #Fuente
        if len(conf.FONT)==0 or conf.FONT == 'monospace':
            conf.FONT = 'monospace'
        else:
            self.chkDefaultFont.set_active(False)
        self.btnFont.selected_font = pango.FontDescription(conf.FONT)
        self.btnFont.set_label(self.btnFont.selected_font.to_string())
        self.btnFont.get_child().modify_font(self.btnFont.selected_font)
        
        #commandos
        self.treeModel = Gtk.TreeStore(GObject.TYPE_STRING, GObject.TYPE_STRING)
        self.treeCmd.set_model(self.treeModel)
        column = Gtk.TreeViewColumn(_(u"Acción"), Gtk.CellRendererText(), text=0)
        column.set_sizing(Gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_expand(True)
        self.treeCmd.append_column( column )
        
        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.connect('edited', self.on_edited, self.treeModel, 1)
        renderer.connect('editing-started', self.on_editing_started, self.treeModel, 1)
        column = Gtk.TreeViewColumn(_("Atajo"), renderer, text=1)
        column.set_sizing(Gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column.set_expand(False)        
        self.treeCmd.append_column( column )
        
        self.treeModel2 = Gtk.TreeStore(GObject.TYPE_STRING, GObject.TYPE_STRING)
        self.treeCustom.set_model(self.treeModel2)
        renderer = MultilineCellRenderer()
        renderer.set_property("editable", True)
        renderer.connect('edited', self.on_edited, self.treeModel2, 0)
        column = Gtk.TreeViewColumn(_("Comando"), renderer, text=0)
        column.set_sizing(Gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_expand(True)       
        self.treeCustom.append_column( column )
        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.connect('edited', self.on_edited, self.treeModel2, 1)
        renderer.connect('editing-started', self.on_editing_started, self.treeModel2, 1)        
        column = Gtk.TreeViewColumn(_("Atajo"), renderer, text=1)
        column.set_sizing(Gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column.set_expand(False)        
        self.treeCustom.append_column( column )
        
        slist = sorted(shortcuts.iteritems(), key=(lambda k_v: (k_v[1], k_v[0]) ))
        
        for s in slist:
            if type(s[1])==list:
                self.treeModel.append(None, [ s[1][0], s[0] ])
        for s in slist:
            if type(s[1])!=list:
                self.treeModel2.append(None, [ s[1], s[0] ])

        self.treeModel2.append(None, [ '', '' ])
    #-- Wconfig.new }

    #-- Wconfig custom methods {
    def addParam(self, name, field, ptype, *args):
        x = self.tblGeneral.rows
        self.tblGeneral.rows += 1
        value = eval(field)
        if ptype==bool:
            obj = Gtk.CheckButton()
            obj.set_label(name)
            obj.set_active(value)
            obj.set_alignment(0, 0.5)            
            obj.show()
            obj.field=field
            self.tblGeneral.attach(obj, 0, 2, x, x+1, Gtk.EXPAND|Gtk.FILL, 0)            
        elif ptype==int:            
            obj = Gtk.SpinButton(climb_rate=10)
            if len(args)==2:
                obj.set_range(args[0], args[1])
            obj.set_increments(1, 10)
            obj.set_numeric(True)
            obj.set_value(value)                        
            obj.show()
            obj.field=field
            lbl = Gtk.Label(name)
            lbl.set_alignment(0, 0.5)
            lbl.show()
            self.tblGeneral.attach(lbl, 0, 1, x, x+1, Gtk.FILL, 0)
            self.tblGeneral.attach(obj, 1, 2, x, x+1, Gtk.EXPAND|Gtk.FILL, 0)
        elif ptype==list:
            obj = Gtk.combo_box_new_text()
            for s in args[0]:
                obj.append_text(s)
            obj.set_active(value)
            obj.show()
            obj.field=field
            lbl = Gtk.Label(name)
            lbl.set_alignment(0, 0.5)
            lbl.show()
            self.tblGeneral.attach(lbl, 0, 1, x, x+1, Gtk.FILL, 0)
            self.tblGeneral.attach(obj, 1, 2, x, x+1, Gtk.EXPAND|Gtk.FILL, 0)
        else:            
            obj = Gtk.Entry()
            obj.set_text(value)            
            obj.show()
            obj.field=field
            lbl = Gtk.Label(name)
            lbl.set_alignment(0, 0.5)
            lbl.show()
            self.tblGeneral.attach(lbl, 0, 1, x, x+1, Gtk.FILL, 0)
            self.tblGeneral.attach(obj, 1, 2, x, x+1, Gtk.EXPAND|Gtk.FILL, 0)
        
    def on_edited(self, widget, rownum, value, model, colnum):        
        model[rownum][colnum] = value
        if model==self.treeModel2:
            i = self.treeModel2.get_iter_first()
            while i != None:
                j = self.treeModel2.iter_next(i)
                self.treeModel2[i]
                if self.treeModel2[i][0] == self.treeModel2[i][1] == "":
                    self.treeModel2.remove(i)
                i = j
            self.treeModel2.append(None, [ '', '' ])
            if self.capture_keys:
                self.capture_keys = False                
            
    def on_editing_started(self, widget, entry, rownum, model, colnum):
        self.capture_keys = True
        entry.connect('key-press-event', self.on_treeCommands_key_press_event, model, rownum, colnum)        
    #-- Wconfig custom methods }

    #-- Wconfig.on_cancelbutton1_clicked {
    def on_cancelbutton1_clicked(self, widget, *args):
        self.get_widget("wConfig").destroy()
    #-- Wconfig.on_cancelbutton1_clicked }

    #-- Wconfig.on_okbutton1_clicked {
    def on_okbutton1_clicked(self, widget, *args):
        for obj in self.tblGeneral:
            if hasattr(obj, "field"):
                if isinstance(obj, Gtk.CheckButton):
                    value = obj.get_active()
                elif isinstance(obj, Gtk.SpinButton):
                    value = obj.get_value_as_int()
                elif isinstance(obj, Gtk.ComboBox):
                    value = obj.get_active()
                else:
                    value = '"%s"' % (obj.get_text())
                exec("%s=%s" % (obj.field, value))
        
        if self.get_widget("chkDefaultColors").get_active():
            conf.FONT_COLOR=""
            conf.BACK_COLOR=""
        else:
            conf.FONT_COLOR = self.btnFColor.selected_color
            conf.BACK_COLOR = self.btnBColor.selected_color
        
        if self.btnFont.selected_font.to_string() != 'monospace' and not self.chkDefaultFont.get_active():
            conf.FONT = self.btnFont.selected_font.to_string()
        else:
            conf.FONT = ''
            
        #Guardar shortcuts
        scuts={}
        for x in self.treeModel:
            if x[0]!='' and x[1]!='':
                scuts[x[1]] = [x[0]]
        for x in self.treeModel2:
            if x[0]!='' and x[1]!='':
                scuts[x[1]] = x[0]        
        global shortcuts        
        shortcuts = scuts
        
        #Boton donate
        global wMain
        if conf.HIDE_DONATE:
            wMain.get_widget("btnDonate").hide_all()
        else:
            wMain.get_widget("btnDonate").show_all()
        
        #Recrear menu de comandos personalizados
        wMain.populateCommandsMenu()        
        wMain.writeConfig()
        
        self.get_widget("wConfig").destroy()
    #-- Wconfig.on_okbutton1_clicked }

    #-- Wconfig.on_btnBColor_clicked {
    def on_btnBColor_clicked(self, widget, *args):
        widget.selected_color = widget.get_color().to_string()
    #-- Wconfig.on_btnBColor_clicked }

    #-- Wconfig.on_btnFColor_clicked {
    def on_btnFColor_clicked(self, widget, *args):
        widget.selected_color = widget.get_color().to_string()
    #-- Wconfig.on_btnFColor_clicked }

    #-- Wconfig.on_chkDefaultColors_toggled {
    def on_chkDefaultColors_toggled(self, widget, *args):
        self.btnFColor.set_sensitive(not widget.get_active())
        self.btnBColor.set_sensitive(not widget.get_active())
    #-- Wconfig.on_chkDefaultColors_toggled }

    #-- Wconfig.on_chkDefaultFont_toggled {
    def on_chkDefaultFont_toggled(self, widget, *args):
        self.btnFont.set_sensitive(not widget.get_active())
        self.lblFont.set_sensitive(not widget.get_active())
    #-- Wconfig.on_chkDefaultFont_toggled }

    #-- Wconfig.on_btnFont_clicked {
    def on_btnFont_clicked(self, widget, *args):
        show_font_dialog(self, _("Seleccione la fuente"), self.btnFont)
    #-- Wconfig.on_btnFont_clicked }

    #-- Wconfig.on_treeCommands_key_press_event {
    def on_treeCommands_key_press_event(self, widget, event, *args):
        if self.capture_keys and len(args)==3 and (event.keyval != Gtk.keysyms.Return or
                                                   event.state != 0):
            model, rownum, colnum = args           
            widget.set_text(get_key_name(event))            
    #-- Wconfig.on_treeCommands_key_press_event }


class Wcluster(SimpleGladeApp):
    COLOR = Gdk.RGBA(1.0, 0.99, 0.0) #FFFC00
    
    def __init__(self, path="gnome-connection-manager.glade",
                 root="wCluster",
                 domain=domain_name, terms=None, **kwargs):
        self.terms = terms
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

    #-- Wcluster.new {
    def new(self):        
        self.treeHosts = self.get_widget('treeHosts')
        self.treeStore = Gtk.TreeStore( GObject.TYPE_BOOLEAN, GObject.TYPE_STRING, GObject.TYPE_OBJECT )
        for x in self.terms:
            self.treeStore.append( None, (False, x[0], x[1]) )
        self.treeHosts.set_model( self.treeStore )               
        
        crt = Gtk.CellRendererToggle()
        crt.set_property('activatable', True)
        crt.connect('toggled', self.on_active_toggled)        
        col = Gtk.TreeViewColumn(_("Activar"), crt, active=0)               
        self.treeHosts.append_column( col )
        self.treeHosts.append_column(Gtk.TreeViewColumn(_("Host"), Gtk.CellRendererText(), text=1 ))
        self.get_widget("txtCommands").history = []
    #-- Wcluster.new }

    #-- Wcluster custom methods {
    #   Write your own methods here
    
    def on_active_toggled(self, widget, path):          
        self.treeStore[path][0] = not self.treeStore[path][0]
        self.change_color(self.treeStore[path][2], self.treeStore[path][0])                

    def change_color(self, term, activate):
        obj = term.get_parent()
        if obj == None:
            return
        nb = obj.get_parent()
        if nb == None:
            return
        if activate:
            nb.get_tab_label(obj).change_color(Wcluster.COLOR)
        else:
            nb.get_tab_label(obj).restore_color()
            
    #-- Wcluster custom methods }

    #-- Wcluster.on_wCluster_destroy {
    def on_wCluster_destroy(self, widget, *args):
        self.on_btnNone_clicked(None)
    #-- Wcluster.on_wCluster_destroy }

    #-- Wcluster.on_cancelbutton2_clicked {
    def on_cancelbutton2_clicked(self, widget, *args):
        self.get_widget("wCluster").destroy()
    #-- Wcluster.on_cancelbutton2_clicked }

    #-- Wcluster.on_btnAll_clicked {
    def on_btnAll_clicked(self, widget, *args):
        for x in self.treeStore:
            x[0] = True
            self.change_color(x[2], x[0])
    #-- Wcluster.on_btnAll_clicked }

    #-- Wcluster.on_btnNone_clicked {
    def on_btnNone_clicked(self, widget, *args):
        for x in self.treeStore:
            x[0] = False
            self.change_color(x[2], x[0])
    #-- Wcluster.on_btnNone_clicked }

    #-- Wcluster.on_btnInvert_clicked {
    def on_btnInvert_clicked(self, widget, *args):
        for x in self.treeStore:
            x[0] = not x[0]
            self.change_color(x[2], x[0])
    #-- Wcluster.on_btnInvert_clicked }

    #-- Wcluster.on_txtCommands_key_press_event {
    def on_txtCommands_key_press_event(self, widget, event, *args):        
        if not event.state & Gtk.gdk.CONTROL_MASK and Gtk.gdk.keyval_name(event.keyval).upper() == 'RETURN':           
           buf = widget.get_buffer()
           text = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
           buf.set_text('')
           for x in self.treeStore:
               if x[0]:
                   x[2].feed_child(text + '\r')
           widget.history.append(text)
           widget.history_index = -1
           return True
        if event.state & Gtk.gdk.CONTROL_MASK and Gtk.gdk.keyval_name(event.keyval).upper() in ['UP','DOWN']:
            if len(widget.history) > 0:
                if Gtk.gdk.keyval_name(event.keyval).upper() == 'UP':
                    widget.history_index -= 1
                    if widget.history_index < -1:
                        widget.history_index = len(widget.history) - 1
                else:
                    widget.history_index += 1
                    if widget.history_index >= len(widget.history):
                        widget.history_index = -1                        
                widget.get_buffer().set_text(widget.history[widget.history_index] if widget.history_index>=0 else '')
    #-- Wcluster.on_txtCommands_key_press_event }


class NotebookTabLabel(Gtk.HBox):
    '''Notebook tab label with close button.
    '''
    def __init__(self, title, owner_, widget_, popup_):
        Gtk.HBox.__init__(self, False, 0)
        
        self.title = title
        self.owner = owner_
        self.eb = Gtk.EventBox()
        label = self.label = Gtk.Label()
        self.eb.connect('button-press-event', self.popupmenu, label)
        label.set_alignment(0.0, 0.5)
        label.set_text(title)
        self.eb.add(label)        
        self.pack_start(self.eb, expand=False, fill=False, padding=1 )        
        label.show()        
        self.eb.show()                
        close_image = Gtk.Image.new_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        result, image_w, image_h = Gtk.IconSize.lookup(Gtk.IconSize.MENU)

        #self.widget = widget_
        self.popup  = popup_  

        close_btn   = Gtk.Button()
        close_btn.set_relief(Gtk.ReliefStyle.NONE)
        close_btn.connect('clicked', self.on_close_tab, owner_)
        close_btn.set_size_request(image_w+7, image_h+6)
        close_btn.add(close_image)
        style = close_btn.get_style();
        self.eb2 = Gtk.EventBox()
        self.eb2.add(close_btn)        
        self.pack_start(self.eb2, expand=False,  fill=False, padding=1)
        self.eb2.show()
        close_btn.show_all()  
        self.is_active = True
        self.show()
        
    def change_color(self, color):
        self.eb.modify_bg(Gtk.STATE_ACTIVE, color)
        self.eb2.modify_bg(Gtk.STATE_ACTIVE, color)
        self.eb.modify_bg(Gtk.STATE_NORMAL, color)
        self.eb2.modify_bg(Gtk.STATE_NORMAL, color)
        
    def restore_color(self):
        bg = self.label.style.bg
        self.eb.modify_bg(Gtk.STATE_ACTIVE, bg[Gtk.STATE_ACTIVE])
        self.eb2.modify_bg(Gtk.STATE_ACTIVE, bg[Gtk.STATE_ACTIVE])
        self.eb.modify_bg(Gtk.STATE_NORMAL, bg[Gtk.STATE_NORMAL])
        self.eb2.modify_bg(Gtk.STATE_NORMAL, bg[Gtk.STATE_NORMAL])
        
    def on_close_tab(self, widget, notebook, *args):
        if conf.CONFIRM_ON_CLOSE_TAB and msgconfirm("%s [%s]?" % ( _("Cerrar consola"), self.label.get_text().strip()) ) != Gtk.RESPONSE_OK:
            return True
        
        self.close_tab(widget)

    def close_tab(self, widget):
        notebook = self.widget.get_parent()        
        page=notebook.page_num(self.widget)
        if page >= 0:
            notebook.is_closed = True
            notebook.remove_page(page)
            notebook.is_closed = False       
            self.widget.destroy()
        
    def mark_tab_as_closed(self):
        self.label.set_markup("<span color='darkgray' strikethrough='true'>%s</span>" % (self.label.get_text()))
        self.is_active = False
        if conf.AUTO_CLOSE_TAB != 0:
            if conf.AUTO_CLOSE_TAB == 2:
                terminal = self.widget.get_parent().get_nth_page(self.widget.get_parent().page_num(self.widget)).get_child()
                if terminal.get_child_exit_status() != 0:
                    return
            self.close_tab(self.widget)
            
    def mark_tab_as_active(self):
        self.label.set_markup("%s" % (self.label.get_text()))
        self.is_active = True
        
    def get_text(self):
        return self.label.get_text()

    def popupmenu(self, widget, event, label):
        if event.type == Gtk.gdk.BUTTON_PRESS and event.button == 3:    
            self.popup.label = self.label
            if self.is_active:
                self.popup.mnuReopen.hide()
            else:
                self.popup.mnuReopen.show()
            
            #enable or disable log checkbox according to terminal 
            self.popup.mnuLog.set_active( hasattr(self.widget.get_child(), "log_handler_id") and self.widget.get_child().log_handler_id != 0 )
            self.popup.popup( None, None, None, event.button, event.time)
            return True
        elif event.type == Gtk.gdk.BUTTON_PRESS and event.button == 2:    
            self.close_tab(self.widget)

class EntryDialog( Gtk.Dialog):
    def __init__(self, title, message, default_text='', modal=True, mask=False):
        Gtk.Dialog.__init__(self)
        self.set_title(title)
        self.connect("destroy", self.quit)
        self.connect("delete_event", self.quit)
        if modal:
            self.set_modal(True)
        box = Gtk.VBox(spacing=10)
        box.set_border_width(10)
        self.vbox.pack_start(box)
        box.show()
        if message:
            label = Gtk.Label(message)
            box.pack_start(label)
            label.show()
        self.entry = Gtk.Entry()
        self.entry.set_text(default_text)
        self.entry.set_visibility(not mask)
        box.pack_start(self.entry)
        self.entry.show()
        self.entry.grab_focus()
        button = Gtk.Button(stock=Gtk.STOCK_OK)
        button.connect("clicked", self.click)
        self.entry.connect("activate", self.click)
        button.set_flags(Gtk.CAN_DEFAULT)
        self.action_area.pack_start(button)
        button.show()
        button.grab_default()
        button = Gtk.Button(stock=Gtk.STOCK_CANCEL)
        button.connect("clicked", self.quit)
        button.set_flags(Gtk.CAN_DEFAULT)
        self.action_area.pack_start(button)
        button.show()
        self.ret = None

    def quit(self, w=None, event=None):
        self.hide()
        self.destroy()        

    def click(self, button):
        self.value = self.entry.get_text()        
        self.response(Gtk.RESPONSE_OK)



class CellTextView(Gtk.TextView, Gtk.CellEditable):

    __gtype_name__ = "CellTextView"

    __gproperties__ = {
            'editing-canceled': (bool, 'Editing cancelled', 'Editing was cancelled', False, GObject.ParamFlags.READWRITE),
        }
        
    def do_editing_done(self, *args):
        self.remove_widget()

    def do_remove_widget(self, *args):
        pass

    def do_start_editing(self, *args):
        pass

    def get_text(self):
        text_buffer = self.get_buffer()
        bounds = text_buffer.get_bounds()
        return text_buffer.get_text(*bounds)

    def set_text(self, text):
        self.get_buffer().set_text(text)


class MultilineCellRenderer(Gtk.CellRendererText):

    __gtype_name__ = "MultilineCellRenderer"

    def __init__(self):
        Gtk.CellRendererText.__init__(self)
        self._in_editor_menu = False

    def _on_editor_focus_out_event(self, editor, *args):
        if self._in_editor_menu: return
        editor.remove_widget()
        self.emit("editing-canceled")

    def _on_editor_key_press_event(self, editor, event):
        if event.state & (Gtk.gdk.SHIFT_MASK | Gtk.gdk.CONTROL_MASK): return
        if event.keyval in (Gtk.keysyms.Return, Gtk.keysyms.KP_Enter):
            editor.remove_widget()
            self.emit("edited", editor.get_data("path"), editor.get_text())
        elif event.keyval == Gtk.keysyms.Escape:
            editor.remove_widget()
            self.emit("editing-canceled")

    def _on_editor_populate_popup(self, editor, menu):
        self._in_editor_menu = True
        def on_menu_unmap(menu, self):
            self._in_editor_menu = False
        menu.connect("unmap", on_menu_unmap, self)

    def do_start_editing(self, event, widget, path, bg_area, cell_area, flags):
        editor = CellTextView()
        editor.modify_font(self.props.font_desc)
        editor.set_text(self.props.text)
        editor.set_size_request(cell_area.width, cell_area.height)
        editor.set_border_width(min(self.props.xpad, self.props.ypad))
        editor.set_data("path", path)
        editor.connect("focus-out-event", self._on_editor_focus_out_event)
        editor.connect("key-press-event", self._on_editor_key_press_event)
        editor.connect("populate-popup", self._on_editor_populate_popup)
        editor.show()
        return editor


from threading import Thread
class CheckUpdates(Thread):
    
    def __init__(self, p):
        Thread.__init__(self)
        self.parent = p
        
    def msg(self, text, parent):        
        self.msgBox = Gtk.MessageDialog(parent, Gtk.DIALOG_MODAL, Gtk.MESSAGE_ERROR, Gtk.BUTTONS_OK, text)
        self.msgBox.set_icon_from_file(ICON_PATH)
        self.msgBox.connect('response', self.on_clicked)
        self.msgBox.show_all()      
        return False
        
    def on_clicked(self, *args):
        self.msgBox.destroy()
    
    def run(self):            
        try:
            import urllib, socket        
            socket.setdefaulttimeout(5)
            web = urllib.urlopen('http://kuthulu.com/gcm/_current.html')
            if web.getcode()==200:
                new_version = web.readline().strip()
                if len(new_version)>0 and new_version != app_version:                                
                    self.tag = GObject.timeout_add(0, self.msg, "%s\n\nVERSION: %s" % (_("Hay una nueva version disponible en http://kuthulu.com/gcm/?module=download"), new_version), self.parent.get_widget("wMain"))
        except:            
            pass

#-- main {

def main():
    w_main = Wmain()
    w_main.run()

if __name__ == "__main__":
    main()

#-- main }

