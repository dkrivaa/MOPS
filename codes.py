def organization_codes():
    # column 12 in files (0 based index)
    return {
        'ministry': [750, 5230],
        'witness': [755],
        'fire': [760],
        'prison': [770, 5240],
        'police': [780, 5250]
    }

def wage_codes():
    # columns 21 and 24 in files (0 based index)
    return [1, 30]


def budget_types():
    return {
        'original': 'מקורי',
        'approved': 'מאושר',
        'executed': 'ביצוע',
    }