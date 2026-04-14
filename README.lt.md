# 🧠 AI-Brain

„Ilgalaikės atminties“ ir „būsenos atsarginių kopijų“ sistema programuotojams, dirbantiems su AI.

„AI-Brain“ išsprendžia „konteksto praradimo“ (angl. *Context Drift*) problemą. Sistema palaiko „Projekto pasą“, kuris seka vizualinę ir loginę projekto struktūrą, todėl bet koks didysis kalbos modelis (ChatGPT, Claude) gali akimirksniu tęsti darbą be pakartotinio kodo aiškinimo.

## 🚀 Funkcijos

*   **Projektų registracija:** Sekite visus savo AI pagalba kuriamus projektus vienoje vietoje (globali duomenų bazė).
*   **Grafinis skenavimas:** Automatiškai atvaizduoja jūsų katalogų struktūrą į loginį JSON grafiką.
*   **Būsenos atsarginės kopijos:** Generuoja suglaustas (ZIP) kodo kopijas, automatiškai ignoruodama sunkius aplankus (`node_modules`, `.git`, `.venv`).
*   **Context Generation:** Sukuria specialią santrauką, skirtą įkelti į AI užklausą (*Prompt Injection*), kad asistentas iškart „suprastų“ visą projektą.

## 📦 Diegimas

Įsitikinkite, kad jūsų kompiuteryje įdiegtas **Python 3.10+**.

1. Klonuokite šią saugyklą arba eikite į jos katalogą.
2. Paleiskite diegimo komandą:

```bash
pip install -e .
```

Po šios komandos `aib` įrankis taps pasiekiamas bet kuriame jūsų terminalo lange.

## 🛠️ Naudojimas

Navigate to any coding project you want to track:

```bash
cd /kelias/iki/jūsų/projekto
```

### 1. Inicijavimas (Initialize)
```bash
aib init
```
Sukuriamas `.ai-brain` aplankas ir užregistruojamas naujas projektas sistemoje.

### 2. Būsenos sinchronizavimas (Sync State)
```bash
aib sync
```
Atnaujinamas projekto struktūros žemėlapis ir įrašoma trumpa darbų istorija (log'as).

### 3. Gilesnė analizė (Deep Analysis)
```bash
aib analyze
```
Giliai nuskenuoja projekto struktūrą ir automatiškai sugeneruoja trumpus aprašymus kiekvienam failui bei katalogui, užtikrinant dar geresnį kontekstą AI asistentui.

### 4. Atsarginė kopija (Backup)
```bash
aib backup
```
Sukuria momentinę kodo kopiją `backups/` aplanke. Saugus būdas eksperimentuoti su AI generuojamu kodu.

### 4. Konteksto įterpimas (Inject Context)
```bash
aib inject
```
Išveda suformatuotą tekstą. Jį tiesiog nukopijuokite ir įklijuokite į savo pokalbį su ChatGPT ar Claude sesijos pradžioje.

### 5. Projektų sąrašas (List Projects)
```bash
aib list
```
Parodo visų jūsų kompiuteryje esančių projektų sąrašą ir jų būsenas.

---
*Sukurta siekiant pagreitinti darbą su dirbtiniu intelektu ir išvengti klaidų dėl konteksto trūkumo.*
