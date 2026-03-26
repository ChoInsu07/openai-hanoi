import sys
import os

ESC = '\033'
RESET = f'{ESC}[0m'
BOLD = f'{ESC}[1m'
CYAN = f'{ESC}[36m'
YELLOW = f'{ESC}[33m'
MAGENTA = f'{ESC}[35m'
GREEN = f'{ESC}[32m'
BLUE = f'{ESC}[34m'
RED = f'{ESC}[31m'
WHITE = f'{ESC}[37m'
BG_CYAN = f'{ESC}[46m'
BG_YELLOW = f'{ESC}[43m'
BG_MAGENTA = f'{ESC}[45m'
BG_GREEN = f'{ESC}[42m'
BG_BLUE = f'{ESC}[44m'
BG_RED = f'{ESC}[41m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_towers_color(towers, poles, step, total, max_disks):
    clear_screen()
    
    colors = [CYAN, YELLOW, MAGENTA, GREEN, BLUE, RED]
    bg_colors = [BG_CYAN, BG_YELLOW, BG_MAGENTA, BG_GREEN, BG_BLUE, BG_RED]
    
    width = 70
    print(f"\n{BOLD}{CYAN}╔{'═' * (width - 2)}╗{RESET}")
    print(f"{BOLD}{CYAN}║{RESET}{WHITE}{BOLD}           🏛️  하노이의 탑 - {max_disks}개 원반           {RESET}{BOLD}{CYAN}║{RESET}")
    print(f"{BOLD}{CYAN}╠{'═' * (width - 2)}╣{RESET}")
    
    pct = int((step / total) * 100) if total > 0 else 100
    bar_len = 30
    filled = int((step / total) * bar_len) if total > 0 else bar_len
    progress_bar = f"{GREEN}{'█' * filled}{RESET}{WHITE}{'░' * (bar_len - filled)}{RESET}"
    
    print(f"{BOLD}{CYAN}║{RESET}   Progress: [{progress_bar}] {pct:3d}%   {BOLD}{CYAN}║{RESET}")
    print(f"{BOLD}{CYAN}╠{'═' * (width - 2)}╣{RESET}")
    
    move_info = f"Step {step} / {total}"
    if step > 0 and step <= total:
        _, frm, to = None, None, None
        for i, h in enumerate(history[:step + 1]):
            if h[1] is not None:
                _, frm, to = h
        if frm and to:
            move_info += f"  ( {frm} → {to} )"
    
    print(f"{BOLD}{CYAN}║{RESET}{WHITE}   {move_info:<{width - 6}} {RESET}{BOLD}{CYAN}║{RESET}")
    print(f"{BOLD}{CYAN}╚{'═' * (width - 2)}╝{RESET}\n")
    
    max_height = max(len(towers[poles.index(p)]) for p in poles)
    
    print()
    for level in range(max_height - 1, -1, -1):
        line = "     "
        for i, pole in enumerate(poles):
            if level < len(towers[i]):
                disk = towers[i][level]
                color = colors[(disk - 1) % len(colors)]
                bg = bg_colors[(disk - 1) % len(bg_colors)]
                w = disk * 4
                disk_str = f"{bg}{color}{BOLD}{'▄' * w}{RESET}"
                line += f"  {disk_str}  "
            else:
                line += f" {CYAN}{BOLD}│{RESET}    "
        print(line)
    
    pole_line = "     "
    for i, pole in enumerate(poles):
        c = colors[i]
        pole_str = f"{c}{BOLD}┌{'─' * 12}┐{RESET}"
        pole_line += f"  {pole_str}  "
    print(pole_line)
    
    name_line = "     "
    for i, pole in enumerate(poles):
        c = colors[i]
        name_line += f"  {c}{BOLD}  {pole}  {RESET}  "
    print(name_line)
    
    print(f"\n{GREEN}└──────────────────────────────────────────────────────┘{RESET}\n")
    
    bar = "    " + "─" * 55
    print(f"{CYAN}{bar}{RESET}\n")
    
    if step == total:
        print(f"      {GREEN}{BOLD}🎉 축하합니다! 모든 원반을 목표 기둥으로 이동했습니다!{RESET}\n")
    
    print(f"  {WHITE}명령어:{RESET}")
    print(f"    {GREEN}[N]{RESET} 다음 이동  {YELLOW}[P]{RESET} 이전 이동  {BLUE}[F]{RESET} 마지막  {MAGENTA}[B]{RESET} 처음")
    print(f"    {CYAN}[G n]{RESET} n번 이동으로 이동  {RED}[Q]{RESET} 종료  {WHITE}[R]{RESET} 처음부터\n")

history = []

def hanoi_solve(n, from_pole, to_pole, aux_pole):
    global history
    towers = {
        'A': list(range(n, 0, -1)),
        'B': [],
        'C': []
    }
    poles = ['A', 'B', 'C']
    history = [([list(towers[p]) for p in poles], None, None)]
    
    def solve(n, frm, to, aux):
        if n == 1:
            disk = towers[frm].pop()
            towers[to].append(disk)
            history.append(([list(towers[p]) for p in poles], frm, to))
        else:
            solve(n - 1, frm, aux, to)
            disk = towers[frm].pop()
            towers[to].append(disk)
            history.append(([list(towers[p]) for p in poles], frm, to))
            solve(n - 1, aux, to, frm)
    
    solve(n, from_pole, to_pole, aux_pole)
    return poles, n

def interactive_mode(poles, max_disks):
    total = len(history) - 1
    current = 0
    
    while True:
        towers = [list(history[current][0][poles.index(p)]) for p in poles]
        print_towers_color(towers, poles, current, total, max_disks)
        
        try:
            cmd = input(f"\n  ▶ 명령어 입력: ").strip().lower()
            
            if cmd == 'n':
                if current < total:
                    current += 1
            elif cmd == 'p':
                if current > 0:
                    current -= 1
            elif cmd.startswith('g '):
                try:
                    target = int(cmd.split()[1])
                    if 0 <= target <= total:
                        current = target
                except:
                    pass
            elif cmd == 'f':
                current = total
            elif cmd == 'b':
                current = 0
            elif cmd == 'r':
                current = 0
            elif cmd == 'q':
                clear_screen()
                print(f"\n  {GREEN}이용해 주셔서 감사합니다! 👋{RESET}\n")
                break
                
        except (EOFError, KeyboardInterrupt):
            break

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    poles, max_disks = hanoi_solve(n, 'A', 'C', 'B')
    interactive_mode(poles, max_disks)
