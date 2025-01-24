# TicTacToe
Programa Kryžiukai-nuliukai skirta žaisti lentoi, kurios konfigūracija nuo 3*3 iki 12*12.
Yra dvi žaidimo versijos – tik su tekstine sąsaja, įvedant judesį 'i-j' formatu. 
Pažymėtų laukų išvedimas į žurnalą spausdinant. Sėkmės balas nustatomas pagal matematinį
algoritmą. Iš įvesto taško tikriname, ar nėra artimos kaimynystės ir jos kryptis.
Visi įvesti taškai įtraukiami į bendrą žurnalą, taškų žodyną.Jei algoritmas randa kaimynus
su tuo pačiu ženklu X arba 0, jie įrašomi į atitinkamus žurnalus lineX arba line0
ir tikrinamas šių taškų buvimas kaimynystės vektoriaus kryptimi. Vykdomas titato_text_best.py
Grafinės sąsajos versijai buvo naudojama PyQt5 biblioteka, o darbui su grafika buvo
naudojamas PIL paketas. Žaidimo lauko dydžio ir laimėjimo srities ilgio pasirinkimas
naudojant du slinkties langelius.Teksto įvesties lange įveskite judėjimą i-j ir
paspauskite Enter. Mažame ekrane rodoma, kas vaikšto: kryžiai ar kojų pirštai, 
priminimas. Atliktas judesys dideliame ekrane rodomas grafine forma – atsiprašau, 
nelabai tvarkingai, bet du grafinius failus labai paprasta pakeisti kryželiu arba
nuliu. Pergalė nustatoma pagal laimėjimo ilgį žurnale, o rezultatas rodomas spausdinimo
komanda.
