import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QCheckBox, QPushButton
from PyQt5.QtCore import Qt, QTimer

class Finestra(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Esempio PyQt5")
        self.resize(400, 300)

        # Layout verticale
        layout = QVBoxLayout()

        # Etichetta per mostrare il valore dello slider + bottone
        # Layout orizzontale per password e bottone copia
        layout_riga = QHBoxLayout()
        self.label = QLabel("Password:")
        layout_riga.addWidget(self.label)

        self.bottone_copia = QPushButton("Copia")
        self.bottone_copia.setMinimumWidth(80)  
        self.bottone_copia.setMaximumWidth(80) # puoi cambiare la larghezza
        self.bottone_copia.clicked.connect(self.copia_password)
        layout_riga.addWidget(self.bottone_copia)
        layout.addLayout(layout_riga)

        self.label1 = QLabel("Numero caratteri: 10")
        layout.addWidget(self.label1)
        

        # Slider (da 7 a 32)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(7)
        self.slider.setMaximum(32)
        self.slider.setValue(10)  # valore iniziale
        self.slider.valueChanged.connect(self.aggiorna_testo)
        layout.addWidget(self.slider)

        # Checkbox 1
        self.check_maiuscole = QCheckBox("Maiuscole (A-Z)")
        self.check_maiuscole.setChecked(False)  # attiva di default
        self.check_maiuscole.stateChanged.connect(self.aggiorna_testo)
        layout.addWidget(self.check_maiuscole)

        # Checkbox 2
        self.check_numeri = QCheckBox("Numeri (0-9)")
        self.check_numeri.setChecked(False)
        self.check_numeri.stateChanged.connect(self.aggiorna_testo)
        layout.addWidget(self.check_numeri)


         # Checkbox 3
        self.check_carspec = QCheckBox("Caratteri speciali (!, @, #, ...)")
        self.check_carspec.setChecked(False)
        self.check_carspec.stateChanged.connect(self.aggiorna_testo)
        layout.addWidget(self.check_carspec)
        self.setLayout(layout)

    def aggiorna_testo(self):
        lunghezza = self.slider.value()
        caratteri = list("abcdefghijklmnopqrstuvwxyz")
        speciali = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+"]
        x=0
        psw=""
        while x<lunghezza:
            psw += str(random.choice(caratteri))
            x+=1

        if self.check_maiuscole.isChecked():
            num = random.randint(int(lunghezza/4), int(lunghezza/2.5))
            while num>0:
                pos = random.randint(0, lunghezza-1)
                pswlist = list(psw)
                pswlist[pos] = pswlist[pos].upper()
                psw = "".join(pswlist)
                num-=1

        if self.check_numeri.isChecked():
            num = random.randint(int(lunghezza/5), int(lunghezza/3))
            while num>0:
                pos = random.randint(0, lunghezza-1)
                pswlist = list(psw)
                pswlist[pos] = str(random.randint(0, 9))
                psw = "".join(pswlist)
                num-=1
        
        if self.check_carspec.isChecked():
            num = random.randint(int(lunghezza/5), int(lunghezza/3))
            while num>0:
                pos = random.randint(0, lunghezza-1)
                pswlist = list(psw)
                pswlist[pos] = random.choice(speciali)
                psw = "".join(pswlist)
                num-=1

        apposto = self.verifica(psw)
        if apposto == False:
            self.aggiorna_testo()
            return
        
        self.label.setText(f"Password: {psw}")
        self.label1.setText(f"Numero caratteri: {lunghezza}")

    def verifica(self, psw):
        apposto = True
        #if any(c.islower() for c in psw):

            
        if self.check_maiuscole.isChecked() == True:
                if any(c.isupper() for c in psw)==False:
                    return False
            
        if self.check_numeri.isChecked() == True:
            if any(c.isdigit() for c in psw)==False:
               return False
            
        if self.check_carspec.isChecked() == True:
            if any(c in "!@#$%^&*()-_=+" for c in psw)==False:
                return False    
            
        return apposto
    
    def copia_password(self, psw):
        clipboard = QApplication.clipboard()
        password = self.label.text().replace("Password: ", "")
        clipboard.setText(password)
        self.bottone_copia.setText("Copiato!")
        #copiata malamente da internet perché non sapevo come fare per fargli aspettare un secondo (con arduino è molto più facile)
        QTimer.singleShot(1000, lambda: self.bottone_copia.setText("Copia"))
       


# Avvio applicazione
app = QApplication(sys.argv)
finestra = Finestra()
finestra.show()
sys.exit(app.exec_())