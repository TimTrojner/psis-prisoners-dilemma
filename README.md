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
- **Analiza stabilnosti:** Preučevanje, katera strategija dosega stabilno ravnovesje (npr. Nashovo ravnovesje) v iterativni igri.
- **Statistična primerjava:** Uporaba statističnih metod za primerjavo rezultatov turnirjev med različnimi strategijami.
- **Eksperimentalna validacija:** Izvajanje eksperimentov s simulacijami turnirja, kot ga je predlagal Axelrod, in preverjanje hipoteze o prednosti sodelovanja pri večkratnem ponavljanju igre.

