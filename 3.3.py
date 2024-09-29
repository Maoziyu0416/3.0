#较为完美的3.3
#尺寸仍需磨合
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import random as r

class Player:
    def __init__(self, name, order):
        self.name = name
        self.order = order
        self.love = []
        self.be_loved = []
        self.marry = -1
        self.hate = []
        self.alive = True
        self.no_sex = True

    def __repr__(self):
        return self.name

class Game:
    def __init__(self, names):
        self.players = [Player(name, i) for i, name in enumerate(names)]
        self.alive_players = [p.order for p in self.players]
        self.event_log = []

    def random_choice(self, a, b):
        return r.randint(0, b-1) < a

    def update_states(self):
        for player in self.players:
            if not player.alive:
                continue
            player.love = [p for p in player.love if self.players[p].alive]
            player.be_loved = [p for p in player.be_loved if self.players[p].alive]

    def end_game(self):
        if len(self.alive_players) == 1:
            self.event_log.append(f"{self.players[self.alive_players[0]]}是最后的赢家!")
        else:
            self.event_log.append("游戏结束，没有赢家!")
        return "\n".join(self.event_log)

    def death_chain(self, reason_people, reason_num):
        reason_text = ["死了", "结婚了"]
        for lover in self.players[reason_people].be_loved:
            if self.random_choice(1, 3) and self.players[lover].alive:
                self.event_log.append(f"由于{self.players[reason_people]}{reason_text[reason_num]},{self.players[lover]}自杀了")
                self.alive_players.remove(lover)
                self.players[lover].alive = False
                if len(self.alive_players) <= 1:
                    return self.end_game()
                self.death_chain(lover, 0)

    def divorce(self, a, b, reason):
        self.event_log.append(f"由于{self.players[b]}{reason}，{self.players[a]}和{self.players[b]}离婚了")
        self.players[a].marry = -1
        self.players[b].marry = -1

    def get_married(self, sub, ob):
        self.event_log.append(f"{self.players[sub]}和{self.players[ob]}结婚了")
        self.players[sub].marry = ob
        self.players[ob].marry = sub

        party_attendees = [p for p in self.alive_players if p != sub and p != ob and r.randint(0, 2)]
        if party_attendees:
            attendees_names = ",".join([self.players[p].name for p in party_attendees])
            self.event_log.append(f"{attendees_names}来到了婚礼现场")
        else:
            self.event_log.append("没人来到了婚礼现场")

        self.event_log.append("婚礼现场，一片幸福的气息，然而当晚：")
        before_alive = len(self.alive_players)
        self.death_chain(sub, 1)
        self.death_chain(ob, 1)
        after_alive = len(self.alive_players)
        if before_alive == after_alive:
            self.event_log.pop()
            self.event_log.append("婚礼美满地结束了")
        else:
            self.event_log.append(f"今晚一共死了{before_alive - after_alive}人")

    def fall_in_love(self, sub, ob):
        self.event_log.append(f"{self.players[sub]}爱上了{self.players[ob]}")
        self.players[sub].love.append(ob)
        self.players[ob].be_loved.append(sub)

        if sub in self.players[ob].love:
            self.event_log.append(f"因为{self.players[ob]}本就喜欢{self.players[sub]}，两人很快就开始谈恋爱")
            if r.randint(0, 1):
                self.get_married(sub, ob)
            else:
                self.event_log.append(f"可惜后来，{self.players[sub]}和{self.players[ob]}分手了")
        else:
            self.event_log.append(f"然而{self.players[ob]}不喜欢{self.players[sub]}")
            if r.randint(0, 3) == 0:
                self.event_log.append(f"因此,{self.players[sub]}自杀了")
                self.alive_players.remove(sub)
                self.players[sub].alive = False
                if len(self.alive_players) <= 1:
                    return self.end_game()
                self.death_chain(sub, 0)

    def cheating(self, sub, ob):
        if self.players[sub].marry == -1 and self.players[ob].marry == -1:
            self.fall_in_love(sub, ob)
            return

        if self.players[sub].marry == -1 and self.players[ob].marry != -1:
            sub, ob = ob, sub  # 交换sub和ob

        self.event_log.append(f"{self.players[sub]}喜欢上{self.players[ob]}，绿了{self.players[self.players[sub].marry]}")

        if self.random_choice(1, 2):
            self.have_sex(sub, ob)

        if not r.randint(0, 2):
            self.event_log.append(f"{self.players[self.players[sub].marry]}发现{self.players[sub]}绿了他，开始犹豫是否要离婚")
            self.divorce(self.players[sub].marry, sub, "绿了他")

    def have_sex(self, sub, ob):
        self.event_log.append(f"{self.players[sub]}和{self.players[ob]}发生了X关系")
        if self.players[sub].no_sex:
            self.players[sub].no_sex = False
            self.event_log.append(f"{self.players[sub]}的第一次给了{self.players[ob]}")
        if self.players[ob].no_sex:
            self.players[ob].no_sex = False
            self.event_log.append(f"{self.players[ob]}的第一次给了{self.players[sub]}")

    def choose_event(self):
        if len(self.alive_players) < 2:
            return self.end_game()
        event_choice = r.randint(0, 3)
        sub, ob = r.sample(self.alive_players, 2)

        if event_choice == 0:
            self.get_married(sub, ob)
        elif event_choice == 1:
            self.fall_in_love(sub, ob)
        elif event_choice == 2:
            self.cheating(sub, ob)
        elif event_choice == 3:
            self.have_sex(sub, ob)

    def start_game(self):
        self.event_log.append(f"{self.players[0]}从小暗恋{r.choice(self.players[1:])}")
        self.event_log.append(f"{self.players[0]}的白月光是{r.choice(self.players[1:])}")
        self.event_log.append(f"{self.players[0]}的初恋是{r.choice(self.players[1:])}")
        self.event_log.append(f"{self.players[0]}和{r.choice(self.players[1:])}是青梅竹马")
        self.event_log.append(f"{self.players[0]}的第一次给了{r.choice(self.players[1:])}")

        while len(self.alive_players) >= 2:
            result = self.choose_event()
            if result:
                return result
        return self.end_game()

# GUI部分，使用old.py的设计
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("炸裂情感史")
        self.input_screen()

    def input_screen(self):
        # 主角输入
        self.label1 = tk.Label(self, text="请输入主角名：")
        self.label1.pack(anchor="nw")
        self.entry_main = tk.Entry(self)
        self.entry_main.pack(fill="x")

        # 配角输入
        self.label2 = tk.Label(self, text="请输入配角名（一行一个）：")
        self.label2.pack(anchor="nw")
        self.text_support = tk.Text(self, height=5)
        self.text_support.pack(fill="x")

        # 确定按钮
        self.button_confirm = tk.Button(self, text="确定", command=self.get_input)
        self.button_confirm.pack(fill="x")

    def get_input(self):
        # 获取主角和配角数据
        main_character = self.entry_main.get().strip()
        supporting_characters = self.text_support.get("1.0", tk.END).strip().split("\n")
        characters = [main_character] + supporting_characters

        if main_character and supporting_characters:
            self.clear_screen()
            self.output_screen(characters)

    def clear_screen(self):
        # 清除输入部分的组件
        self.label1.pack_forget()
        self.entry_main.pack_forget()
        self.label2.pack_forget()
        self.text_support.pack_forget()
        self.button_confirm.pack_forget()

    def output_screen(self, characters):
        # 事件日志输出
        self.text_output = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15)
        self.text_output.pack(fill="both")

        # 生成剧情
        game = Game(characters)
        result = game.start_game()

        # 输出结果
        self.text_output.insert(tk.END, result)

        # 保存按钮
        self.button_save = tk.Button(self, text="保存", command=self.save_result)
        self.button_save.pack(fill="x")

    def save_result(self):
        # 保存事件日志到文件
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_output.get("1.0", tk.END))
            messagebox.showinfo("保存成功", "文件已保存")

if __name__ == "__main__":
    win = Window()
    win.size=
    win.mainloop()
