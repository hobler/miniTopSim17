# miniTopSim
Project of the Seminar "Scientific Programming in Python" WS 2017/18.

Set $PYTHONPATH to find modules (assuming you are in the directory where this readme resides):
```bash
export PYTHONPATH="$(pwd)/code:$PYTHONPATH"
```

In diesem README finden Sie folgende Informationen:

    1. Allgemeine Hinweise
    2. Spezifizieren der Eingabeparameter
    3. Testen
    4. Hinweise zur Präsentation
    
    
----------------------
1. Allgemeine Hinweise
----------------------

- Benützen Sie ausschließlich die folgenden Verzeichnisse:

    code - für miniTopSim code (*.py Files) und die Parameterdatenbank (parameters.db)
    
    tables - für Tabellen (nur bei einigen Aufgaben)
    
    work/AufgabeXX_YYY - alle Files, die nur für Ihre Aufgabe von Bedeutung sind, insbesondere alle cfg-, srf- und png-Files, alle Tests und Plot-Skripts, die nur für Ihre Aufgabe relevant sind. XX bezeichnet die Nummer Ihrer Aufgabe, YYY einen erklärenden String (wird in der Aufgabenstellung angegeben).

- Sie können den Code jederzeit herunterladen (fetch bzw. pull). Uploaden (push) aber bitte erst NACH der Präsentation.

- Wir wollen anstreben, dass spätestens eine Woche nach der Präsentation (9:00) ein stabiler Code auf Github vorhanden ist. D.h. bei zweiwöchigem Abstand der Vorträge, dass sich ab einer Woche vor Ihrem Vortrag nichts mehr auf Github ändern sollte.

- Grundsätzlich nur getesteten, voll funktionsfähigen Code uploaden.

- Laden Sie die "abzugebenden Files" bis 9:00 am Tag Ihrer Präsentation auf TUWEL hoch.

- png- und srf-Files werden nicht versioniert, d.h. sie werden nicht ins Repository übertragen. Damit die srf-Files für Vergleichszwecke erhalten bleiben, kopieren Sie sie auf Files mit gleichem Namen aber Endung .srf_save, wenn Sie sicher sind, dass sich nichts mehr ändert.

Lesen Sie sorgfältig die Folien "Working with GitHub" aus Kapitel VI der Vorlesung. 


-------------------------------------
2. Spezifizieren der Eingabeparameter
-------------------------------------

Das Programm soll mit 

    python3 <path-to-project-directory>/code/miniTopSim.py beispiel.cfg

von Ihrem Arbeitsverzeichnis aus aufgerufen werden können, wobei beispiel.cfg durch Ihr cfg-File zu ersetzen ist. Wenn Sie PYTHONPATH richtig gesetzt haben, sollte das auch mit

    python3 miniTopSim.py beispiel.cfg

möglich sein. cfg-Files sind wie folgt formatiert:

    [SectionName1]
    ParameterName1 = Wert1
    ParameterName2 = Wert2
    ...
    [SectionName2]
    ParameterNameN+1 = WertN+1
    ParameterNameN+2 = WertN+2
    ...

ParameterNameI ist durch den Namen des Parameters zu ersetzen, WertI durch den Parameterwert. Die Parameter sind in Gruppen („Sections”) eingeteilt. 

Welche Parameter in welchen Sections einzuführen sind, ist in den einzelnen Aufgaben angegeben. "Einführen" heißt für Sie, dass Sie einen Eintrag in der Parameter-Datenbank (parameters.db Datei im IO Verzeichnis) vornehmen. Die Parameter-Datenbank ist ein Textfile in folgendem Format:

    [SectionName1]
    ParameterName1 = (DefaultWert1, 'Bedingung1', '''Erklärung1''')
    ParameterName2 = (DefaultWert2, 'Bedingung2', '''Erklärung2''')
    ...
    [SectionName2]
    ParameterNameN+1 = (DefaultWertN+1, 'BedingungN+1', '''ErklärungN+1''')
    ParameterNameN+2 = (DefaultWertN+2, 'BedingungN+2', '''ErklärungN+2''')
    ...

Für jeden Parameter sind in einem Tupel der Defaultwert, eine Bedingung und eine Erklärung angegeben. Der Defaultwert kann auch ein Datentyp sein, dann ist der Parameter obligatorisch im cfg-File anzugeben. Die Bedingung kann auch None sein, dann wird keine Bedingung überprüft. Ansonsten ist die Bedingung ein gültiger boolscher Python-Ausdruck, in einem String gespeichert. Er kann denselben oder andere Parameternamen (in Großbuchstaben) als Variablen enthalten. Die Erklärung ist ein String, der (bei Verwendung von Triple-Quotes) auch über mehrere Zeilen laufen kann. Wann immer ein neuer Parameter eingeführt wird, muss also auch ein Eintrag in der Parameter-Datenbank erfolgen.

Im Programm werden die Parameter über das parameters Modul (Datei parameters.py) des IO Pakets zur Verfügung gestellt. Dieses wird mit

    import parameters as par

importiert. Die Parameter stehen als Modulvariablen des parameters Modul zur Verfügung, d.h. sie können unter den Namen par.ParameterNameI (ParameterNameI entsprechend ersetzen) angesprochen werden.


---------
3. Testen
---------

Für das Testen verwenden wir Pytest. ACHTUNG: Es gibt ein altes Tool gleichen Namens, das auf einigen Linux-Distributionen noch installiert ist. Falls Sie nicht die Anaconda-Distribution verwenden, vergewissern Sie sich, dass Sie mit dem richtigen Tool arbeiten.

Ihre Tests sollen sowohl vom Arbeitsverzeichnis aus aufgerufen laufen (solange Sie daran arbeiten), als auch vom miniTopSim-Verzeichnis (mit "pytest" laufen dann alle Tests des Projekts). Damit die Tests den miniTopSim-Code importieren können, auch wenn PYTHONPATH nicht als Umgebungsvariable gesetzt ist, fügen Sie am Beginn Ihrer Tests folgende Zeilen ein:

    import os, sys
    filedir = os.path.dirname(__file__)
    codedir = os.path.join(filedir, '..', ’..’, ’code’)
    sys.path.insert(0, codedir)

Tests müssen ein assert Statement enthalten (siehe Vortragsfolien).

Wenn nichts anderes angegeben ist, besteht ein Test aus einer Simulation, die ein srf-File erzeugt. Die letzte Oberfläche soll auf "geringen Abstand" von der letzten Oberfläche des entsprechenden srf_save-Files überprüft werden. Letzteres wird durch Kopieren des srf-Files einer vorangegangenen Simulation erzeugt. Die in den Angaben verlangten Tests stellen ein Minimum dar. Sie können auch weitere Tests definieren. Achten Sie aber darauf, dass diese kurz (bezüglich Rechenzeit) sind.


----------------------------
4. Hinweise zur Präsentation
----------------------------

Sie sollen Ihre Arbeit in einem ca. 10-15-minütigen Vortrag präsentieren. Halten Sie den Vortrag in erster Linie für Ihre Kollegen und berücksichtigen Sie deren Wissensstand. Ihr Vortrag soll die Aufgabenstellung darlegen, den Code präsentieren und die Ergebnisse der Tests und/oder Simulationen beschreiben. Sie können dazu mehrere Hilfsmittel verwenden, Powerpoint-Präsentation, Spyder, Editor. Sie können Ihren Laptop verwenden oder Ihre Files auf einem USB-Stick mitbringen. Unser Rechner hat Powerpoint und Spyder installiert. Kurze Rechnungen können Sie online laufen lassen, bei längeren wird es angebracht sein, die Ergebnisse vorzubereiten.

Damit Ihr Code "präsentierbar" ist, schreiben Sie möglichst übersichtlichen Code. Kommentare sollten hauptsächlich im doc-String am Beginn eines Moduls, einer Klasse bzw. einer Funktion stehen; im Code höchstens Einzeiler oder am Zeilenende.

