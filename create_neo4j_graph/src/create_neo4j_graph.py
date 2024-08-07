import os, json
import argparse
import pandas as pd
from neo4j import GraphDatabase

class GraphNodeCreator:
    def __init__(self, neo4j_auradb_uri, aura_username, aura_password):
        self.neo4j_auradb_uri = neo4j_auradb_uri
        self.aura_username = aura_username
        self.aura_password = aura_password

    # Test neo4j connection
    def test_neo4j_connection(self, query):
        driver = GraphDatabase.driver(self.neo4j_auradb_uri, auth=(self.aura_username, self.aura_password))
        with driver.session() as session:
            result = session.run(query)
            return result.data()

    # Functions to generate Cypher query for creating a node
    def create_single_node_query(self, label, properties):
        '''
        Create a single cypher query statement for a new node with label and properties
        '''        
        props_str = ', '.join([f"{key}: ${key}" for key in properties.keys()])
        query = f"CREATE (:{label} {{{props_str}}})"        
        return query

    def update_node_query(self, label, identifier_key, identifier_value, properties):
        '''
        Create cypher statement to add properties on pre-existing nodes
        '''
        props_str = ', '.join([f"{key}: ${key}" for key in properties.keys()])
        query = f"MATCH (n:{label} {{{identifier_key}: '{identifier_value}'}}) SET n += {{{props_str}}}"
        return query
    
    def delete_graph(query):
        '''Delete graph nodes and relationships''' 
        ''' e.g'''
        '''MATCH (n) DETACH DELETE n;'''
        '''MATCH ()-[r]->() DELETE r;'''
        with driver.session() as session:
            result = session.run(query)
            return result.data()

    
    
    def create_nodes(self, queries, properties):
        '''
        Submit the cypher statement to the Neo4j db and create a new node 
        '''
        driver = GraphDatabase.driver(self.neo4j_auradb_uri, auth=(self.aura_username, self.aura_password))

        # Run queries using the Neo4j driver
        with driver.session() as session:
            for query, kv in zip(queries, properties):
                session.run(query, **kv)
        return None
    
    #################
    """ 
    Define functions to iterate over DataFrame to create list of queries for nodes
    
    Input: A dataframe containing OpenAlex Metadata
    Output: List of queries to be submitted to neo4j
    """
    def create_article_nodes(self, df):
        create_queries = []
        properties = []
        for _, row in df.iterrows():
            label = 'Article'
            kv = {
                'article_id' : row['id']
                ,'title' : row['title']
                ,'journal_name' : row['journal']
                ,'journal_id' : row['journal']
                ,'publication_year' : int(row['publication_year'])
                ,'doi' : row['landing_page_url']
                ,'is_retracted' : row['is_retracted']
                ,'citation_count': row['citation_count']
                #,'citation_by_yr': row['citation_by_yr']
                #,'out_citations': [item.lstrip('https://openalex.org/') for item in row['referenced_works']]
                ,'in_citations': row['incoming_citations']
                #,'related_works' : [item.lstrip('https://openalex.org/') for item in row['related_works']]
                ,'abstract' : row['abstract']
                ,'topics' : row['topics_name']
                ,'funders': list(set(row['funders_list'][1]))
                ,'twitter': row['twitter']
                ,'reddit': row['reddit']

            } 
            query = self.create_single_node_query(label, kv)
            create_queries.append(query) 
            properties.append(kv)
        return create_queries, properties
    
    def create_title_nodes(self, df):
        create_queries = []
        properties = []
        for _, row in df.iterrows():
            label = 'Title'
            kv = {
                'title_id' : row['title_id']
                ,'text' : row['title'] 
                ,'article_id': row['id']
            }
            query = self.create_single_node_query(label, kv)
            create_queries.append(query)            
            properties.append(kv)
        return create_queries, properties
    
    def create_abstract_nodes(self, df):
        create_queries = []
        properties = []
        for index, row in df.iterrows():
            label = 'Abstract'
            kv = {
                'abstract_id' : row['abstract_id']
                ,'text' : row['abstract']        
            }
            query = self.create_single_node_query(label, kv)
            create_queries.append(query)            
            properties.append(kv)
        return create_queries, properties
    
    def create_topic_nodes(self, df):
        create_queries = []
        properties = []
        for index, row in df.iterrows():
            label = 'Topic'
            kv = {
                'topic_id' : row['topic_id']
                ,'text' : row['topics_name']        
            }
            query = self.create_single_node_query(label, kv)
            create_queries.append(query)            
            properties.append(kv)
        return create_queries, properties

    def create_journal_nodes(self, df):
        create_queries = []
        properties = []
        for index, row in df.iterrows():
            label = 'Journal'
            kv = {
                'journal_id' : row['journal_id']
                ,'journal_name' : row['journal']
                ,'issn' : row['issn']
                ,'sjr_score' : row['sjr_score']
                ,'h_index' : row['h_index']
                ,'sjr_best_quartile' : row['sjr_best_quartile']

            }
            query = self.create_single_node_query(label, kv)
            create_queries.append(query)            
            properties.append(kv)
        return create_queries, properties

    def create_date_nodes(self, df):
        create_queries = []
        properties = []
        for index, row in df.iterrows():
            label = 'Year'
            kv = {
                'year_id' : str(row['publication_year'])
                ,'publication_year' : row['publication_year']

            }
            query = self.create_single_node_query(label, kv)
            create_queries.append(query)            
            properties.append(kv)
        return create_queries, properties

    def create_author_nodes(self, df):
        create_queries = []
        properties = []
        for index, row in df.iterrows():
            label = 'Author'
            kv = {
                'author_id' : str(row['author_id'])
                ,'author_names' : row['author_name']
                ,'institution_id' : row['institution_id']
                ,'institution_name' : row['institution_name']

            }
            query = self.create_single_node_query(label, kv)
            create_queries.append(query)            
            properties.append(kv)
        return create_queries, properties

    def create_institution_nodes(self, df):
        create_queries = []
        properties = []
        for index, row in df.iterrows():
            label = 'Institution'
            kv = {
                'institution_id' : str(row['institution_id'])
                ,'institution_name' : row['institution_name']
                ,'institution_country_code' : row['institution_country_code']
                ,'country' : row['country']
                ,'city' : row['city']
                ,'latitude' : row['latitude']
                ,'longitude' : row['longitude']
                ,'institution_type' : row['institution_type']
                ,'homepage_url' : row['homepage_url']
                ,'works_count' : row['works_count']
                ,'cited_by_count' : row['cited_by_count']
                ,'associated_institution' : row['associated_institution_list']
            }
            query = self.create_single_node_query(label, kv)
            create_queries.append(query)            
            properties.append(kv)
        return create_queries, properties

    def create_funder_nodes(self, df):
        '''Note double for loop for funder data'''
        create_queries = []
        properties = []
        for index, row in df.iterrows():
            label = 'Funder'
            kv = {
                'funder_id' : row['funder_id']
                ,'funder_name': row['display_name']
                ,'country_code': row['country_code']
                ,'description': row['description']
                ,'alternate_titles': row['alternate_titles']
                ,'homepage' : row['homepage_url']
                ,'grants_count': row['grants_count']
                ,'h_index': row['summary_stats']['h_index']
                ,'i10_index': row['summary_stats']['i10_index'] 
                #,'2yr_mean_citedness': row['summary_stats']['2yr_mean_citedness']
                ,'cited_by_count': row['cited_by_count']
            }
            query = self.create_single_node_query(label, kv)
            create_queries.append(query)            
            properties.append(kv)
        return create_queries, properties

    def create_country_nodes(self, df):
        create_queries = []
        properties = []
        for index, row in df.iterrows():
            label = 'Country'
            kv = {
                'country_id' : row['institution_country_code']
                ,'country_name' : row['country']
            }
            query = self.create_single_node_query(label, kv)
            create_queries.append(query)            
            properties.append(kv)
        return create_queries, properties
    
############
    def update_funder_nodes(self, df):
        '''Function to add properties to existing node'''
        create_queries = []

        # Iterate over rows in the DataFrame and generate queries
        for index, row in df.iterrows():
            label = 'Funder'
            identifier_key = 'funder_id'
            identifier_value = row['funder_id']
            properties = {
                'country_code': row['country_code'],
                'homepage' : row['homepage_url'],
                'grants_count': row['grants_count'],
                'h_index': row['summary_stats']['h_index'],
                'i10_index': row['summary_stats']['i10_index'],        
            }   
            query = generate_update_query(label, identifier_key, identifier_value, properties)
            create_queries.append(query)
        return create_queries


    
class GraphRelationshipCreator:
    
    def __init__(self, neo4j_auradb_uri, aura_username, aura_password):
        self.neo4j_auradb_uri = neo4j_auradb_uri
        self.aura_username = aura_username
        self.aura_password = aura_password        

        
    def create_relationships(self, queries):
        driver = GraphDatabase.driver(self.neo4j_auradb_uri, auth=(self.aura_username, self.aura_password))
        # Run relationship creation queries
        with driver.session() as session:
            for query in queries:
                session.run(query)
        return None
    
    def create_single_relationship_query(self, start_node, end_node, relationship_label, **kwargs):
        start_node_id = kwargs.get('start_node_id')
        end_node_id = kwargs.get('end_node_id')
        start_label = kwargs.get('start_label')
        end_label = kwargs.get('end_label')

        query = f"""
        MATCH (a:{start_label} {{{start_node_id}: '{start_node}'}}), (b:{end_label} {{{end_node_id}: '{end_node}'}}) MERGE (a)-[:{relationship_label}]->(b)
        """
        return query.strip()
    
    ##########
    
    """ 
    Define functions to iterate over DataFrame to create list of queries for relationships
    
    Input: A dataframe containing OpenAlex Metadata
    Output: List of queries to be submitted to neo4j
    """
    
    def create_relationship_article_year(self, df):
        """ (Article)-[YEAR_PUBLISHED]-(Year) """
        relationship_queries = []
        for _, row in df.iterrows():
            start_node = row['id']
            end_node = str(row['publication_year'])
            relationship_label = 'YEAR_PUBLISHED'
            start_label = 'Article'
            end_label = 'Year'
    
            query = self.create_single_relationship_query(start_node, end_node, relationship_label, start_label=start_label, end_label=end_label, start_node_id='article_id', end_node_id='year_id')
        
            relationship_queries.append(query)
        
        return relationship_queries
    
    
    def create_relationship_article_title(self, df):
        """ (Article)-[HAS_TITLE]-(Title) """
        relationship_queries = []
        for _, row in df.iterrows():
            start_node = row['id']
            end_node = row['title_id']
            relationship_label = 'HAS_TITLE'
            start_label = 'Article'
            end_label = 'Title'
    
            query = self.create_single_relationship_query(start_node, end_node, relationship_label, start_label=start_label, end_label=end_label, start_node_id='article_id', end_node_id='title_id')
        
            relationship_queries.append(query)
        
        return relationship_queries

# Article -> HAS_ABSTRACT -> ABSTRACT
    def create_relationship_article_abstract(self, df):
        """ (Article)-[HAS_ABSTRACT]-(Abstract) """
        relationship_queries = []
        for _, row in df.iterrows():
            start_node = row['id']
            end_node = row['abstract_id']
            relationship_label = 'HAS_ABSTRACT'
            start_label = 'Article'
            end_label = 'Abstract'
    
            query = self.create_single_relationship_query(start_node, end_node, relationship_label, start_label=start_label, end_label=end_label, start_node_id='article_id', end_node_id='abstract_id')
        
            relationship_queries.append(query)
        
        return relationship_queries
    
# Article -> HAS_TOPIC -> Topic
    def create_relationship_article_topic(self, df):
        """ (Article)-[HAS_TOPIC]-(Topic) """
        relationship_queries = []
        for _, row in df.iterrows():
            start_node = row['id']
            end_node = row['topic_id']
            relationship_label = 'HAS_TOPIC'
            start_label = 'Article'
            end_label = 'Topic'
    
            query = self.create_single_relationship_query(start_node, end_node, relationship_label, start_label=start_label, end_label=end_label, start_node_id='article_id', end_node_id='topic_id')
        
            relationship_queries.append(query)
        
        return relationship_queries
    
# Article -> published_in -> Journal
    def create_relationship_article_journal(self, df):
        """ (Article)-[PUBLISHED_IN]-(Journal) """
        relationship_queries = []
        for _, row in df.iterrows():
            start_node = row['id']
            end_node = row['primary_location']['source']['id'].lstrip('https://openalex.org/')
            relationship_label = 'PUBLISHED_IN'
            start_label = 'Article'
            end_label = 'Journal'
    
            query = self.create_single_relationship_query(start_node, end_node, relationship_label, start_label=start_label, end_label=end_label, start_node_id='article_id', end_node_id='journal_id')
        
            relationship_queries.append(query)
        
        return relationship_queries
    
# Article -> written_by -> Author
    def create_relationship_article_author(self, df):
        """ (Article)-[WRITTEN_BY]-(Author) """
        relationship_queries = []
        for _, row in df.iterrows():
            start_node = row['id']
            for author_info in row['author_info']:
                end_node = author_id = author_info[0]
                relationship_label = 'WRITTEN_BY'
                start_label = 'Article'
                end_label = 'Author'
    
                query = self.create_single_relationship_query(start_node, end_node, relationship_label, start_label=start_label, end_label=end_label, start_node_id='article_id', end_node_id='author_id')
        
                relationship_queries.append(query)
        
        return relationship_queries

# Author -> affiliated_to -> Institution
    def create_relationship_author_institution(self, df):
        """ (Author)-[AFFILIATED_TO]-(Institution) """
        """ Use author_df """
        relationship_queries = []
        for _, row in df.iterrows():
            start_node = str(row['author_id'])
            end_node = str(row['institution_id'])
            relationship_label = 'AFFILIATED_TO'
            start_label = 'Author'
            end_label = 'Institution'
    
            query = self.create_single_relationship_query(start_node, end_node, relationship_label, start_label=start_label, end_label=end_label, start_node_id='author_id', end_node_id='institution_id')
        
            relationship_queries.append(query)
        
        return relationship_queries
    
# Institution -> from -> Country
    def create_relationship_institution_country(self, df):
        """ (Institution)-[IS_FROM]-(Country) """
        """ Use institution_df """
        relationship_queries = []
        for _, row in df.iterrows():
            start_node = row['institution_id']
            end_node = row['institution_country_code']
            relationship_label = 'IS_FROM'
            start_label = 'Institution'
            end_label = 'Country'
    
            query = self.create_single_relationship_query(start_node, end_node, relationship_label, start_label=start_label, end_label=end_label, start_node_id='institution_id', end_node_id='country_id')
        
            relationship_queries.append(query)
        
        return relationship_queries
##

# Article -> funded_by -> Funder
    def create_relationship_article_funder(self, df_funder):
        """ (Article)-[FUNDED_BY]-(Funder) """
        """ Need a dataframe with article and funder id """
        relationship_queries = []
        for _, row in df_funder[df_funder['funders_list_dedup_final'] != 0].iterrows(): 
            start_node = row['id']
            for item in list(row['funders_list_dedup_final']):
                end_node = item[0]
                relationship_label = 'FUNDED_BY'
                start_label = 'Article'
                end_label = 'Funder'
    
                query = self.create_single_relationship_query(start_node, end_node, relationship_label, start_label=start_label, end_label=end_label, start_node_id='article_id', end_node_id='funder_id')
        
                relationship_queries.append(query)
        
        return relationship_queries

# Funder -> located_in -> Country
    def create_relationship_funder_country(self, df):
        """ (Funder)-[LOCATED_IN]-(Country) """
        """ Need a funder country dataframe """
        """ Create this relationship directly from Neo4j Browser """
        relationship_queries = []
        for _, row in df.iterrows(): 
            start_node = row['funder_id']
            end_node = row['country_id'] 
            relationship_label = 'LOCATED_IN'
            start_label = 'Funder'
            end_label = 'Country'  
            
            query = self.create_single_relationship_query(start_node, end_node, relationship_label, start_label=start_label, end_label=end_label, start_node_id='funder_id', end_node_id='country_id')

            relationship_queries.append(query)
        return relationship_queries
    
    
# Article -> cites -> Article
    def create_relationship_article_article(self, df):
        """ (Article)-[CITES]-(Article) """
        """ Use df_citations """
        relationship_queries = []
        for _, row in df_funder[df_funder['funders_list_dedup_final'] != 0].iterrows(): 
            start_node = row['id']
            end_node = row['referenced_works'] 
            relationship_label = 'CITES'
            start_label = 'Article'
            end_label = 'Article'

            query = self.create_single_relationship_query(start_node, end_node, relationship_label, start_label=start_label, end_label=end_label, start_node_id='article_id', end_node_id='article_id')

            relationship_queries.append(query)
        
        return relationship_queries
    
    
    
