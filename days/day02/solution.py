from pathlib import Path

CURRENT_DIR = Path(__file__).absolute().parent

HANDS = {
    # R
    0: 1,
    # P
    1: 2,
    # S
    2: 3,
}
table = "abcxyz".maketrans("abcxyz", "012012")


def get_score(opponent: str, my_hand: str):
    # (R)ock (P)aper (S)cissors
    if (myh := int(my_hand.lower().translate(table))) == (opp := int(opponent.lower().translate(table))):
        return 3 + HANDS[myh]
    # Won condition
    if myh == (opp + 1) % 3:
        return 6 + HANDS[myh]
    return 0 + HANDS[myh]


def part_a(puzzle: str) -> str:
    games = [get_score(s[0], s[2]) for s in puzzle.splitlines() if s]
    return str(sum(games))


def part_b(puzzle: str) -> str:
    # We will throw our hands depending on the opponent's hand
    games = [(int(s[0].lower().translate(table)), int(s[2].lower().translate(table))) for s in puzzle.splitlines() if s]
    score = 0
    for opp, own in games:
        if own == 1:
            score += 3 + HANDS[opp]
            continue

        own_s = 6 if own == 2 else 0
        hidx = (opp + (1 if own == 2 else 2)) % 3
        score += own_s + HANDS[hidx]
    return str(score)


if __name__ == "__main__":
    puzzle = CURRENT_DIR / "input.txt"
    puzzle_input = puzzle.read_text()
    print(part_a(puzzle_input))
    print(part_b(puzzle_input))
