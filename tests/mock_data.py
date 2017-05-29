articles = {
    'Cooking': [
        'Cooking101',
        'How to Bake Bread',
        'The Perfect Pasta'
    ],
    'Engineering': [
        'Kafka: The Definitive Guide',
        'Building Real-Time Data Pipelines',
        'Clean Code'
    ],
    'Sports': [
        'How To Run A Marathon'
    ]
}

alice_feeds = ['Sports', 'Engineering']
bob_feeds = ['Sports', 'Cooking', 'Movies']
charlie_feeds = ['Sports', 'Engineering']

def get_mock_feeds():
    return (alice_feeds[:], bob_feeds[:], charlie_feeds[:])

def get_mock_articles():
    return (articles['Cooking'][:], articles['Engineering'][:], articles['Sports'][:])
