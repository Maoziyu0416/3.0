#3.2
#OPP+cmd
import random as r
import os
import sys

def input_name():
    while True:
        names = []
        names.append(input("请输入主角名："))

        # 禁止特定名字进入游戏
        forbidden_names = {"9", "2", "20230609", "20230602", "yqx", "mzy", "YQX", "MZY",
                           "yaoqixuan", "Maoziyu", "Yaoqixuan", "Maoziyu", "YaoQiXuan",
                           "MaoZiYu", "YAOQIXUAN", "MAOZIYU", "姚祁轩", "毛子煜"}

        if names[0] in forbidden_names:
            print("滚")
            sys.exit()

        print("请输入配角名，输入end以结束输入")
        while True:
            name = input()
            if name in forbidden_names:
                print(f"{name} 被禁止")
                continue
            if name == "end":
                if len(names) <= 2:
                    print("人数不足")
                else:
                    print("选定成功")
                    return names
            names.append(name)


def output(text):
    for line in text:
        print(line)
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
        output(self.event_log)
        os.system("cls")

    def death_chain(self, reason_people, reason_num):
        reason_text = ["死了", "结婚了"]
        for lover in self.players[reason_people].be_loved:
            if self.random_choice(1, 3) and self.players[lover].alive:
                self.event_log.append(f"由于{self.players[reason_people]}{reason_text[reason_num]},{self.players[lover]}自杀了")
                self.alive_players.remove(lover)
                self.players[lover].alive = False
                if len(self.alive_players) <= 1:
                    self.end_game()
                    return
                self.death_chain(lover, 0)

    def divorce(self, a, b, reason):
        self.event_log.append(f"由于{self.players[b]}{reason}，{self.players[a]}和{self.players[b]}离婚了")
        self.players[a].marry = -1
        self.players[b].marry = -1

        if not r.randint(0, 5):
            try:
                next_a_marriage = r.choice(self.players[a].be_loved)
                if self.players[next_a_marriage].marry == -1:
                    self.get_married(a, next_a_marriage)
                else:
                    self.cheating(next_a_marriage, a)
            except:
                pass

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

    def fall_in_love(self, sub, ob, root_event):
        self.event_log.append(f"{self.players[sub]}爱上了{self.players[ob]}")
        self.players[sub].love.append(ob)
        self.players[ob].be_loved.append(sub)

        if sub in self.players[ob].love:
            self.event_log.append(f"因为{self.players[ob]}本就喜欢{self.players[sub]}，两人很快就开始谈恋爱")
            if r.randint(0, 1):
                self.get_married(sub, ob)
            else:
                self.event_log.append(f"可惜后来，{self.players[sub]}和{self.players[ob]}分手了")
        elif r.randint(0, 2) == 0 or root_event == 1:
            self.event_log.append(f"{self.players[ob]}也喜欢{self.players[sub]}")
            self.players[ob].love.append(sub)
            self.players[sub].be_loved.append(ob)
            self.event_log.append(f"{self.players[sub]}和{self.players[ob]}很快就开始谈恋爱")
            if r.randint(0, 1):
                self.get_married(sub, ob)
            else:
                self.event_log.append(f"可惜后来，{self.players[sub]}和{self.players[ob]}分手了")
        elif r.randint(0, 2) == 1:
            self.event_log.append(f"然而{self.players[ob]}不喜欢{self.players[sub]}")
            if r.randint(0, 3) == 0:
                self.event_log.append(f"因此,{self.players[sub]}自杀了")
                self.alive_players.remove(sub)
                self.players[sub].alive = False
                if len(self.alive_players) <= 1:
                    self.end_game()
                    return
                self.death_chain(sub, 0)
            else:
                self.event_log.append(f"{self.players[sub]}得知{self.players[ob]}不喜欢他，很快从阴影中走出来了")
                self.players[sub].love.remove(ob)
                self.players[ob].be_loved.remove(sub)
        else:
            self.event_log.append(f"{self.players[sub]}为了有朝一日能和{self.players[ob]}在一起，决定将这个秘密藏在心底")

    def cheating(self, sub, ob):
        if self.players[sub].marry == -1 and self.players[ob].marry == -1:
            self.fall_in_love(sub, ob, 1)
            return

        if self.players[sub].marry == -1 and self.players[ob].marry != -1:
            sub, ob = ob, sub  # 交换sub和ob

        self.event_log.append(f"{self.players[sub]}喜欢上{self.players[ob]}，绿了{self.players[self.players[sub].marry]}")

        if self.random_choice(1, 2):
            self.have_sex(sub, ob)

        if not r.randint(0, 2):
            self.event_log.append(f"{self.players[self.players[sub].marry]}发现{self.players[sub]}绿了他，开始犹豫是否要离婚")
            self.choose_event()
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
            self.end_game()
            return
        event_choice = r.randint(0, 3)
        sub, ob = r.sample(self.alive_players, 2)

        if event_choice == 0:
            self.get_married(sub, ob)
        elif event_choice == 1:
            self.fall_in_love(sub, ob, 0)
        elif event_choice == 2:
            self.cheating(sub, ob)
        elif event_choice == 3:
            self.have_sex(sub, ob)

    def start_game(self):
        print(f"{self.players[0]}从小暗恋{r.choice(self.players[1:])}")
        print(f"{self.players[0]}的白月光是{r.choice(self.players[1:])}")
        print(f"{self.players[0]}的初恋是{r.choice(self.players[1:])}")
        print(f"{self.players[0]}和{r.choice(self.players[1:])}是青梅竹马")
        print(f"{self.players[0]}的第一次给了{r.choice(self.players[1:])}")

        while len(self.alive_players) >= 2:
            self.choose_event()

def main():
    names = input_name()
    game = Game(names)
    game.start_game()

if __name__ == "__main__":
    main()
