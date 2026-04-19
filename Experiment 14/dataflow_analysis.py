class BasicBlock:
    def __init__(self, name, gen, kill, preds):
        self.name = name
        self.gen = set(gen)
        self.kill = set(kill)
        self.preds = preds
        self.ins = set()
        self.outs = set()

def reaching_definitions(blocks):
    changed = True

    while changed:
        changed = False
        for block in blocks.values():
            new_in = set()
            for pred in block.preds:
                new_in |= blocks[pred].outs

            new_out = block.gen | (new_in - block.kill)

            if new_in != block.ins or new_out != block.outs:
                block.ins = new_in
                block.outs = new_out
                changed = True

def display_results(blocks):
    print("\nReaching Definitions Analysis")
    print("-" * 40)
    for name, block in blocks.items():
        print(f"Block: {name}")
        print(f"GEN  = {block.gen}")
        print(f"KILL = {block.kill}")
        print(f"IN   = {block.ins}")
        print(f"OUT  = {block.outs}")
        print()

def main():
    blocks = {
        "B1": BasicBlock("B1", {"d1", "d2"}, set(), []),
        "B2": BasicBlock("B2", {"d3"}, {"d1"}, ["B1"]),
        "B3": BasicBlock("B3", {"d4"}, {"d2"}, ["B1"]),
        "B4": BasicBlock("B4", {"d5"}, {"d3", "d4"}, ["B2", "B3"])
    }

    reaching_definitions(blocks)
    display_results(blocks)

if __name__ == "__main__":
    main()
