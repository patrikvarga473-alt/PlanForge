# PlanForge

Moderná tréningová web appka vytvorená kompletne v Pythone cez Streamlit.

## Spustenie vo Windows

1. Rozbaľ priečinok.
2. Otvor CMD alebo PowerShell v priečinku aplikácie.
3. Nainštaluj závislosti:

   pip install -r requirements.txt

4. Spusti aplikáciu:

   streamlit run app.py

Prehliadač sa otvorí automaticky.

## Čo už funguje

- tmavý moderný fitness dizajn
- lokálny fitness hero obrázok
- profil: pohlavie, vek, výška a váha
- výber cieľa, úrovne, dní a vybavenia
- vynechanie celých svalových partií
- zakázanie nechcených cvikov
- automatický výber splitu
- jemná personalizácia výberu cvikov podľa profilu
- miernejší objem pre začiatočníkov a starších cvičencov
- série, opakovania a pauzy
- cviky zoskupené po svalových partiách; každá partia ide kompletne za sebou
- technika a nastavenie cviku
- výmena cviku za vhodnú alternatívu
- nový variant plánu

## Ďalšie logické vylepšenia

- prihlasovanie a ukladanie používateľov
- progres tréningov
- zapisovanie váh a opakovaní
- export do PDF
- obrázky alebo videá ku každému cviku
- platený premium účet

## Týždenný progres

- trvalé lokálne ukladanie cez SQLite
- Týždeň 1, Týždeň 2 a ďalšie zápisy
- priemerná týždenná váha a voliteľný obvod pása
- počet odcvičených tréningov
- hodnotenie výkonu a regenerácie
- graf vývoja váhy
- rozpoznanie chudnutia, naberania a stagnácie
- bezpečné úpravy tréningu podľa trendu
