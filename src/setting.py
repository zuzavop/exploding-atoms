game_title = "Exploding Atoms"
res_path = "..\\res\\"
font_path = res_path + "font_title.ttf"
background_path = res_path + "universe.jpg"
icon_path = res_path + "icon.png"

window_width = 1000
window_height = 700
field_size = 8

colors = {"blue": (58, 214, 204), "red": (255, 36, 36), "black": "black", "aqua": (114, 242, 208), "white": "white"}

hint_text = ["Hráči střídavě vybírají políčka neboli atomy z hracího plánu. Nelze zvolit atom,",
             "který je již zabran soupeřem. Když je atom NAPLNĚN, tj. obsahuje dostatečný počet",
             "částic (tak velké číslo, jako má políčko sousedních políček - tedy podle umístění políčka",
             "čísla 2, 3 nebo 4), exploduje a rozdělí se mezi sousední atomy. Případné soupeřovy částice,",
             "které tam již byly, přebarví na svou barvu. Soupeřovi vlastní atomy zůstávají a pokud je atom",
             "znovu naplněn následuje další exploze. Vyhrává hráč, který eliminuje soupeře,",
             "tedy jinak řečeno dokáže obarvit celé hrací pole svou barvou."]

texts = {
    "first_turn": "Na tahu je první hráč",
    "second_turn": "Na tahu je druhý hráč",
    "computer_turn": "Na tahu je počítač",
    "back": "Zpět"
}
