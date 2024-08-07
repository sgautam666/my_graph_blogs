import pandas as pd
import os, json
import uuid

class DataPreProcess:
    def __init__(self):
        pass
    
class DataPrep:
    def __init__(self):
        pass
    
    def generate_unique_uuids(self, n):
        unique_uuids = set()
        while len(unique_uuids) < n:
            unique_uuids.add(str(uuid.uuid4()))
        return list(unique_uuids)

    
    def create_article_df(self, data):
        '''Input article dataframe'''
        '''Any uuid creation should be performed here for consistency'''
        '''For production, need to find better way to create unique ids for the item below'''
        df = data.copy()
        
        # Generate unique UUIDs
        df['uuid'] = self.generate_unique_uuids(len(df))
        # Create unique id for multiple columns
        df['title_id'] = df['uuid'].apply(lambda x: str(x)+'title')
        df['abstract_id'] = df['uuid'].apply(lambda x: str(x)+'abstract')
        df['topic_id'] = df['uuid'].apply(lambda x: str(x)+'topic')
        return df
    
    def create_journal_df(self, data):
        # Create journal dataframe
        df = data.copy()
        df['journal_id'] = df['primary_location'].apply(lambda x: x['source']['id'].lstrip('https://openalex.org'))
        df_journal = df[['journal_id', 'journal', 'issn', 'sjr_score', 'h_index', 'sjr_best_quartile']].copy() 
        df_journal.drop_duplicates(subset=['journal_id'], inplace=True)
        return df_journal
    
    def create_date_df(self, data):
        df = data[['publication_year']].copy()
        df['year_id'] = df['publication_year']
        df.drop_duplicates(subset=['year_id'], inplace=True)
        return df
    
    def create_author_df(self, data):
        df = data.copy()
        
        # Extract Authors info
        authors_info= []
        for index, row in df.iterrows():
            # Create unique set of authors
            for author_info in row['author_info']:
                authors_info.append([author_info[0], author_info[1], author_info[2], author_info[3]])

        df_author = pd.DataFrame(authors_info, columns = ['author_id', 'author_name', 'institution_id', 'institution_name'])
        df_author.drop_duplicates(subset=['author_id'], inplace=True)
        return df_author
        
    def create_institution_df(self, data):
        df = data.copy()
        df['associated_institution_list'] = df['associated_institution'].apply(lambda x: [item[0] for item in x if x is not None] if x is not None else [])
        df = df.drop(columns=['author_name', 'oa_extract', 'associated_institution'])
        df.drop_duplicates(subset=['institution_id'], inplace=True)
        return df
    
    def create_author_institution_df(self, data):
        return data[['author_id', 'institution_id']]
    
    def create_country_df(self, data):
        df = data.copy()
        df = df[['institution_country_code', 'country']].copy()
        df = df.drop_duplicates(subset=['country'])
        df = df[df['country'] != 'The Netherlands']
        return df

    def create_funder_df(self, data):
        df = data.copy()
        df = df.rename(columns={'index':'funder_id'})
        return df
    
    def create_article_funder_df(self, data):
        df = data[['id', 'funders_list']].copy()
        # Create a pair of funder id and funder name
        df['funders_list_dedup'] = df['funders_list'].apply(lambda x: set(zip(x[0],x[1])))
        # We want to omit rows with no value or zero value
        df['funders_list_dedup_final'] = df['funders_list_dedup'].apply(lambda x: len(x) if len(x)==0 else x)
        return df

    def create_funder_country_df(self, data):
        df = data[['funder_id', 'country_code']].copy()
        df['country_id'] = df['country_code']
        return df[['funder_id', 'country_id']]
    
    def create_citation_df(self, data):
        '''place holder'''
        df = data.copy()
        return None