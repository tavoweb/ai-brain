🧠 AI-Brain
„Ilgalaikės atminties“ ir „būsenos atsarginių kopijų“ sistema programuotojams, dirbantiems su AI.

„AI-Brain“ išsprendžia „konteksto praradimo“ (angl. Context Drift) problemą. Sistema palaiko „Projekto pasą“, kuris seka vizualinę ir loginę projekto struktūrą, todėl bet koks didysis kalbos modelis (ChatGPT, Claude) gali akimirksniu tęsti darbą be pakartotinio kodo aiškinimo.

Funkcijos
Projektų registracija: sekite visus savo AI pagalba kuriamus projektus vienoje vietoje.

Grafinis skenavimas: atvaizduoja jūsų katalogų struktūrą JSON grafiko pavidalu.

Būsenos atsarginės kopijos: automatiškai suglaudina (zip) ir daro kodo kopijas be .git ar node_modules šiukšlių.

Konteksto generavimas: sukuria lengvai nukopijuojamą „Markdown“ santrauką apie projektą ir naujausią istoriją, skirtą įkelti į AI užklausą (prompt injection).

Diegimas
Įsitikinkite, kad turite įdiegtą Python 3.10+.

Klonuokite šią saugyklą, eikite į jos katalogą ir paleiskite:

Bash
pip install -e .
Tai įdiegs aib komandą jūsų sistemoje globaliai.

Naudojimas
Eikite į bet kurį programavimo projektą, kurį norite sekti:

Bash
cd /kelias/iki/jūsų/projekto
Inicijavimas (Initialize)
Bash
aib init
Paruošia „AI-Brain“ darbui esamame aplanke. Paprašys nurodyti projekto pavadinimą.

Būsenos sinchronizavimas (Sync State)
Bash
aib sync
Nuskanuoja esamus failus, atnaujina vietinį projekto struktūros žemėlapį ir paprašo trumpo „sesijos apibendrinimo“ (pvz., „Pridėtas prisijungimo modulis“), kuris įtraukiamas į projekto istoriją.

Atsarginė kopija (Backup)
Bash
aib backup
Sukuria suglaustą (ZIP) esamos būsenos momentinę kopiją ir išsaugo ją projekto viduje esančiame backups/ kataloge, ignoruodama sunkius aplankus, tokius kaip node_modules ar .venv.

Konteksto įterpimas (Inject Context)
Bash
aib inject
Išveda suformatuotą „Markdown“ bloką, kuriame yra visa projekto architektūra ir naujausi pakeitimai. Nukopijuokite šį bloką ir įklijuokite į ChatGPT/Claude naujos sesijos pradžioje – AI iškart žinos jūsų projekto kontekstą!

Projektų sąrašas (List Projects)
Bash
aib list
Parodo išsamią lentelę su visais jūsų sistemoje „AI-Brain“ valdomais projektais ir jų paskutinio atnaujinimo būseną.
