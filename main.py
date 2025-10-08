import csv

class Automobile:
    def __init__(self, codice, marca, modello, anno_immatricolazione, num_posti):
        self.codice = codice
        self.marca = marca
        self.modello = modello
        self.anno_immatricolazione = anno_immatricolazione
        self.num_posti = num_posti
        self.noleggiata = False

    def __str__(self):
        return f'{self.codice} - {self.marca} {self.modello} ({self.anno_immatricolazione}) - {self.num_posti} posti'


class Noleggio:
    def __init__(self, codice, data, id_automobile, cognome_cliente):
        self.codice = codice
        self.data = data
        self.id_automobile = id_automobile
        self.cognome_cliente = cognome_cliente

    def __str__(self):
        return f'{self.codice} - Auto {self.id_automobile} - Cliente {self.cognome_cliente} - Data {self.data}'


class Autonoleggio:
    def __init__(self, nome, responsabile):
        self.nome = nome
        self.responsabile = responsabile
        self.automobili = []
        self.noleggi = []

    def carica_file_automobili(self, file_path):
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    auto = Automobile(
                        codice=row[0],
                        marca=row[1],
                        modello=row[2],
                        anno_immatricolazione=int(row[3]),
                        num_posti=int(row[4])
                    )
                    self.automobili.append(auto)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} non trovato")

    def aggiungi_automobile(self, marca, modello, anno, num_posti):
        # Controlla se l'auto esiste già
        for auto in self.automobili:
            if (auto.marca == marca and
                    auto.modello == modello and
                    auto.anno_immatricolazione == anno):
                return None

        # Genera codice univoco
        if self.automobili:
            codici = [auto.codice for auto in self.automobili]
            ultimoCodice = max(int(codice[1:]) for codice in codici)
            nuovo_codice_a = f'A{ultimoCodice + 1}'
        else:
            nuovo_codice_a = "A1"

        # Crea la nuova auto
        nuova_auto = Automobile(
            codice=nuovo_codice_a,
            marca=marca,
            modello=modello,
            anno_immatricolazione=anno,
            num_posti=num_posti
        )
        self.automobili.append(nuova_auto)
        return nuova_auto

    def automobili_ordinate_per_marca(self):
        automobili_ordinate = sorted(self.automobili, key=lambda auto: auto.marca)
        return automobili_ordinate

    def nuovo_noleggio(self, data, id_automobile, cognome_cliente):
        # Cerca l'auto
        auto_trovata = None
        for auto in self.automobili:
            if auto.codice == id_automobile:
                auto_trovata = auto
                break

        # Controlli
        if auto_trovata is None:
            raise Exception(f"Auto {id_automobile} non trovata")

        if auto_trovata.noleggiata:
            raise Exception(f"Auto {id_automobile} già noleggiata")

        # Genera codice noleggio
        if self.noleggi:
            ultimo_numero = max(int(n.codice[1:]) for n in self.noleggi)
            nuovo_codice_n = f'N{ultimo_numero + 1}'
        else:
            nuovo_codice_n = 'N1'

        # Crea il noleggio
        noleggio = Noleggio(nuovo_codice_n, data, id_automobile, cognome_cliente)
        self.noleggi.append(noleggio)
        auto_trovata.noleggiata = True

        return noleggio

    def termina_noleggio(self, id_noleggio):
        # Cerca il noleggio
        noleggio_trovato = None
        for noleggio in self.noleggi:
            if noleggio.codice == id_noleggio:
                noleggio_trovato = noleggio
                break

        if noleggio_trovato is None:
            raise Exception(f"Noleggio {id_noleggio} non trovato")

        # Trova l'auto e la rende disponibile
        auto_trovata = None
        for auto in self.automobili:
            if auto.codice == noleggio_trovato.id_automobile:
                auto_trovata = auto
                break

        if auto_trovata:
            auto_trovata.noleggiata = False

        # Rimuove il noleggio
        self.noleggi.remove(noleggio_trovato)


def main():
    autonoleggio = Autonoleggio('Breaking Bad', 'Walter White')

    while True:
        print("\n" + "=" * 40)
        print("MENU AUTONOLEGGIO")
        print("=" * 40)
        print("1. Modifica nome responsabile")
        print("2. Carica automobili da file")
        print("3. Aggiungi nuova automobile")
        print("4. Visualizza automobili ordinate per marca")
        print("5. Noleggia automobile")
        print("6. Termina noleggio automobile")
        print("7. Esci")
        print("-" * 40)

        scelta = input("Scegli un'opzione: ")

        if scelta == '1':
            nuovo_responsabile = input('Nuovo responsabile: ')
            autonoleggio.responsabile = nuovo_responsabile
            print(f"Responsabile cambiato: {nuovo_responsabile}")

        elif scelta == '2':
            file_path = input('File path: ')
            try:
                autonoleggio.carica_file_automobili(file_path)
                print(f"Caricate {len(autonoleggio.automobili)} automobili")
            except Exception as e:
                print(f'Errore: {e}')

        elif scelta == '3':
            marca = input('Marca: ')
            modello = input('Modello: ')
            anno = int(input('Anno: '))
            posti = int(input('Posti: '))

            auto = autonoleggio.aggiungi_automobile(marca, modello, anno, posti)

            if auto:
                print(f"Aggiunta {auto}")
            else:
                print('Auto già esistente')

        elif scelta == '4':
            auto_ordinate = autonoleggio.automobili_ordinate_per_marca()
            print("\nAutomobili ordinate per marca:")
            for auto in auto_ordinate:
                stato = "Noleggiata" if auto.noleggiata else "Disponibile"
                print(f"  {auto} - {stato}")

        elif scelta == '5':
            print("\nAuto disponibili:")
            auto_disponibili = [auto for auto in autonoleggio.automobili if not auto.noleggiata]
            for auto in auto_disponibili:
                print(f"  {auto.codice} - {auto.marca} {auto.modello}")

            if not auto_disponibili:
                print("  Nessuna auto disponibile")
                continue

            id_auto = input("\nCodice auto da noleggiare (es: A1): ")
            data = input("Data noleggio (es: 2024-01-15): ")
            cliente = input("Cognome cliente: ")

            try:
                noleggio = autonoleggio.nuovo_noleggio(data, id_auto, cliente)
                print(f"Noleggio creato: {noleggio}")
            except Exception as e:
                print(f"Errore: {e}")

        elif scelta == "6":
            print("\nNoleggi attivi:")
            for noleggio in autonoleggio.noleggi:
                print(f"  {noleggio}")

            if not autonoleggio.noleggi:
                print("  Nessun noleggio attivo")
                continue

            id_noleggio = input("\nCodice noleggio da terminare (es: N1): ")
            try:
                autonoleggio.termina_noleggio(id_noleggio)
                print(f"Noleggio {id_noleggio} terminato")
            except Exception as e:
                print(f"Errore: {e}")

        elif scelta == "7":
            print("Arrivederci!")
            break

        else:
            print("Opzione non valida!")


if __name__ == "__main__":
    main()