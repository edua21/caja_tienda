from wx import *
from wx.dataview import *
from wx.adv import *
import sqlite3
from sqlalchemy import *
from datetime import date

class MyApp(App):
    def OnInit(self):
        self.op = "a"
        f = Frame(None, title="Te va gustar", size=(1100,600))
        p = self.p = Panel(f, -1)
        p.SetBackgroundColour((255,51,202))
        self.dvlc = dvlc = DataViewListCtrl(p)
        dvlc.SetBackgroundColour((255,51,202))
        dvlc.AppendTextColumn('#', width=30)
        dvlc.AppendTextColumn('Apellido y nombres', width=150)
        dvlc.AppendTextColumn('Fecha', width=100)
        dvlc.AppendTextColumn('Retira', width=100)
        dvlc.AppendTextColumn('Entrega', width=100)
        dvlc.AppendTextColumn('Forma de pago', width=100)
        dvlc.AppendTextColumn('Saldo', width=100)
        dvlc.AppendTextColumn('Telefono', width=100)
        dvlc.AppendTextColumn('Dirección', width=250)
        hor = BoxSizer(HORIZONTAL)
        b = Button(p, -1, "&Agregar persona")
        b.SetBackgroundColour((255,51,202))
        self.search = search = SearchCtrl(self.p)
        search.ShowCancelButton(True)
        relleno = StaticText(self.p) #El relleno espara qe el botòn Buscar se ubique en el lado opuesto del botòn Agregar
        hor.Add(b, 1)
        hor.Add(relleno, 7)
        hor.Add(search, 1)
        sizer = BoxSizer(VERTICAL)
        sizer.Add(dvlc, 1, EXPAND)
        b.Bind(EVT_BUTTON, self.abrirAgP)
        sizer.Add(hor)
        p.SetSizer(sizer)
        lista = self.recupBD()
        self.search.Bind(EVT_TEXT, self.buscar)
        for e in lista:
            self.dvlc.AppendItem(e)        
        f.Show()
        dvlc.Bind(EVT_DATAVIEW_SELECTION_CHANGED, self.sele)
        return True

    def sele(self, e):#Llamo a la función abrir con el click del mouse
        self.op = "m"
        self.abrirAgP(e)
        self.op = "a"




    def recupBD(self):#Funcion para recuperar los datos 
        con = sqlite3.connect("caja.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM datos ORDER BY nombre")
        tuplas = cur.fetchall()
        listaA = [list(e) for e in tuplas]
        for e in listaA:
            e[0] = str(e[0])#convirto los campos enteros en string
            e[3] = str(e[3])
            e[4] = str(e[4])
            e[6] = str(e[6])
        con.close()
        return listaA


    ## Comienza funcion Buscar personas 

    def buscar(self, event):
        lista = self.recupBD()
        print("--------------------------")
        busco = self.search.GetValue()
        num = self.search.GetLastPosition()
        tot = self.dvlc.GetItemCount()
        for i in range(tot):
            self.dvlc.DeleteItem(0)

        for i in range(len(lista)):
            if busco == lista[i][1][:num]:
                self.dvlc.AppendItem(lista[i])
                print("#", lista[i][1])

## Termina funcion Buscar 

    def abrirAgP(self, e):
        self.f2 = f2 = Frame(None, -1, "Agregar persona", size = (350, 300))
        p2 = self.p2 = Panel(f2, -1, style = TAB_TRAVERSAL)
        p2.SetBackgroundColour((255,51,202))
        grilla = GridBagSizer(5,5)
        

# Nombre - Caja de Texto
        l_nom = StaticText(p2, -1, "Apellido y nombres")
        grilla.Add(l_nom, pos = (0,0))
        nom = self.nom =TextCtrl(p2, -1)
        if self.op == "m":
            nom.SetLabel(self.recupDV(1))
        grilla.Add(nom, pos = (0,1), span = (1, 3))
# Fecha - Caja de Texto con fecha de hoy - Abre datepicker
        l_fna = StaticText(p2, -1, "Fecha")
        grilla.Add(l_fna, pos = (1,0))
        self.fe = date.today().isoformat()# Si no hay cambio de fecha le asigna directamente la fecha de
        fna =self.fna = DatePickerCtrl(p2, size=(120, -1), style= DP_DROPDOWN | DP_SHOWCENTURY)
        fna.Bind(EVT_DATE_CHANGED, self.OnDateChanged, fna) # este evento es para cuando NO ES BOTON
        grilla.Add(self.fna, pos = (1,1), span = (1, 3))
# Retira - Caja de texto
        l_ret = StaticText(p2, -1, "Retira")
        grilla.Add(l_ret, pos = (2,0))
        ret = self.ret = TextCtrl(p2, -1)
        grilla.Add(ret, pos=(2,1), span = (1, 3))
        ret.Bind(EVT_KILL_FOCUS, self.poneSaldo)
# Entrega - Caja de texto
        l_ent = StaticText(p2, -1, "Entrega")
        grilla.Add(l_ent, pos = (3,0))
        ent = self.ent =TextCtrl(p2, -1)
        ent.Bind(EVT_KILL_FOCUS, self.calculaSaldo)
        grilla.Add(ent, pos = (3,1), span = (1, 3))
# Forma de pago - Combo
        l_fpag = StaticText(p2, -1, "Forma de pago")
        grilla.Add(l_fpag, pos = (4,0))
        fpagList = ["Efectivo", "Tarjeta debito", "Tarjeta credito", "Solo retira"]
        self.fpag = cb = ComboBox(p2, 500, "Forma de pago", (0, 0), (160, -1), fpagList, CB_DROPDOWN | TE_PROCESS_ENTER )
        cb.Bind(EVT_KILL_FOCUS, self.OnKillFocus)
        grilla.Add(self.fpag, pos = (4,1), span = (1, 3))
# Saldo - Caja de Texto
        l_sal = StaticText(p2, -1, "Saldo")
        grilla.Add(l_sal, pos=(5,0))
        sal = self.sal = TextCtrl(p2, -1)
        sal.SetLabel("0")
        if self.op == "m":
            sal.SetLabel(self.recupDV(6))
        grilla.Add(sal, pos=(5,1), span = (1, 3))
# Telefono - Caja de Texto
        l_tel = StaticText(p2, -1, "Telefono")
        grilla.Add(l_tel, pos=(6,0))
        tel = self.tel = TextCtrl(p2, -1)
        if self.op == "m": # En esta dos lineas obtengo del dataview los datos del campo marcado y los reflejo en la segunda ventana, con los datos ya cargados
            tel.SetLabel(self.recupDV(7))
        grilla.Add(tel, pos=(6,1), span = (1, 3))
# Direccion - Caja de texto
        l_dire = StaticText(p2, -1, "Dirección")
        grilla.Add(l_dire, pos = (7,0))
        dire = self.dire =TextCtrl(p2, -1)
        if self.op == "m":  
            dire.SetLabel(self.recupDV(8))
        grilla.Add(dire, pos = (7,1), span = (1, 3))
# Botón Guardar
        guardar = Button(p2, -1, "&Guardar")
        grilla.Add(guardar, pos = (8, 0))
        guardar.Bind(EVT_BUTTON, self.guardaPart)

# Muestra la grilla
        p2.SetSizerAndFit(grilla)
        f2.Show()

    def poneSaldo(self, event):
        s = int(self.sal.GetValue())
        e = int(self.ret.GetValue())
        ns = str(s+e)
        self.sal.SetLabel(ns)

    def calculaSaldo(self, event):
        s = int(self.sal.GetValue())
        e = int(self.ent.GetValue())
        ns = str(s-e)
        self.sal.SetLabel(ns)


    def recupDV(self, campo):#Función de recuperar datos en la base
        row = self.dvlc.GetSelectedRow()
        return self.dvlc.GetTextValue(row, campo)

#Guarda el participante
    def guardaPart(self, evt):
        no = self.nom.GetValue()
        fn = self.fna.GetValue()
        re = self.ret.GetValue()
        en = self.ent.GetValue()
        fp = self.fp = self.fpag.GetValue()
        sa = self.sal.GetValue()
        te = self.tel.GetValue()
        di = self.dire.GetValue()
        self.dvlc.AppendItem(["0", no, self.fe, re, en, fp, sa, te, di]) 
        print(self.fe)       
        self.grabaBD(no, self.fe, re, en, fp, sa, te, di)
        self.f2.Close()

# Begin Combo
    def OnKillFocus(self, evt):
        self.fp = self.fpag.GetValue()
        evt.Skip()
# End Combo

# Begin Calendario
    def OnDateChanged(self, evt):
        print("OnDateChanged: %s\n" % evt.GetDate())
        d = evt.GetDate()
        print(d.FormatISODate())
        self.fe = d.FormatISODate()
        print("->", self.fe, "<-")
# End Calendario
    def grabaBD(self, pnombre, pfecha, pretira, pentrega, pformadepago, psaldo, ptelefono, pdireccion):#Graba en la base de datos
        
        engine = create_engine('sqlite:///caja.db')
        conn = engine.connect()
        metadata = MetaData()

        datos = Table('datos', metadata, 
                Column('id', Integer(), primary_key=True),
                Column('nombre', String(50)),
                Column('fecha', String(50)),
                Column('retira', Integer()),
                Column('entrega', Integer()),
                Column('formadepago', String(20)),
                    Column('saldo', Integer()),
                Column('telefono', String(50)),
                Column('direccion', String(50))
        )

        t = conn.begin()
        ins = datos.insert().values(
                nombre = pnombre,
                fecha = pfecha,
                retira = pretira,
                entrega = pentrega,
                formadepago = pformadepago,
                saldo = psaldo,
                telefono = ptelefono,
                direccion = pdireccion      
        )

        conn.execute(ins) 
        t.commit()
                



app = MyApp()
app.MainLoop()
