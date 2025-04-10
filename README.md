# Projekt 9 – Implementacija igre Iterativna zapornikova dilema

## Definicija problema

V tej nalogi se ukvarjamo z implementacijo igre "Iterativna zapornikova dilema". Osnovni problem izhaja iz realnega sveta, kjer se posamezniki soočajo z dilemami med sodelovanjem in izdajo, vendar je koncept igre umetno ustvarjen za simulacijo medsebojnega sodelovanja v več ponovljenih interakcijah. Igra temelji na matematični formulaciji, kjer je cilj vsakega agenta maksimizirati svojo korist. Matematično je možno definirati korist agenta \(i\) kot:

$$
U_i = \sum_{t=1}^{T} u_i(t)
$$

kjer je:

- $U_i$ skupna korist agenta $i$,
- $T$ število iteracij igre,
- $u_i(t)$ korist, ki jo agent $i$ doseže v $t$-ti iteraciji.

Problem se dotika ključnih vprašanj strategij odločanja in merjenja učinkovitosti različnih pristopov pri iterativni igri.  
**Ključne besede:** iterativna zapornikova dilema, strategije, sodelovanje, evalvacija, Axelrod

## Pregled sorodnih del in pregled evaluacije rešitve problema

Pregled literature kaže, da so raziskovalci že dolgo preučujejo dileme med sodelovanjem in izdajo. Pomembni viri vključujejo:

- [M. Jurišić, D. Kermek and M. Konecki, "A review of iterated prisoner's dilemma strategies," 2012 Proceedings of the 35th International Convention MIPRO, Opatija, Croatia, 2012, pp. 1093-1097. keywords: {Thin film transistors;Games;Educational institutions;Noise;Game theory;Economics;Biological system modeling}](https://ieeexplore.ieee.org/abstract/document/6240806)
- [Wikipedia: The Evolution of Cooperation](https://en.wikipedia.org/wiki/The_Evolution_of_Cooperation)
- [William H. Press, and Freeman J. Dysonb: "Iterated Prisoner’s Dilemma contains strategies that dominate any evolutionary opponent"](https://www.pnas.org/doi/epdf/10.1073/pnas.1206569109)
- [Bravetti, A., Padilla, P. An optimal strategy to solve the Prisoner’s Dilemma. Sci Rep 8, 1948 (2018).](https://www.nature.com/articles/s41598-018-20426-w)

Evaluacija rešitev v tem področju se pogosto izvaja z naslednjimi metodami:

- **Simulacijska analiza:** Izvajanje večkratnih iteracij igre in primerjava povprečne koristi različnih strategij.
- **Analiza stabilnosti:** Preučevanje, katera strategija dosega stabilno ravnovesje (npr. Nashovo ravnovesje - Nash Equilibrium) v iterativni igri.
- **Statistična primerjava:** Uporaba statističnih metod za primerjavo rezultatov turnirjev med različnimi strategijami.
- **Eksperimentalna validacija:** Izvajanje eksperimentov s simulacijami turnirja, kot ga je predlagal Axelrod, in preverjanje hipoteze o prednosti sodelovanja pri večkratnem ponavljanju igre.

## Strategije v igri Prisoner's Dilemma

V igri Prisoner's Dilemma igralci ponavljajo dilemo zapornikov in sprejemajo odločitve o sodelovanju ali izdaji. Različne strategije določajo, kako igralec sprejema odločitve glede na prejšnje poteze nasprotnika. Spodaj so opisane strategije, katere bomo implementirali:

### Tit for Tat (Tit4Tat)

- Strategija začne s sodelovanjem.
- Nato ponavlja potezo nasprotnika iz prejšnje runde (če je nasprotnik v prejšnji rundi sodeloval, sodeluje tudi Tit4Tat, če je nasprotnik izdal, tudi Tit4Tat izda).
- Ta strategija nagrajuje sodelovanje in kaznuje izdajo.

### Always Defect (ALL-D)

- Igralec vedno izda ne glede na zgodovino igre.
- Ta strategija je agresivna in deluje dobro proti sodelovalnim strategijam, vendar je slaba proti drugim strategijam, ki kaznujejo izdajo.

### Random

- Igralec naključno izbira med sodelovanjem in izdajo z določeno verjetnostjo.
- Ta strategija je nepredvidljiva, vendar lahko deluje slabše proti bolj strateškim nasprotnikom.

### Tester
- Strategija začne z izdajo, da preveri odziv nasprotnika.
- V drugem krogu sodeluje, da vidi, kako nasprotnik reagira na začetno izdajo.
- Če je nasprotnik v drugem krogu kaznoval začetno izdajo (z izdajo), strategija preklopi na tit-for-tat pristop in ponavlja zadnjo potezo nasprotnika.
- Če nasprotnik ni kaznoval začetne izdaje (je še naprej sodeloval), ga strategija izkorišča z nadaljnjimi izdajami.
- Ta pristop omogoča testiranje nasprotnikove strategije in prilagajanje lastnega vedenja glede na njegove odzive.

### JOSS

- Podobna strategiji Tit4Tat, vendar občasno izda, tudi če bi Tit4Tat sicer sodeloval.
- Običajno ima majhno verjetnost izdaje (npr. 10 %), kar otežuje popolno sodelovanje nasprotnika.
- Ta strategija je bolj manipulativna, saj izkorišča preveč sodelovalne nasprotnike.

Vsaka strategija ima svoje prednosti in slabosti, odvisno od tega, proti komu igra. Pri ponavljajočih se igrah lahko določene strategije (npr. Tit4Tat) vzpostavijo dolgoročno sodelovanje, medtem ko druge (npr. ALL-D) izkoristijo sodelovalne nasprotnike.

## Načrt rešitve

Za implementacijo projekta smo pripravili naslednji načrt:

### Izbrana projektna skupina in sodelavci

- **Projektna skupina:** S7
- **Sodelavci:** Matic Lukežič, Tim Trojner Hlade, Dejan Tominc

### Povezava do repozitorija

- [Git repozitorij projekta](https://github.com/TimTrojner/psis-prisoners-dilemma)

### Izbran programski jezik

- Python

### Opravila in razvojne iteracije

Projekt bomo implementirali v štirih razvojnih iteracijah:

- [ ] **Iteracija 1:** Načrtovanje in postavitev osnovne strukture projekta. V tej fazi bomo definirali osnovne razrede in module za simulacijo igre ter pripravo podatkov za evalvacijo.
- [ ] **Iteracija 2:** Implementacija osnovnih strategij: ALL-D, RANDOM in TIT-FOR-TAT. V tej fazi bomo zagotovili, da strategije pravilno odločajo glede sodelovanja ali izdaje.
- [ ] **Iteracija 3:** Implementacija dodatnih strategij: TESTER in JOSS. Prav tako bomo integrirali evalvacijske metode za merjenje uspešnosti strategij preko simulacij.
- [ ] **Iteracija 4:** Razvoj lastne strategije, izvedba celovitega turnirja po Axelrodovih principih in optimizacija kode na podlagi rezultatov ter zaključna dokumentacija.

### Diagram razredov

![alt text](<UML class.svg>)

### Diagram odločitev primer

![alt text](diagramOdlocitevPrimer.png)

Prikaz s pomočjo tabele:

|               | Jaz molčim                    | Jaz priznam                  |
| ------------- | ----------------------------- | ---------------------------- |
| **On molči**  | **Jaz** 1 leto, **On** 1 leto | **Jaz** 0 let, **On** 10 let |
| **On prizna** | **Jaz** 10 let, **On** 0 let  | **Jaz** 5 let, **On** 5 let  |


# Prisoner's Dilemma Tournament Results

## Match Results

| Match | Score |
|-------|-------|
| Random vs TitForTat | 292 - 292 |
| Random vs AlwaysDefect | 770 - 230 |
| Random vs JOSS | 304 - 304 |
| Random vs Tester | 280 - 280 |
| TitForTat vs Random | 408 - 408 |
| TitForTat vs AlwaysDefect | 505 - 495 |
| TitForTat vs JOSS | 497 - 487 |
| TitForTat vs Tester | 501 - 491 |
| AlwaysDefect vs Random | 275 - 725 |
| AlwaysDefect vs TitForTat | 500 - 500 |
| AlwaysDefect vs JOSS | 500 - 500 |
| AlwaysDefect vs Tester | 495 - 505 |
| JOSS vs Random | 368 - 408 |
| JOSS vs TitForTat | 496 - 496 |
| JOSS vs AlwaysDefect | 505 - 495 |
| JOSS vs Tester | 501 - 491 |
| Tester vs Random | 413 - 403 |
| Tester vs TitForTat | 496 - 496 |
| Tester vs AlwaysDefect | 505 - 495 |
| Tester vs JOSS | 496 - 496 |

## Results Table (lower score is better)

|              | Random | TitForTat | AlwaysDefect | JOSS  | Tester |
|--------------|--------|-----------|--------------|-------|--------|
| Random       | 0.0    | 292.0     | 770.0        | 304.0 | 280.0  |
| TitForTat    | 408.0  | 0.0       | 505.0        | 497.0 | 501.0  |
| AlwaysDefect | 275.0  | 500.0     | 0.0          | 500.0 | 495.0  |
| JOSS         | 368.0  | 496.0     | 505.0        | 0.0   | 501.0  |
| Tester       | 413.0  | 496.0     | 505.0        | 496.0 | 0.0    |

## Ranking (Average Score)

1. **Random**: 329.20
2. **AlwaysDefect**: 354.00
3. **JOSS**: 374.00
4. **Tester**: 382.00
5. **TitForTat**: 382.20