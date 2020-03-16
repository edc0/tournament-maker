import gui
import logic

if __name__ == "__main__":
    player_keys = ["Rafael DÜS", "Moggi DUI", "Ben MÜ","Patrick BRÜ", "Frank HAN",
    "Aislan GRO", "Markus HAN", "Julius HAL", "Holger ALA", "Thommy HAN",
    "Aljoscha BER", "Christoph LEI", "Markus BER", "Richie LEI", "Emílio D. C. BER",
    "Max CAM", "Florian GRO", "Levin HAL", "John MAN", "Oli MAN",
    "Dima Kharkiv", "Megan AUS", "Daniel HAL", "Judith HH ", "Antonio LON", "Domi ULM",
    "Sam ZÜR", "Thomas HAN ", "Rado FRA", "David MÜ", "Chris HH ", "Steffn HH",
    "Fabian BÜ", "Ole BÜ", "Flo BÜ", "Johannes BÜ", "Buby BÜ", "Kai BÜ", "Andy BÜ",
    "Franky BÜ"]

    game_number = (len(player_keys)//2 if len(player_keys)%6 == 0 else (len(player_keys)//6)+1)
    player_list = logic.init_players(player_keys)

    ui = gui.SchedulerGUI("Scheduler", player_list)

    ui.mainloop()
