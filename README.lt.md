# 🧠 AI-Brain

„Ilgalaikės atminties“ ir „būsenos atsarginių kopijų“ sistema programuotojams, dirbantiems su AI.

„AI-Brain“ išsprendžia „konteksto praradimo“ (angl. *Context Drift*) problemą. Sistema palaiko **Projekto pasą** su loginiu **Simbolių žemėlapiu** (Symbol Map), kuris seka projekto struktūrą, klases ir logiką, todėl asistentai (ChatGPT, Claude, Cursor) gali akimirksniu tęsti darbą be papildomo kodo aiškinimo.

## 🚀 Funkcijos

- **Projektų registracija:** Sekite visus savo AI pagalba kuriamus projektus vienoje vietoje (globali duomenų bazė).
- **Simbolių žemėlapis:** Automatiškai aptinka klases, funkcijas ir logiką PHP, Python, JS ir TS kalbose.
- **Išmanioji kategorizacija:** Sugrupuoja kodą į [MODELS], [CTRLS], [SERVICES] ir [HELPERS] geresnei AI orientacijai.
- **Būsenos atsarginės kopijos:** Generuoja suglaustas (ZIP) kodo kopijas, ignoruodama sunkius aplankus (`node_modules`, `.git`, `.venv`).
- **AI taisyklių generavimas:** Sukuria `.cursorrules` ir `.clauderules`, kad AI asistentai automatiškai „atpažintų“ projekto struktūrą.
- **Optimizuotas kontekstas:** Sugeneruoja trumpą, AI tinkamą Markdown santrauką, skirtą tiesioginiam įkėlimui (*Prompt Injection*).

## 📦 Diegimas

Įsitikinkite, kad jūsų kompiuteryje įdiegtas **Python 3.10+**.

Klonuokite šią saugyklą arba eikite į jos katalogą ir paleiskite:

```bash
pip install -e .
```

Tai įdiegs `aib` komandą jūsų sistemoje globally.

## 🛠️ Naudojimas

Eikite į pasirinktą programavimo projektą:

```bash
cd /kelias/iki/jūsų/projekto
```

### 1. Inicijavimas (Initialize)
```bash
aib init
```
Sukuriamas `.ai-brain` aplankas ir užregistruojamas naujas projektas sistemoje.

### 2. Gilesnė analizė (Symbol Map)
```bash
aib analyze
```
Giliai nuskenuoja struktūrą ir ištraukia simbolius (klases, metodus). Tai užtikrina aukščiausios kokybės kontekstą AI modeliams.

### 3. Būsenos sinchronizavimas (Sync State)
```bash
aib sync
```
Atnaujina žemėlapį ir įraša trumpą „sesijos santrauką“ į ilgalaikę projekto atmintį.

### 4. AI taisyklės (Rules)
```bash
aib rules
```
Sugeneruoja `.cursorrules`, `.clauderules` ir `AI_INSTRUCTIONS.md` failus. Tai priverčia AI asistentus (Cursor, Claude Code) automatiškai naudoti „AI-Brain“ duomenis.

### 5. Konteksto įterpimas (Inject Context)
```bash
aib inject
```
Išveda optimizuotą Markdown bloką su projekto architektūra. Nukopijuokite jį į pokalbį su AI sesijos pradžioje – tai veikia kaip projekto „smegenų transplantacija“ asistentui.

### 6. Atsarginė kopija (Backup)
```bash
aib backup
```
Sukuria ZIP archyvą `backups/` aplanke, saugiai ignoruodamas pagalbinius sistemos failus.

### 7. Projektų sąrašas (List)
```bash
aib list
```
Parodo visų sekamų projektų sąrašą ir jų būsenas.

---
*Sukurta siekiant panaikinti konteksto praradimą ir pagreitinti programavimą su AI.*
