examples= [
    {
        "question": "What are the articles connected to the given titles?",
        "query": "MATCH (a:Article)-[:HAS_TITLE]->(t:Title) WHERE a.article_id = 'W2036181141' RETURN a.article_id, a.title",
    },
    {
        "question": "Find author of the articles that are connected to the given titles?",
        "query": "MATCH (a:Article)-[:HAS_TITLE]->(t:Title) WHERE a.article_id = 'W2036181141' MATCH (a)-[:WRITTEN_BY]->(au:Author) RETURN au.author_names",
    },
    {
        "question": "What are the articles connected to the given titles?",
        "query": "MATCH (a:Article)-[:HAS_TITLE]->(t:Title) WHERE a.article_id = 'W2036181141' MATCH (a)-[:WRITTEN_BY]->(au:Author)-[:AFFILLIATED_TO]-(inst:Institution) RETURN a.title, au.author_names, inst.institution_name",
    },
    {
        "question": "How many articles have citation > 50? Return their title and authors",
        "query": "MATCH (a:Article)-[:WRITTEN_BY]->(au:Author) WHERE a.citation_count > 50  RETURN a.title, au.author_names",
    },
    {
        "question": "What are the articles published in a specific year?",
        "query": "MATCH (a:Article) WHERE a.publication_year = year RETURN a.title",
    },
    {
        "question": "How many articles does a particular author have?",
        "query": "MATCH (au:Author)<-[:WRITTEN_BY]-(a:Article) WHERE au.name = 'Author Name' RETURN count(a)",
    },
    {
        "question": "What are the articles published in a specific journal?",
        "query": "MATCH (a:Article)-[:PUBLISHED_IN]-(j:Journal) WHERE j.journal_name = 'Journal Name' RETURN a.title",
    },
    {
        "question": "What are the articles authored by a specific author?", 
        "query": "MATCH (author:Author)-[:WRITTEN_BY]->(a:Article) WHERE author.author_names = 'Author Name' RETURN a.title",
    },
    {
        "question": "How many authors collaborated on a particular article?",
        "query": "MATCH (a:Article)-[:WRITTEN_BY]-(au:Author) WHERE a.title = 'Title of the the article' RETURN count(au.author_names)",
    },
    {
        "question": "Name the author who author a particular article and their institutions",
        "query": "MATCH (a:Article)-[:WRITTEN_BY]-(au:Author) WHERE a.title = 'Title of the the article' RETURN au.author_names, au.institution_name",
    },
    {
        "question": "What institutions are affiliated with a particular author?", 
        "query": "MATCH (author:Author)-[:AFFILLIATED_TO]-(institution:Institution) WHERE author.author_names = 'Author Name' RETURN institution.institution_name",
    },
    {
        "question": "How many authors are affiliated with a particular institution?",
        "query": "MATCH (i:Institution)<-[:AFFILLIATED_TO]-(au:Author) WHERE i.institution_name = 'University Name' RETURN count(au)",
    },
    {
        "question": "Find authors who are affiliated to a particular insitution",
        "query": "MATCH (i:Institution)<-[:AFFILLIATED_TO]-(au:Author) WHERE i.institution_name = 'University Name' RETURN au.author_names",
    },
    {
        "question": "What are the articles authored by authors affiliated with a University of Sheffield?", 
        "query": "MATCH (i:Institution)<-[:AFFILLIATED_TO]-(au:Author)<-[:WRITTEN_BY]->(a:Article) WHERE i.institution_name = 'University of Sheffield' RETURN a.title",
    },
    {
        "question": "What are the top 10 cited articles authored by authors affiliated with an institution?",
        "query": "MATCH (i:Institution)-[:AFFILLIATED_TO]-(au:Author)-[:WRITTEN_BY]-(a:Article) WHERE i.institution_name='University of California, Santa Barbara' WITH a ORDER BY a.citation_count DESC RETURN a.title, a.citation_count LIMIT 10",
    },
    {
        "question": "What are the top journals by the number of articles published?",
        "query": "MATCH (j:Journal)-[:PUBLISHED_IN]-(a:Article) RETURN j.journal_name, count(a) AS num_articles ORDER BY num_articles DESC LIMIT 10",
    },
    {
        "question": "What are the top 10 cited articles by a particular journal", 
        "query": "MATCH (j:Journal)-[:PUBLISHED_IN]-(a:Article) WHERE j.journal_name='The Plant Journal' WITH a ORDER BY a.citation_count DESC RETURN a.title LIMIT 10",
    },
    {
        "question": "What are the authors of articles with a specific title?",
        "query": "MATCH (title:Title)-[:HAS_TITLE]-(a:Article)-[:WRITTEN_BY]-(au:Author) WHERE title.text = 'Title of the article' RETURN a.title, au.author_names",
    },
    {
        "question": "How many articles were published in a specific year, e.g 2020?",
        "query": "MATCH (a:Article)-[p:YEAR_PUBLISHED]-(y:Year {publication_year:2020}) RETURN a.title",
    },
    {
        "question": "Which journal publication published the most article in a specific year, e.g 2020", 
        "query": "MATCH (j:Journal)-[:PUBLISHED_IN]-(a:Article) WHERE a.publication_year=2020 WITH j, count(a) AS num_articles ORDER BY num_articles DESC RETURN j.journal_name, num_articles",
    },
    {
        "question": "What are the articles published after a specific year?",
        "query": "MATCH (a:Article) WHERE a.publication_year > year RETURN a.title",
    },
    {
        "question": "What are the top cited articles published after a specific year, e.g 2010?",
        "query": "MATCH (a:Article) WHERE a.publication_year > 2010 WITH a ORDER BY a.citation_count DESC RETURN a.title, a.citation_count LIMIT 10",
    },
    {
        "question": "Which articles were funded by a specific funder, e.g National Science Foundation?", 
        "query": "MATCH (f:Funder)-[:FUNDED_BY]-(a:Article) WHERE f.funder_name = 'National Science Foundation' RETURN a.title",
    },
    {
        "question": "What are the funders of a specific article?",
        "query": "MATCH (f:Funder)<-[:FUNDED_BY]-(a:Article) WHERE a.title = 'Title of the article' RETURN f.funder_name",
    },
    {
        "question": "Where is a specific intitution located?",
        "query": "MATCH (i:Institution) WHERE i.institution_name='Name of the Insitution' RETURN i.country, i.city",
    },
    {
        "question": "Provide the list of institution from a specific country, e.g Japan", 
        "query": "MATCH (i:Institution)-[:IS_FROM]-(c:Country) WHERE c.country_name='Japan' RETURN i.country, i.institution_name ",
    },
    {
        "question": "How many articles are authored by authors from a specific country, e.g Japan?",
        "query": "MATCH (c:Country)-[:IS_FROM]-(i:Institution)-[:AFFILLIATED_TO]-(au:Author)-[:WRITTEN_BY]-(a:Article) WHERE c.country_name = 'Japan' RETURN count(a)",
    },
    {
        "question": "What are the top cited articles from insitutions from a specific country, e.g Japan",
        "query": "MATCH (c:Country)-[:IS_FROM]-(i:Institution)-[:AFFILLIATED_TO]-(au:Author)-[:WRITTEN_BY]-(a:Article) WHERE c.country_name = 'Japan' WITH c, a ORDER BY a.citation_count DESC RETURN DISTINCT(a.title), a.citation_count, c.country_name",
    },
    {
        "question": "List the top cited articles with authors from institution from a specific country, e.g Japan", 
        "query": "MATCH (i:Institution)-[:IS_FROM]-(c:Country) WHERE c.country_name='Japan' WITH i, c MATCH (i)-[:AFFILLIATED_TO]-(au:Author)-:WRITTEN_BY]-(a:Article) WITH a, au, c ORDER BY a.citation_count DESC RETURN DISTINCT(a.title) AS Title, a.citation_count AS Citations, COLLECT(au.author_names) LIMIT 10",
    },
]