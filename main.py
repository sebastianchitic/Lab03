from autonoleggio import Autonoleggio
from datetime import datetime


def menu():
    print("\n--- MENU AUTONOLEGGIO ---")
    print("1. Modifica nome del responsabile dell'autonoleggio")
    print("2. Carica automobili da file")
    print("3. Aggiungi nuova automobile (da tastiera)")
    print("4. Visualizza automobili ordinate per marca")
    print("5. Noleggia automobile")
    print("6. Termina noleggio automobile")
    print("7. Esci")
    return input("Scegli un'opzione >> ")


def main():
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")

    while True:
        scelta = menu()

        if scelta == "1":
            nuovo_responsabile = input("Inserisci il nuovo responsabile: ")
            autonoleggio.responsabile = nuovo_responsabile
            print(f"Responsabile aggiornato a: {nuovo_responsabile}")

        elif scelta == "2":
            while True:
                try:
                    file_path = input("Inserisci il path del file da caricare: ").strip()
                    autonoleggio.carica_file_automobili(file_path)
                    print(f"Caricate {len(autonoleggio.automobili)} automobili con successo!")
                    break
                except Exception as e:
                    print(e)

        elif scelta == "3":
            marca = input("Marca: ")
            modello = input("Modello: ")
            try:
                anno = int(input("Anno di Immatricolazione: ").strip())
                posti = int(input("Numero di posti: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno e posti.")
                continue

            automobile = autonoleggio.aggiungi_automobile(marca, modello, anno, posti)
            if automobile:
                print(f"Automobile aggiunta: {automobile}")
            else:
                print("Errore: automobile già esistente!")

        elif scelta == "4":
            automobili_ordinate = autonoleggio.automobili_ordinate_per_marca()
            print("\nAutomobili ordinate per marca:")
            for a in automobili_ordinate:
                print(f'- {a}')

        elif scelta == "5":
            id_auto = input("ID automobile: ")
            cognome_cliente = input("Cognome cliente: ")
            data = datetime.now().date()
            try:
                noleggio = autonoleggio.nuovo_noleggio(data, id_auto, cognome_cliente)
                print(f"Noleggio andato a buon fine: {noleggio}")
            except Exception as e:
                print(e)

        elif scelta == "6":
            id_noleggio = input("ID noleggio da terminare: ")
            try:
                autonoleggio.termina_noleggio(id_noleggio)
                print(f"Noleggio {id_noleggio} terminato con successo.")
            except Exception as e:
                print(e)

        elif scelta == "7":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida!")


if __name__ == "__main__":
    main()