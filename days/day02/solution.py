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
    opp = int(opponent.lower().translate(table))
    myh = int(my_hand.lower().translate(table))
    # (R)ock (P)aper (S)cissors
    if myh == opp:
        return 3 + HANDS[myh]
    # Won condition
    if myh == (opp + 1) % 3:
        return 6 + HANDS[myh]
    return 0 + HANDS[myh]


def part_a(puzzle: str) -> str:
    games = [get_score(s[0], s[2]) for s in puzzle.splitlines() if s]
    return str(sum(games))


def part_b(puzzle: str) -> str:
    # In this version, the second part is what we should do
    # X: Lose
    # Y: Draw
    # Z: Win

    # We will throw our hands depending on the opponent's hand
    games = [s for s in puzzle.splitlines() if s]
    score = 0
    for game in games:
        opp = int(game[0].lower().translate(table))
        direction = game[2]
        if direction == "Y":
            # Make it draw
            score += 3 + HANDS[opp]
            continue

        # big brain time
        add = 1 if direction == "Z" else 2
        hand = 6 if direction == "Z" else 0
        hidx = (opp + add) % 3
        score += hand + HANDS[hidx]
    return str(score)


if __name__ == "__main__":
    puzzle = CURRENT_DIR / "input.txt"
    puzzle_input = puzzle.read_text()
    print(part_a(puzzle_input))
    print(part_b(puzzle_input))
