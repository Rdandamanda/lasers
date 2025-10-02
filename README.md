# Simulace 2D paprskové optiky
#### Hlavní cíl: Offline desktopová aplikace v Pythonu s grafickým rozhraním pro simulaci 2D paprskové optiky pro výuku
#### Rozepsané cíle:
- **Simulace paprskové optiky**
  - Chování paprsku podle zákona odrazu a Snellova zákona o lomu paprsku
  - Optické prvky: Obdélník ze skla, hranol, zrcadlo, spojná čočka a rozptylka, obdélníková překážka blokující světlo, zdroj paprsku
  - Materiály podporující odražení části paprsku a průchod zbytku paprsku materiálem
  - Index lomu některých materiálů je měnitelný pomocí GUI, není pevně daný
- **GUI napsané v Tkinteru**
  - Přidávání, přesouvání, nastavování, mazání prvků simulace
  - Scrollovatelná pracovní plocha, kde uživatel připraví zadání a program vykreslí cestu paprsku
  - Přesouvání prvků myší stylem "Drag 'n drop"
  - Lišta nástrojů inspirovaná jinými desktopovými programy (tlačítka pro uložení a načtení souboru a pro přidávání prvků na pracovní plochu)
  - Možnost mít víc pracovních ploch najednou a switchovat mezi nimi pomocí ttk.Notebook widgetu
- **Ukládání do souborů, načítání ze souborů**
  - Zadání simulace lze uložit do souboru a jindy z něj znovu načíst
  - Defaultní předem vytvořené demo soubory, které lze načíst a předvádět na nich, co program umí
- **Využití OOP**
  - Kód bude navržený objektově tak, aby šlo naprogramovat nové objekty založené na těch existujících a integrovat je do zbytku programu (bez nutnosti přepsat celý simulační a renderovací engine)

> Doplňující informace k tomu, jak plánuji některé části řešit, jsou dostupné v mých veřejných poznámkách na [GitHub Projects](https://github.com/users/Rdandamanda/projects/1/views/1). Jsou to pouze orientační poznámky, co jsem si napsal před začátkem práce. Závazné zadání je obsaženo výhradně v tomto souboru

### Předběžný časový plán projektu:
- Do 31. 10.: Vytvoření OOP struktury. Základ simulace - zdroj paprsku, cesta paprsku prostorem a jeho interakce s jednoduššími prvky: skleněný obdélník, zrcadlo, obdélníková překážka. Renderování paprsku na obrazovku. Simulace je zatím nastavena staticky v kódu a GUI v tuto chvíli slouží pouze k zobrazení výsledku.
- Do 24. 11.: GUI - Přidávání prvků na plochu pomocí GUI, možnost je myší vybírat, přesouvat a upravovat jejich vlastnosti (pokud nějaké mají)
- Do 31. 12.: Dodělání chybějících věcí: Ukládání do souboru, načítání ze souboru. Zbylé prvky - čočky a hranol. Scrollování plochy, vyladění zobrazování. Odstranění případných problémů s GUI a jeho celkové doladění
- Po 31. 12. 2025: Testování aplikace a odstranění nalezených chyb. V případě časové rezervy rozšíření programu o doplňkové funkce a vytvoření ukázkových demo scénářů

### Předběžný časový plán dokumentace:
- Do 26. 1.: Vytvoření kostry dokumentace s minimálně polovinou plánovaného obsahu. V této fázi nebude kladen důraz na stylistiku a vizuální zpracování
- Do 1. 3.: Dokumentace hotová, konzultace posledních stylistických úprav

> Zadání sepsáno 1. 10. 2025
> 
> Upraveno 2. 10. 2025
