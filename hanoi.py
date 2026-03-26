import sys

def hanoi(n, from_pole, to_pole, aux_pole, towers, moves):
    if n == 1:
        disk = towers[from_pole].pop()
        towers[to_pole].append(disk)
        moves.append((n, from_pole, to_pole))
    else:
        hanoi(n - 1, from_pole, aux_pole, to_pole, towers, moves)
        disk = towers[from_pole].pop()
        towers[to_pole].append(disk)
        moves.append((n, from_pole, to_pole))
        hanoi(n - 1, aux_pole, to_pole, from_pole, towers, moves)

def print_towers(towers, poles, step, total):
    print(f"\n{'='*50}")
    print(f"Step {step}/{total}")
    print('='*50)
    
    max_height = max(len(towers[p]) for p in poles)
    
    for level in range(max_height - 1, -1, -1):
        row = ""
        for pole in poles:
            if level < len(towers[pole]):
                disk = towers[pole][level]
                width = disk * 2 - 1
                row += f"{'█' * width:^15}"
            else:
                row += f"{'|':^15}"
        print(row)
    
    print(' '.join(f"{p:^15}" for p in poles))
    print('─' * 50)

def solve_hanoi(n):
    towers = {
        'A': list(range(n, 0, -1)),
        'B': [],
        'C': []
    }
    poles = ['A', 'B', 'C']
    moves = []
    
    total_moves = 2 ** n - 1
    print(f"\n🏛️  하노이의 탑 - {n}개의 원반")
    print(f"   A → C (B를 보조 기둥으로 사용)")
    print(f"   총 {total_moves}번 이동 필요\n")
    
    input("시작하려면 Enter를 누르세요...")
    
    hanoi(n, 'A', 'C', 'B', towers, moves)
    
    towers = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}
    
    for i, (disk, frm, to) in enumerate(moves, 1):
        towers[frm].pop()
        towers[to].append(disk)
        print_towers(towers, poles, i, total_moves)
    
    print(f"\n✅ 완료! {n}개의 원반을 {total_moves}번 만에 모두 이동했습니다.\n")

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    solve_hanoi(n)
