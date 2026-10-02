#!/usr/bin/env python3
'AI Semantic Cataloguer (read-through): Read the only trade name, use the semantics of the fixed 7 subject and print the full allocation for review.\nNo final file, only review tables + classifications JSON to/tmp/classify result.json.'
import json, sys

NAMES_JSON = "/tmp/names_out.json"

SUBJECTS = {
    "1403.01.01": 'A herbal food.',
    "1403.01.02": 'Vegetables and vegetables',
    "1403.01.03": 'Main foods',
    "1403.01.04": 'Food and oil.',
    "1403.01.05": 'Drinking materials',
    "1403.01.06": 'Packaging group',
    "1403.01.07": 'Low-value perishable',
}

# Visible exception over: - (code, subject, confidence, review, review)
# It's a difficult item for a rule that can be miscalculated or manually reviewed.
OVERRIDE = {
    # "Staff" trap: Not meat.
    'Garlic.':        ("1403.01.02", 'Vegetables and vegetables', "high", False, 'Garlic/garlicate, onion-based vegetables'),
    'Garlic bags.':    ("1403.01.02", 'Vegetables and vegetables', "high", False, 'Garlic bags, garlic vegetables.'),
    'Ginger.':        ("1403.01.02", 'Vegetables and vegetables', "high", False, 'Ginger, cedar.'),
    'Chon!':        ("1403.01.02", 'Vegetables and vegetables', "high", False, 'Ginger, cedar.'),
    'Nam-Gung!':        ("1403.01.02", 'Vegetables and vegetables', "high", False, 'Nan Ginger, cedar vegetables.'),
    'Dry onions.':    ("1403.01.04", 'Food and oil.', "high", False, 'Dry onions, dry spices.'),
    'Horseshoe.':      ("1403.01.02", 'Vegetables and vegetables', "med", True,  'Horseshoe (soft) meat, treated by vegetables, recommended for review'),
    # Liquor: No "diens" in category 7, classified as closest to the drinking material and reviewed
    'Red Star 2-Op 52 degrees.': ("1403.01.05", 'Drinking materials', "low", True, "White wine is a drinker, classified as a drinker's raw material, but is recommended for manual review"),
    # sandwich/bread: ready-made pasta, for staple food
    'Portuguese sandwich.':  ("1403.01.03", 'Main foods', "med", True, 'The food is a face-to-face sandwich, which is the main food type, and is recommended for review.'),
    'Bread by the intestines.':  ("1403.01.03", 'Main foods', "high", False, 'Bread ready-to-eat pasta'),
    # Pepper: peppers are vegetables, dry/sauce/oil is sauce
    'Paprika Day.':      ("1403.01.04", 'Food and oil.', "high", False, 'Dry peppers, spices.'),
    # Main foods, powder/salin
    'Windmills, powdered 2':   ("1403.01.03", 'Main foods', "high", False, 'Potassium (salmon) and powdered staples'),
    'Little red potato powder.': ("1403.01.03", 'Main foods', "high", False, 'Potato starch, powdered staple.'),
    'Scratch.':  ("1403.01.03", 'Main foods', "high", False, 'Pink fries, powdered staples.'),
    # Bean products (which contain the word "oil" but are essentially soy products, which need to be pre-covered or otherwise be sentenced to food and oil.
    'Tofu oil. Tofu.': ("1403.01.02", 'Vegetables and vegetables', "high", False, 'Tofu is a tofu product, non-eat oil'),
    # Border blurr: classified as closest to the subject and marked for manual recovery Nuclear
    'Corn grains':      ("1403.01.03", 'Main foods', "med", True,  'Corn with staple/vegetable properties, temporarily classified as staple, recommended for review'),
    'A corn bar with leather.':  ("1403.01.03", 'Main foods', "med", True,  'Corn with staple/vegetable properties, temporarily classified as staple, recommended for review'),
    '- The sweet potatoes.':    ("1403.01.03", 'Main foods', "med", True,  'Potato and vegetable properties, temporarily classified as staple, recommended for review'),
    'Two long hearts and potatoes.': ("1403.01.03", 'Main foods', "med", True, 'Potato and vegetable properties, temporarily classified as staple, recommended for review'),
    'Go to the twilight.': ("1403.01.03", 'Main foods', "med", True, 'Potato and vegetable properties, temporarily classified as staple, recommended for review'),
}

def classify(norm: str, orig: str):
    if norm in OVERRIDE:
        c, s, conf, rev, reason = OVERRIDE[norm]
        return c, s, conf, rev, reason

    # Low-value perishable
    for k in ('An apron.', 'Cleaning.', 'Cleaning agent', 'Heavy oil.', 'Steel ball.'):
        if k in norm:
            return "1403.01.07", 'Low-value perishable', "high", False, f"\"Han.\"{k}\", non-food consumables"

    # Packaging group
    for k in ('Pack your bags.', "- I'm not gonna be able to get a skin mask."):
        if k in norm:
            return "1403.01.06", 'Packaging group', "high", False, f"\"Han.\"{k}\", food packaging"

    # Drinking materials
    for k in ('Milk', 'Light milk.', 'Occurate.', 'Milk.', '- Vitamins.', 'Coconut.'):
        if k in norm:
            return "1403.01.05", 'Drinking materials', "high", False, f"\"Han.\"{k}\" Drinking materials"

    # Main foods -- Note: No nudity packs, or "packages" are miscalculated; only match the end of the line.
    for k in ('- Chammy.', '-Scammy.', 'Pyro-rice.', '- Meow.', 'River powder', 'Flour', '- Brick.', 'Flounder',
              'Oil bars', 'Bread.', 'Fans', 'Pink bars', 'Corn', 'Potatoes.', '- Oh, my God.',
              'Black rice', 'Red rice', 'A green cabbage.', '- A meat bag.', 'Noodles.'):
        if k in norm:
            return "1403.01.03", 'Main foods', "high", False, f"\"Han.\"{k}\" Main foods, such as rice flour/pack spot"

    # Food and oil (saline and sweets, etc.)
    for k in ('Oil', 'Soy sauce.', 'Jealousy.', 'Soy sauce.', 'Sugar', 'Taste.', 'Fever.', 'Pepper sauce.', 'Pepper powder.',
              'Chicken powder.', 'Salt chicken powder.', "It's so good.", 'Base', 'Oil oil.', 'Doudou.', 'Sand tea.',
              'Shang.', 'Eight.', 'Cinnamon', 'Orange oil.', 'Pepper oil.', 'Pepper powder.', 'Old Scrap.', 'Smoking.'):
        if k in norm:
            return "1403.01.04", 'Food and oil.', "high", False, f"\"Han.\"{k}\"..saline sauce/spicin"

    # Fresh peppers -- after the oil, the peppers are partially edged, and here they are.
    for k in ('Pepper.', 'Paprika.', 'Cyanapple.', '-Piperium.', '-Pretty peppers.', 'Cyclops.', '- Piper.',
              'Miho.', 'Hunan pepper.', 'Paprika.', 'Hainan pepper.'):
        if k in norm:
            return "1403.01.02", 'Vegetables and vegetables', "high", False, f"\"Han.\"{k}\" Fresh peppers are vegetables."

    # Salmon (polyfish eggs, seafood and meat products)
    for k in ('Chicken.', 'Pigs.', 'Cow.', 'Duck.', 'Fish', 'Shrimp.', 'Crabs.', 'Meat.', 'Intestines', '- The ribs.', 'Liver',
              'Foot.', 'Whoa.', 'Legs.', '- Meat.', 'Maru.', 'Volume', 'Thread', 'Eggs.', 'The fish.', 'The ropha.',
              'Nine-bread.', 'Strawfish.', 'Yellowfish.', 'Akirkfish.', 'Solar fish.', 'Skullfish.', 'Ink fish.',
              "A pig's hand.", 'Burning.', 'Hot dogs.', 'Lion Head.', "- It's a bitter intestine.", 'Five flowers.', 'Skinny meat.', 'Ridge.',
              'A plum.', 'Meatloaf.', 'Meatloaf.', 'Fresh chops.', 'Cut off the pigs.', 'Lion Head.'):
        if k in norm:
            return "1403.01.01", 'A herbal food.', "high", False, f"\"Han.\"{k}\". Meat fish eggs/meat products"

    # Bottom: The remainder are explicitly not compulsory for vegetables by vegetable accelerants (vegetable/peasant/ pickles/ mushrooms/dry) Nuclear
    return "1403.01.02", 'Vegetables and vegetables', "high", False, 'Vegetables/peasers/chords/ mushrooms/dry products, classified as vegetable accelerants'


def main():
    data = json.load(open(NAMES_JSON, encoding="utf-8"))
    names = data["unique_names"]
    classifications = {}
    print(f"{'idx':>3} | {'subject':<10} | {'rev':<3} | {'name':<22} | reason")
    print("-" * 100)
    for i, n in enumerate(names):
        norm = n["normalized"]; orig = n["original"]
        c, s, conf, rev, reason = classify(norm, orig)
        classifications[norm] = {"code": c, "subject": s,
                                 "confidence": conf, "review": rev, "reason": reason}
        print(f"{i:>3} | {s:<10} | {'Y' if rev else '':<3} | {norm:<22} | {reason}")

    # Statistics
    from collections import Counter
    cnt = Counter(v["subject"] for v in classifications.values())
    print("♪ ♪ I'm gonna be ♪")
    for code, subj in SUBJECTS.items():
        print(f"  {code} {subj}: {cnt.get(subj,0)}It's the only commodity.")
    reviews = [k for k, v in classifications.items() if v["review"]]
    print(f"\n Requires manual review (%){len(reviews)}）：")
    for k in reviews:
        print("  -", k, "|", classifications[k]["subject"], "|", classifications[k]["reason"])

    out = {"header_idx": 1, "col_name_idx": 4, "insert_idx": 5,
           "classifications": classifications}
    json.dump(out, open("/tmp/classify_result.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print('Written /tmp/classify result.json')


if __name__ == "__main__":
    main()
