from app.home.utils.load_rankings_cache import load_rankings_cache

rankings_cache = {
        'Consumer Discretionary': load_rankings_cache('Consumer Discretionary'),
        'Consumer Staples': load_rankings_cache('Consumer Staples'),
        'Energy': load_rankings_cache('Energy'),
        'Financial Services': load_rankings_cache('Financial Services'),
        'Healthcare': load_rankings_cache('Healthcare'),
        'Materials & Processing': load_rankings_cache('Materials & Processing'),
        'Producer Durables': load_rankings_cache('Producer Durables'),
        'Technology': load_rankings_cache('Technology'),
        'Utilities': load_rankings_cache('Utilities'),
    }
