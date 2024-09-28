import sys
import os
import random
import string
import json
import pyperclip
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QCheckBox,
    QMessageBox,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
)
import webbrowser  # Voor het openen van de GitHub-link

from cryptography.fernet import Fernet

# Functie om een sleutel te genereren
def generate_key():
    return Fernet.generate_key()

# Versleutel de tekst
def encrypt_password(key, password):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password.decode()

# Ontsleutel de tekst
def decrypt_password(key, encrypted_password):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password.encode())
    return decrypted_password.decode()


class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.key = self.load_key()
        self.initUI()

    def load_key(self):
        # Zorg ervoor dat de instance map bestaat
        key_path = os.path.join('instance', 'secret.key')
        if not os.path.exists('instance'):
            os.makedirs('instance')

        # Probeer de sleutel te laden of genereer een nieuwe als die niet bestaat
        if os.path.exists(key_path):
            with open(key_path, 'rb') as key_file:
                return key_file.read()
        else:
            key = generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(key)
            return key

    def initUI(self):
        self.setWindowTitle("Wachtwoord Generator")

        # Tab widget
        self.tabs = QTabWidget()
        
        # Layouts
        self.layout = QVBoxLayout()
        self.serviceLayout = QHBoxLayout()
        self.usernameLayout = QHBoxLayout()
        self.lengthLayout = QHBoxLayout()
        
        # Invoerveld voor service
        self.serviceLabel = QLabel("Service:")
        self.serviceLineEdit = QLineEdit()

        self.serviceLayout.addWidget(self.serviceLabel)
        self.serviceLayout.addWidget(self.serviceLineEdit)

        # Invoerveld voor gebruikersnaam
        self.usernameLabel = QLabel("Gebruikersnaam:")
        self.usernameLineEdit = QLineEdit()

        self.usernameLayout.addWidget(self.usernameLabel)
        self.usernameLayout.addWidget(self.usernameLineEdit)

        # Dropdown menu voor lengte
        self.lengthLabel = QLabel("Kies de lengte van het wachtwoord:")
        self.lengthComboBox = QComboBox()
        self.lengthComboBox.addItems([str(i) for i in range(6, 31)])  # Lengtes van 6 tot 30
        self.lengthComboBox.setCurrentText("12")  # Standaardwaarde

        self.lengthLayout.addWidget(self.lengthLabel)
        self.lengthLayout.addWidget(self.lengthComboBox)

        # Checkboxen voor opties
        self.lowercaseCheck = QCheckBox("Kleine letters")
        self.uppercaseCheck = QCheckBox("Hoofdletters")
        self.digitsCheck = QCheckBox("Cijfers")
        self.specialCheck = QCheckBox("Speciale tekens")

        self.lowercaseCheck.setChecked(True)  # Standaard aan
        self.uppercaseCheck.setChecked(True)  # Standaard aan

        # Knop om wachtwoord te genereren
        self.generateButton = QPushButton("Genereer Wachtwoord")
        self.generateButton.clicked.connect(self.generate_password)

        # Knop om te kopiëren
        self.copyButton = QPushButton("Kopieer naar klembord")
        self.copyButton.clicked.connect(self.copy_to_clipboard)

        # Knop om wachtwoorden te resetten
        self.resetButton = QPushButton("Reset Wachtwoorden")
        self.resetButton.clicked.connect(self.reset_passwords)

        # Lijn voor het gegenereerde wachtwoord
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setReadOnly(True)

        # Voeg alles toe aan de layout
        self.layout.addLayout(self.serviceLayout)
        self.layout.addLayout(self.usernameLayout)
        self.layout.addLayout(self.lengthLayout)
        self.layout.addWidget(self.lowercaseCheck)
        self.layout.addWidget(self.uppercaseCheck)
        self.layout.addWidget(self.digitsCheck)
        self.layout.addWidget(self.specialCheck)
        self.layout.addWidget(self.generateButton)
        self.layout.addWidget(self.copyButton)
        self.layout.addWidget(self.resetButton)  # Voeg reset knop toe
        self.layout.addWidget(self.passwordLineEdit)

        # Maak tab voor wachtwoord genereren
        self.generateTab = QWidget()
        self.generateTab.setLayout(self.layout)

        # Maak tab voor wachtwoorden weergeven
        self.viewTab = QWidget()
        self.viewLayout = QVBoxLayout()
        
        # Tabel voor wachtwoorden
        self.passwordTable = QTableWidget()
        self.passwordTable.setColumnCount(3)
        self.passwordTable.setHorizontalHeaderLabels(["Service", "Gebruikersnaam", "Wachtwoord"])
        
        self.refreshButton = QPushButton("Vernieuw Tabel")
        self.refreshButton.clicked.connect(self.load_passwords)

        self.viewLayout.addWidget(self.passwordTable)
        self.viewLayout.addWidget(self.refreshButton)
        self.viewTab.setLayout(self.viewLayout)

        # Voeg tabs toe
        self.tabs.addTab(self.generateTab, "Genereer Wachtwoord")
        self.tabs.addTab(self.viewTab, "Bekijk Wachtwoorden")

        # Knop voor GitHub
        self.githubButton = QPushButton("Bekijk op GitHub")
        self.githubButton.clicked.connect(self.open_github)

        # Voeg de knoppen voor GitHub toe aan de hoofdlayout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabs)
        mainLayout.addWidget(self.githubButton)  # Voeg GitHub knop toe
        self.setLayout(mainLayout)

        # Laad de wachtwoorden bij opstarten
        self.load_passwords()

    def generate_password(self):
        length = int(self.lengthComboBox.currentText())
        characters = ""

        if self.lowercaseCheck.isChecked():
            characters += string.ascii_lowercase
        if self.uppercaseCheck.isChecked():
            characters += string.ascii_uppercase
        if self.digitsCheck.isChecked():
            characters += string.digits
        if self.specialCheck.isChecked():
            characters += string.punctuation

        if characters:
            password = ''.join(random.choice(characters) for _ in range(length))
            self.passwordLineEdit.setText(password)
            self.save_password(password)

    def save_password(self, password):
        service = self.serviceLineEdit.text()
        username = self.usernameLineEdit.text()

        if service and username:
            encrypted_password = encrypt_password(self.key, password)
            data = {
                "service": service,
                "username": username,
                "password": encrypted_password
            }

            # Zorg ervoor dat de instance map bestaat
            file_path = os.path.join('instance', 'passwords.json')
            if not os.path.exists('instance'):
                os.makedirs('instance')

            # Laad bestaande gegevens of maak een nieuw bestand
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    try:
                        passwords = json.load(f)
                    except json.JSONDecodeError:
                        passwords = []
            else:
                passwords = []

            passwords.append(data)

            # Sla de gegevens op in het JSON-bestand
            with open(file_path, 'w') as f:
                json.dump(passwords, f, indent=4)

            self.show_confirmation("Wachtwoord is opgeslagen!")
            self.load_passwords()  # Vernieuw de tabel na opslaan
        else:
            self.show_confirmation("Voer zowel service als gebruikersnaam in.")

    def load_passwords(self):
        self.passwordTable.setRowCount(0)  # Leeg de tabel
        file_path = os.path.join('instance', 'passwords.json')

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    passwords = json.load(f)
                    for entry in passwords:
                        row_position = self.passwordTable.rowCount()
                        self.passwordTable.insertRow(row_position)
                        self.passwordTable.setItem(row_position, 0, QTableWidgetItem(entry['service']))
                        self.passwordTable.setItem(row_position, 1, QTableWidgetItem(entry['username']))
                        decrypted_password = decrypt_password(self.key, entry['password'])
                        self.passwordTable.setItem(row_position, 2, QTableWidgetItem(decrypted_password))
                except json.JSONDecodeError:
                    self.passwordTable.setRowCount(0)
        else:
            self.passwordTable.setRowCount(0)

    def copy_to_clipboard(self):
        password = self.passwordLineEdit.text()
        if password:
            pyperclip.copy(password)
            self.show_confirmation("Het wachtwoord is succesvol gekopieerd naar het klembord.")

    def reset_passwords(self):
        # Bevestiging vragen
        reply = QMessageBox.question(self, 'Bevestiging', 'Weet je zeker dat je alle wachtwoorden wilt resetten?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Verwijder het JSON-bestand en de sleutel
            file_path = os.path.join('instance', 'passwords.json')
            key_path = os.path.join('instance', 'secret.key')
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(key_path):
                os.remove(key_path)

            self.show_confirmation("Alle wachtwoorden zijn gereset!")
            self.load_passwords()  # Vernieuw de tabel na reset

    def show_confirmation(self, message):
        QMessageBox.information(self, "Bevestiging", message)

    def open_github(self):
        webbrowser.open("https://github.com/Nico-Darth")  # Open de GitHub-pagina

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.resize(500, 400)
    ex.show()
    sys.exit(app.exec_())
