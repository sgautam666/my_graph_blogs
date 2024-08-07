import os, json
import uuid
import argparse
import pandas as pd
from neo4j import GraphDatabase
from create_neo4j_graph import GraphNodeCreator, GraphRelationshipCreator
from data_prep import DataPrep

def main():
    parser = argparse.ArgumentParser(description="Process a graph query.")    
    parser.add_argument("--neo4j_auradb_uri", type=str, required=True)
    parser.add_argument("--aura_username", type=str, required=True)
    parser.add_argument("--aura_password", type=str, required=True)
    
    args = parser.parse_args()
    
    
    # Instantiate some classes
    data_preparer = DataPrep()
    node_creator = GraphNodeCreator(args.neo4j_auradb_uri, args.aura_username, args.aura_password)
    relationship_creator = GraphRelationshipCreator(args.neo4j_auradb_uri, args.aura_username, args.aura_password)
    
    
    #-------Prepare some dataframes-------#
    
    # Data for Article 
    df = None
    data = pd.read_csv('meta data file', index_col=[0])
    df = pd.read_json('your file here')
    print(df.shape)

    # Generate unique UUIDs
    df['uuid'] = data_preparer.generate_unique_uuids(len(df))

    # Verify that all UUIDs are unique
    assert df['uuid'].is_unique, "There are duplicate UUIDs!"
    
    
    # Data for Date
    date_df = data_preparer.create_date_df(df)
    # Data for Journal
    journal_df = data_preparer.create_journal_df(df)
    # Data for Author
    author_df = data_preparer.create_author_df(df)
    # Data for Institution
    author_institution_data = pd.read_json('institution data ')
    institution_df = data_preparer.create_institution_df(author_institution_data)
    # Data for Country
    country_df = data_preparer.create_country_df(author_institution_data)    
    # Data for Funder
    funder_data = pd.read_json('funder data', orient='index').reset_index()
    funder_df = data_preparer.create_funder_df(funder_data)
    
    # Data for Author - Instituion relationship
    author_institution_df = data_preparer.create_author_institution_df(author_institution_data)
    # Data for Article - Funder relationship
    article_funder_df = data_preparer.create_article_funder_df(data)
    # Data for Funder - Country relationship
    article_funder_df = data_preparer.create_funder_country_df(funder_df)

    #-------Create Cypher Queries for Nodes-------#
    ''' Note different dataframes for some nodes'''
    article_nodes, article_properties = node_creator.create_article_nodes(df)
    year_nodes, year_properties = node_creator.create_date_nodes(date_df)
    title_nodes, title_properties = node_creator.create_title_nodes(df)
    abstract_nodes, abstract_properties = node_creator.create_abstract_nodes(df)
    topic_nodes, topic_properties = node_creator.create_topic_nodes(df)
    journal_nodes, journal_properties = node_creator.create_journal_nodes(journal_df)
    author_nodes, author_properties = node_creator.create_author_nodes(author_df)
    institution_nodes, institution_properties = node_creator.create_institution_nodes(institution_df)
    country_nodes, country_properties = node_creator.create_country_nodes(country_df)
    funder_nodes, funder_properties = node_creator.create_funder_nodes(funder_df)
    
    #-------Submit Cypher Queries to Neo4j Graph-------#
    node_creator.create_nodes(article_nodes, article_properties)
    node_creator.create_nodes(year_nodes, year_properties)
    node_creator.create_nodes(title_nodes, title_properties)
    node_creator.create_nodes(abstract_nodes, abstract_properties)
    node_creator.create_nodes(topic_nodes, topic_properties)
    node_creator.create_nodes(journal_nodes, journal_properties)
    node_creator.create_nodes(author_nodes, author_properties)
    node_creator.create_nodes(institution_nodes, institution_properties)
    node_creator.create_nodes(country_nodes, country_properties)
    node_creator.create_nodes(funder_nodes, funder_properties)
    
    #-------Create Cypher Queries for Relationships-------#
    ''' Note different dataframes for some relationships'''
    # Variable article_year => article to year
    article_year = relationship_creator.create_relationship_article_year(df)
    article_title = relationship_creator.create_relationship_article_title(df)
    article_abstract = relationship_creator.create_relationship_article_abstract(df)
    article_topic = relationship_creator.create_relationship_article_topic(df)
    article_journal = relationship_creator.create_relationship_article_journal(df)
    article_author = relationship_creator.create_relationship_article_author(df)
    author_institution = relationship_creator.create_relationship_author_institution(author_institution_df)
    institution_country = relationship_creator.create_relationship_institution_country(institution_df)
    article_funder = relationship_creator.create_relationship_article_funder(article_funder_df)
    funder_country = relationship_creator.create_relationship_funder_country(article_funder_df)
    
    #-------Submit Cypher Queries to Neo4j Graph-------#
    relationship_creator.create_relationships(article_year)
    relationship_creator.create_relationships(article_title)
    relationship_creator.create_relationships(article_abstract)
    relationship_creator.create_relationships(article_topic)
    relationship_creator.create_relationships(article_journal)
    relationship_creator.create_relationships(article_author)
    relationship_creator.create_relationships(author_institution)
    relationship_creator.create_relationships(institution_country)
    relationship_creator.create_relationships(article_funder)
    relationship_creator.create_relationships(funder_country)
    
    
    

if __name__ == "__main__":
    main()