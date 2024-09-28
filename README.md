# Wachtwoord Generator

Dit is een eenvoudige wachtwoordgenerator geschreven in Python met behulp van PyQt5. Het programma biedt een gebruikersvriendelijke interface voor het genereren en beheren van veilige wachtwoorden. De gegenereerde wachtwoorden kunnen worden versleuteld en opgeslagen in een JSON-bestand, en er is ook een functie om alle wachtwoorden te resetten.

## Functionaliteiten

- **Wachtwoordgeneratie**: Genereer sterke wachtwoorden met behulp van kleine letters, hoofdletters, cijfers en speciale tekens.
- **Opslag van wachtwoorden**: Sla gegenereerde wachtwoorden op met bijbehorende service en gebruikersnaam in een JSON-bestand.
- **Versleuteling**: Wachtwoorden worden versleuteld met AES (met de `cryptography` bibliotheek) voordat ze worden opgeslagen.
- **Wachtwoorden bekijken**: Bekijk opgeslagen wachtwoorden in een tabelvormige interface.
- **Wachtwoorden resetten**: Verwijder alle opgeslagen wachtwoorden met een bevestigingsdialoog.
- **Kopiëren naar klembord**: Kopieer het gegenereerde wachtwoord eenvoudig naar het klembord.
- **GitHub Koppeling**: Ga naar de GitHub-pagina van de ontwikkelaar voor meer informatie.

## Vereisten

Zorg ervoor dat je de volgende pakketten geïnstalleerd hebt:

- `PyQt5`
- `cryptography`
- `pyperclip`

Je kunt deze installeren met pip:

```bash
pip install PyQt5 cryptography pyperclip
```

## Gebruik

1. **Voer de service en gebruikersnaam in**: Vul het invoerveld in met de naam van de service waarvoor je een wachtwoord wilt genereren en de bijbehorende gebruikersnaam.

2. **Kies de lengte van het wachtwoord**: Selecteer de gewenste lengte van het wachtwoord uit de dropdown.

3. **Selecteer opties**: Vink de vakjes aan voor kleine letters, hoofdletters, cijfers en speciale tekens om op te nemen in het wachtwoord.

4. **Genereer het wachtwoord**: Klik op de knop "Genereer Wachtwoord" om een nieuw wachtwoord te genereren.

5. **Opslaan**: Het gegenereerde wachtwoord wordt automatisch versleuteld en opgeslagen in een JSON-bestand in de `instance`-map, samen met de ingevoerde service en gebruikersnaam.

6. **Bekijk opgeslagen wachtwoorden**: Navigeer naar het tabblad "Bekijk Wachtwoorden" om een lijst van opgeslagen wachtwoorden te bekijken.

7. **Resetten**: Klik op de knop "Reset Wachtwoorden" om alle opgeslagen wachtwoorden te verwijderen. Je krijgt een bevestiging voordat de actie wordt uitgevoerd.

8. **Kopiëren**: Klik op de knop "Kopieer naar klembord" om het huidige wachtwoord te kopiëren naar je klembord.

9. **GitHub**: Klik op de knop "Bekijk op GitHub" om de GitHub-pagina van de ontwikkelaar te openen.


## Bestanden

- **`password-generator.py`**: Het hoofdscript voor de wachtwoordgenerator.
- **`instance/`**: Map waarin de versleutelde wachtwoorden en de sleutel worden opgeslagen.
- **`README.md`**: Deze documentatie.
- **`password-generator.exe`**: Het uitvoerbare bestand voor de wachtwoordgenerator, te gebruiken als je geen Python geïnstalleerd hebt.




## Probleemoplossing

Als je problemen ondervindt bij het uitvoeren van het Python-script of als je geen Python op je systeem hebt geïnstalleerd, kun je het `.exe`-bestand gebruiken dat is gemaakt met PyInstaller.

### Hoe de `.exe` uit te voeren

1. **Download de `.exe`**: Zorg ervoor dat je het `password-generator.exe`-bestand hebt gedownload. Dit bestand is beschikbaar in de `root-directory`. na het uitvoeren van PyInstaller.
  
2. **Voer de `.exe` uit**: Dubbelklik op het `password-generator.exe`-bestand om het programma te starten.

3. **Zorg voor benodigde bestanden**: Controleer of de `instance`-map aanwezig is in dezelfde directory als het `.exe`-bestand, zodat het programma correct kan functioneren.

### Opmerking

Dit `.exe`-bestand is een zelfstandige applicatie en vereist geen Python-installatie of andere afhankelijkheden op je systeem. Het kan direct worden uitgevoerd op Windows-systemen.
