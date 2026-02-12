# Analiză Proiect: Suplimente Django

Acest proiect este o aplicație web de tip E-commerce (magazin online) dezvoltată în **Django**, dedicată vânzării de suplimente.

## Structura Generală

- **Nume Proiect:** `suplimente_django`
- **Aplicații:**
    - `magazin`: Aplicația principală care conține logica magazinului.
    - `Mesaje`: Un director utilizat pentru stocarea mesajelor primite prin formularul de contact (format JSON).
    - `suplimente`: Directorul de configurare a proiectului.

## Configurare Tehnică
- **Bază de date:** Este configurat pentru a utiliza **PostgreSQL** (`proiectsuplimente`), deși există un fișier `db.sqlite3` în rădăcină (probabil nefolosit sau vechi).
- **Dependency Management:** Fișiere standard Django (`manage.py`, `wsgi.py`, `asgi.py`).

## Funcționalități Principale (Aplicația `magazin`)

### 1. Modele de Date (`models.py`)
Structura bazei de date este bine definită pentru un magazin:
- **`Produs`**: Elementul central. Include preț, stoc, status (activ/inactiv), și relații către Categorie, Producător, Ingrediente și Oferte.
- **`Categorie`**: Categoriile produselor, având proprietăți vizuale precum `culoare` (hex) și `icon` (FontAwesome).
- **`Producator`**: Informații despre producători (țară, an înființare, cifră afaceri).
- **`Ingredient`**: Lista de ingrediente posibile, clasificate după tip (activ, aromă, vitamină, altele).
- **`Oferta`**: Gestionarea reducerilor procentuale pe perioade de timp.
- **`ProfilUtilizator`**: Extensie a utilizatorului standard Django, adăugând telefon și adresă completă.

### 2. Fluxuri de Utilizator (`views.py` & `urls.py`)
- **Navigare Publică:** Pagini pentru Acasă, Despre, Info.
- **Catalog Produse:**
    - Listare produse cu **filtrare avansată** (după nume, preț minim/maxim, categorie, status activ).
    - Sortare (ascendentă/descendentă după preț).
    - Paginare customizabilă.
    - Pagini de detaliu produs și filtrare după categorie.
- **Cont Utilizator:**
    - Înregistrare (creează automat și profilul de utilizator).
    - Autentificare (Login) și Delogare.
    - Pagina de profil (accesibilă doar utilizatorilor autentificați).
- **Coș Virtual:** Există rute pentru coș, dar momentan afișează o pagină "În lucru".

### 3. Funcționalități Speciale
- **Formular de Contact Complex:**
    - Validează vârsta utilizatorului.
    - Procesează textul mesajului (corectează spațierea, formatează majusculele după punctuație).
    - **Calcul Urgență:** Determină automat dacă un mesaj este urgent pe baza tipului de mesaj și a timpului de așteptare selectat.
    - Salvează mesajele ca fișiere **JSON** în folderul `Mesaje`, cu timestamp.
- **Sistem Custom de Logging:**
    - Clasa `Accesare` reține în memorie (RAM) istoricul cererilor (IP, URL, data).
    - Pagina `/log/` permite vizualizarea acestor loguri, filtrarea lor și chiar afișarea interogărilor SQL executate (pentru debugging).
- **Context Processors:**
    - `categorii_meniu`: Face categoriile disponibile în toate template-urile (pentru meniu).
    - `status_relatii_clienti`: Verifică un orar dintr-un fișier JSON (`program_relatii.json`) și afișează dacă serviciul de relații cu clienții este deschis sau închis în momentul accesării.

### Concluzie
Proiectul este un prototip funcțional avansat pentru un magazin online, având implementate structurile de date de bază și fluxurile principale, cu câteva elemente interesante de procesare a datelor (contact form) și monitorizare (logging). Zona de "Coș de cumpărături" și "Comandă" pare a fi încă în dezvoltare ("in_lucru").
