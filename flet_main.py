import flet as ft
import random
import os
import time
from pathlib import Path


class Card:
    def __init__(self, number, color, image_path):
        self.number = number
        self.color = color
        self.image_path = image_path
        self.original_position = None  # Salva la posizione originale


class CardGame:
    def __init__(self):
        self.total_list = []
        self.score = 0
        self.available_cards = [None] * 5  # 5 posizioni fisse per le carte disponibili
        self.used_cards = [None] * 3  # 3 posizioni fisse per le carte in uso
        self.free_positions = []  # Posizioni libere nelle carte disponibili

    def initialize_cards(self):
        # Creazione delle carte per ogni colore (blu, rosso, verde)
        colors = ["blu", "rosso", "verde"]
        for color in colors:
            for i in range(1, 9):
                image_name = f"carta{i}_{color}.png"
                self.total_list.append((i, image_name, color))

        # Inizializza le posizioni libere (all'inizio tutte)
        self.free_positions = list(range(5))

        # Mescola le carte
        random.shuffle(self.total_list)

    def deal_initial_cards(self):
        # Distribuisci 5 carte iniziali nelle posizioni fisse
        for i in range(5):
            if len(self.total_list) > 0:
                number, image_name, color = self.total_list.pop(0)
                card = Card(number, color, image_name)
                self.available_cards[i] = card
                if i in self.free_positions:
                    self.free_positions.remove(i)

    def deal_new_cards(self):
        # Aggiungi carte solo nelle posizioni libere
        if len(self.free_positions) > 0 and len(self.total_list) > 0:
            positions_to_fill = min(len(self.free_positions), len(self.total_list))

            for _ in range(positions_to_fill):
                position = self.free_positions.pop(0)
                number, image_name, color = self.total_list.pop(0)
                self.available_cards[position] = Card(number, color, image_name)

            return True
        return False

    def move_card_to_used(self, index):
        # Sposta una carta dalla mano alla sezione di carte usate
        card = self.available_cards[index]
        if card:
            # Trova la prima posizione libera nelle carte usate
            for i in range(3):
                if self.used_cards[i] is None:
                    self.used_cards[i] = card
                    self.available_cards[index] = None
                    self.free_positions.append(index)
                    return True
        return False

    def move_card_to_available(self, index):
        # Sposta una carta dalla sezione usata alla mano
        card = self.used_cards[index]
        if card and len(self.free_positions) > 0:
            position = self.free_positions.pop(0)
            self.available_cards[position] = card
            self.used_cards[index] = None
            return True
        return False

    def check_combination(self):
        # Verifica se è presente una combinazione valida con le carte usate
        # Raccogliamo solo le carte valide (non None)
        valid_cards = [card for card in self.used_cards if card is not None]

        if len(valid_cards) == 3:
            # Estrai numeri e colori
            numbers = [int(card.number) for card in valid_cards]
            colors = [card.color for card in valid_cards]

            # Ordina i numeri per controllare scale
            sorted_numbers = sorted(numbers)

            # Verifica scala dello stesso colore
            if (sorted_numbers[0] + 1 == sorted_numbers[1] and
                    sorted_numbers[1] + 1 == sorted_numbers[2] and
                    colors[0] == colors[1] == colors[2]):
                self.score += sum(sorted_numbers) * 5
                # Pulisci le carte usate
                self.used_cards = [None, None, None]
                return "Scala Colore", True

            # Verifica scala di colori diversi
            elif (sorted_numbers[0] + 1 == sorted_numbers[1] and
                  sorted_numbers[1] + 1 == sorted_numbers[2]):
                self.score += sum(sorted_numbers)
                # Pulisci le carte usate
                self.used_cards = [None, None, None]
                return "Scala", True

            # Verifica tris
            elif sorted_numbers[0] == sorted_numbers[1] == sorted_numbers[2]:
                self.score += sum(sorted_numbers) * 3
                # Pulisci le carte usate
                self.used_cards = [None, None, None]
                return "Tris", True

        return "", False


def main(page: ft.Page):
    page.title = "Card Game"
    page.window_width = 360
    page.window_height = 740
    page.padding = 0

    # Inizializza il gioco
    game = CardGame()
    game.initialize_cards()

    # Elementi UI
    score_text = ft.Text(f"PUNTEGGIO: {game.score}", size=24, color=ft.colors.WHITE)
    remaining_cards_text = ft.Text(f"{len(game.total_list)}", size=24, color=ft.colors.WHITE)
    message_text = ft.Text("", size=20, color=ft.colors.WHITE)

    # Contenitore per le carte disponibili (in mano)
    available_cards_row = ft.Row(
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[ft.Container(width=60, height=90) for _ in range(5)]  # Placeholders
    )

    # Contenitore per le carte usate (in gioco)
    used_cards_row = ft.Row(
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[ft.Container(width=100, height=150) for _ in range(3)]  # Placeholders
    )

    # Mazzo di carte
    deck_container = ft.Container(
        content=ft.Image(
            src="/retro.png",  # Adatta il percorso
            width=130,
            height=160,
        ),
        width=130,
        height=160,
        border_radius=10,
    )

    # Funzione per creare un container per una carta
    def create_card_container(card, position, is_used=False):
        if card is None:
            return ft.Container(
                width=60 if not is_used else 100,
                height=90 if not is_used else 150,
                border_radius=8,
                border=ft.border.all(1, ft.colors.WHITE24),
            )

        card_image = ft.Image(
            src=f"/{card.color}/{card.image_path}",  # Adatta il percorso
            width=60 if not is_used else 100,
            height=90 if not is_used else 150,
            fit=ft.ImageFit.CONTAIN,
        )

        def on_card_tap(e):
            if is_used:
                # Sposta dalla sezione usata alla mano
                if game.move_card_to_available(position):
                    update_ui()
            else:
                # Sposta dalla mano alla sezione usata
                if game.move_card_to_used(position):
                    update_ui()
                    # Controlla per combinazioni dopo un breve ritardo
                    combo_name, combo_found = game.check_combination()
                    if combo_found:
                        message_text.value = f"{combo_name.upper()}!"
                        page.update()
                        time.sleep(1)
                        message_text.value = ""
                        update_ui()

        return ft.GestureDetector(
            content=ft.Container(
                content=card_image,
                border_radius=8,
                ink=True,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=5,
                    color=ft.colors.BLACK38,
                    offset=ft.Offset(0, 2),
                ),
            ),
            on_tap=on_card_tap,
        )

    # Gestione click sul mazzo
    def on_deck_tap(e):
        if game.deal_new_cards():
            update_ui()

        # Se il mazzo è vuoto, nascondilo
        if len(game.total_list) == 0:
            deck_container.visible = False
            page.update()

    deck_container.on_click = on_deck_tap

    # Aggiornamento UI
    def update_ui():
        # Aggiorna punteggio e carte rimanenti
        score_text.value = f"PUNTEGGIO: {game.score}"
        remaining_cards_text.value = f"{len(game.total_list)}"

        # Aggiorna carte disponibili (in mano)
        available_cards_row.controls.clear()
        for i in range(5):
            available_cards_row.controls.append(create_card_container(game.available_cards[i], i))

        # Aggiorna carte usate (in gioco)
        used_cards_row.controls.clear()
        for i in range(3):
            used_cards_row.controls.append(create_card_container(game.used_cards[i], i, True))

        page.update()

    # Distribuisci le carte iniziali
    game.deal_initial_cards()

    # Layout principale
    page.add(
        ft.Container(
            content=ft.Column([
                # Area superiore con punteggio
                ft.Container(
                    content=score_text,
                    padding=20,
                    alignment=ft.alignment.top_right,
                ),

                # Area messaggi
                ft.Container(
                    content=message_text,
                    padding=10,
                    alignment=ft.alignment.center,
                ),

                # Area per le carte selezionate
                ft.Container(
                    content=used_cards_row,
                    margin=ft.margin.only(top=50),
                    padding=10,
                    alignment=ft.alignment.center,
                ),

                # Spaziatore
                ft.Container(height=200),

                # Area per le carte disponibili in mano
                ft.Container(
                    content=available_cards_row,
                    padding=10,
                    alignment=ft.alignment.center,
                ),

                # Area inferiore con mazzo
                ft.Container(
                    content=ft.Row([
                        deck_container,
                        ft.Container(
                            content=remaining_cards_text,
                            margin=ft.margin.only(left=20),
                            alignment=ft.alignment.center,
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    margin=ft.margin.only(top=50),
                    padding=20,
                    alignment=ft.alignment.center,
                ),
            ]),
            width=page.width,
            height=page.height,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.BLUE_900, ft.colors.INDIGO_900],
            ),
        )
    )

    # Inizializza UI
    update_ui()


ft.app(target=main)