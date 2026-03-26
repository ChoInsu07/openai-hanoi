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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

history = []

def print_towers_color(towers, poles, step, total, max_disks):
    clear_screen()
    
    colors = [CYAN, YELLOW, MAGENTA]
    disk_colors = [
        f'{ESC}[41m', f'{ESC}[42m', f'{ESC}[43m',
        f'{ESC}[44m', f'{ESC}[45m', f'{ESC}[46m'
    ]
    
    print(f"\n{BOLD}{CYAN}┌────────────────────────────────────────────────────────┐{RESET}")
    print(f"{BOLD}{CYAN}│{RESET}           🏛️  하노이의 탑 - {max_disks}개 원반                    {BOLD}{CYAN}│{RESET}")
    print(f"{BOLD}{CYAN}├────────────────────────────────────────────────────────┤{RESET}")
    
    pct = int((step / total) * 100) if total > 0 else 100
    bar_len = 25
    filled = int((step / total) * bar_len) if total > 0 else bar_len
    progress_bar = f"{GREEN}{'█' * filled}{RESET}{WHITE}{'░' * (bar_len - filled)}{RESET}"
    
    move_str = ""
    if step > 0 and step <= total:
        for h in history[:step + 1]:
            if h[1] is not None:
                _, frm, to = h
                move_str = f" ({frm} → {to})"
    
    step_str = f"Step {step}/{total}{move_str}"
    print(f"{BOLD}{CYAN}│{RESET}  Progress: [{progress_bar}] {pct:3d}%                         {BOLD}{CYAN}│{RESET}")
    print(f"{BOLD}{CYAN}│{RESET}  {step_str:<54} {BOLD}{CYAN}│{RESET}")
    print(f"{BOLD}{CYAN}└────────────────────────────────────────────────────────┘{RESET}")
    
    max_height = max(len(towers[i]) for i in range(len(poles)))
    base_width = max_disks * 3
    inner_width = base_width + 2
    
    print()
    print("  ", end="")
    for i, pole in enumerate(poles):
        c = colors[i]
        sep = " " if i > 0 else ""
        print(f"{sep}{c}┌{'─' * inner_width}┐", end="")
    print()
    
    for level in range(max_height - 1, -1, -1):
        line = "  "
        for i, pole in enumerate(poles):
            if level < len(towers[i]):
                disk = towers[i][level]
                dc = disk_colors[(disk - 1) % len(disk_colors)]
                w = disk * 3
                padding = (base_width - w) // 2
                content = f"{' ' * padding}{dc}{'█' * w}{RESET}"
            else:
                content = ""
            c = colors[i]
            sep = " " if i > 0 else ""
            line += f"{sep}{c}│{content:^{inner_width}}│"
        print(line)
    
    name_line = "  "
    for i, pole in enumerate(poles):
        c = colors[i]
        sep = " " if i > 0 else ""
        name_line += f"{sep}{c}│{BOLD}{pole:^{inner_width}}{RESET}│"
    print(name_line)
    
    print("  ", end="")
    for i, pole in enumerate(poles):
        c = colors[i]
        sep = " " if i > 0 else ""
        print(f"{sep}{c}└{'─' * inner_width}┘", end="")
    print()
    
    print()
    
    if step == total:
        print(f"  {GREEN}{BOLD}🎉 축하합니다! 모든 원반을 목표 기둥으로 이동했습니다!{RESET}")
        print()
    
    print(f"  {WHITE}명령어:{RESET}")
    print(f"    {GREEN}[N]{RESET} 다음  {YELLOW}[P]{RESET} 이전  {BLUE}[F]{RESET} 끝  {MAGENTA}[B]{RESET} 처음")
    print(f"    {CYAN}[G n]{RESET} 특정 단계로 이동  {RED}[Q]{RESET} 종료")
    print()

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
            cmd = input("  ▶ ").strip().lower()
            
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
