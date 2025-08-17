#!/usr/bin/env python3

import os
import json
import logging
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import List, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PricingFetcher:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'pricing'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'postgres')
        }
        
    def get_anthropic_pricing(self) -> List[Dict[str, Any]]:
        """Fetch Anthropic pricing data"""
        pricing_data = []
        
        anthropic_models = {
            'claude-3-5-sonnet-20241022': {
                'input_price_per_1k': 0.003,
                'output_price_per_1k': 0.015,
                'context_window': 200000,
                'max_output': 8192
            },
            'claude-3-5-haiku-20241022': {
                'input_price_per_1k': 0.001,
                'output_price_per_1k': 0.005,
                'context_window': 200000,
                'max_output': 8192
            },
            'claude-3-opus-20240229': {
                'input_price_per_1k': 0.015,
                'output_price_per_1k': 0.075,
                'context_window': 200000,
                'max_output': 4096
            },
            'claude-3-sonnet-20240229': {
                'input_price_per_1k': 0.003,
                'output_price_per_1k': 0.015,
                'context_window': 200000,
                'max_output': 4096
            },
            'claude-3-haiku-20240307': {
                'input_price_per_1k': 0.00025,
                'output_price_per_1k': 0.00125,
                'context_window': 200000,
                'max_output': 4096
            },
            'claude-2.1': {
                'input_price_per_1k': 0.008,
                'output_price_per_1k': 0.024,
                'context_window': 200000,
                'max_output': 4096
            },
            'claude-2.0': {
                'input_price_per_1k': 0.008,
                'output_price_per_1k': 0.024,
                'context_window': 100000,
                'max_output': 4096
            },
            'claude-instant-1.2': {
                'input_price_per_1k': 0.0008,
                'output_price_per_1k': 0.0024,
                'context_window': 100000,
                'max_output': 4096
            }
        }
        
        for model_name, details in anthropic_models.items():
            pricing_data.append({
                'provider': 'anthropic',
                'model_name': model_name,
                'input_price_per_1k_tokens': details['input_price_per_1k'],
                'output_price_per_1k_tokens': details['output_price_per_1k'],
                'context_window': details['context_window'],
                'max_output_tokens': details['max_output'],
                'last_updated': datetime.utcnow()
            })
        
        logger.info(f"Fetched {len(pricing_data)} Anthropic models")
        return pricing_data
    
    def get_openai_pricing(self) -> List[Dict[str, Any]]:
        """Fetch OpenAI pricing data"""
        pricing_data = []
        
        openai_models = {
            'gpt-4o': {
                'input_price_per_1k': 0.0025,
                'output_price_per_1k': 0.01,
                'context_window': 128000,
                'max_output': 16384
            },
            'gpt-4o-2024-11-20': {
                'input_price_per_1k': 0.0025,
                'output_price_per_1k': 0.01,
                'context_window': 128000,
                'max_output': 16384
            },
            'gpt-4o-2024-08-06': {
                'input_price_per_1k': 0.0025,
                'output_price_per_1k': 0.01,
                'context_window': 128000,
                'max_output': 16384
            },
            'gpt-4o-2024-05-13': {
                'input_price_per_1k': 0.005,
                'output_price_per_1k': 0.015,
                'context_window': 128000,
                'max_output': 4096
            },
            'gpt-4o-mini': {
                'input_price_per_1k': 0.00015,
                'output_price_per_1k': 0.0006,
                'context_window': 128000,
                'max_output': 16384
            },
            'gpt-4o-mini-2024-07-18': {
                'input_price_per_1k': 0.00015,
                'output_price_per_1k': 0.0006,
                'context_window': 128000,
                'max_output': 16384
            },
            'o1-preview': {
                'input_price_per_1k': 0.015,
                'output_price_per_1k': 0.06,
                'context_window': 128000,
                'max_output': 32768
            },
            'o1-preview-2024-09-12': {
                'input_price_per_1k': 0.015,
                'output_price_per_1k': 0.06,
                'context_window': 128000,
                'max_output': 32768
            },
            'o1-mini': {
                'input_price_per_1k': 0.003,
                'output_price_per_1k': 0.012,
                'context_window': 128000,
                'max_output': 65536
            },
            'o1-mini-2024-09-12': {
                'input_price_per_1k': 0.003,
                'output_price_per_1k': 0.012,
                'context_window': 128000,
                'max_output': 65536
            },
            'gpt-4-turbo': {
                'input_price_per_1k': 0.01,
                'output_price_per_1k': 0.03,
                'context_window': 128000,
                'max_output': 4096
            },
            'gpt-4-turbo-2024-04-09': {
                'input_price_per_1k': 0.01,
                'output_price_per_1k': 0.03,
                'context_window': 128000,
                'max_output': 4096
            },
            'gpt-4-turbo-preview': {
                'input_price_per_1k': 0.01,
                'output_price_per_1k': 0.03,
                'context_window': 128000,
                'max_output': 4096
            },
            'gpt-4-0125-preview': {
                'input_price_per_1k': 0.01,
                'output_price_per_1k': 0.03,
                'context_window': 128000,
                'max_output': 4096
            },
            'gpt-4-1106-preview': {
                'input_price_per_1k': 0.01,
                'output_price_per_1k': 0.03,
                'context_window': 128000,
                'max_output': 4096
            },
            'gpt-4': {
                'input_price_per_1k': 0.03,
                'output_price_per_1k': 0.06,
                'context_window': 8192,
                'max_output': 8192
            },
            'gpt-4-0613': {
                'input_price_per_1k': 0.03,
                'output_price_per_1k': 0.06,
                'context_window': 8192,
                'max_output': 8192
            },
            'gpt-4-32k': {
                'input_price_per_1k': 0.06,
                'output_price_per_1k': 0.12,
                'context_window': 32768,
                'max_output': 32768
            },
            'gpt-4-32k-0613': {
                'input_price_per_1k': 0.06,
                'output_price_per_1k': 0.12,
                'context_window': 32768,
                'max_output': 32768
            },
            'gpt-3.5-turbo': {
                'input_price_per_1k': 0.0005,
                'output_price_per_1k': 0.0015,
                'context_window': 16385,
                'max_output': 4096
            },
            'gpt-3.5-turbo-0125': {
                'input_price_per_1k': 0.0005,
                'output_price_per_1k': 0.0015,
                'context_window': 16385,
                'max_output': 4096
            },
            'gpt-3.5-turbo-1106': {
                'input_price_per_1k': 0.001,
                'output_price_per_1k': 0.002,
                'context_window': 16385,
                'max_output': 4096
            },
            'gpt-3.5-turbo-0613': {
                'input_price_per_1k': 0.0015,
                'output_price_per_1k': 0.002,
                'context_window': 4097,
                'max_output': 4096
            },
            'gpt-3.5-turbo-16k-0613': {
                'input_price_per_1k': 0.003,
                'output_price_per_1k': 0.004,
                'context_window': 16385,
                'max_output': 16385
            },
            'gpt-3.5-turbo-0301': {
                'input_price_per_1k': 0.0015,
                'output_price_per_1k': 0.002,
                'context_window': 4097,
                'max_output': 4096
            }
        }
        
        for model_name, details in openai_models.items():
            pricing_data.append({
                'provider': 'openai',
                'model_name': model_name,
                'input_price_per_1k_tokens': details['input_price_per_1k'],
                'output_price_per_1k_tokens': details['output_price_per_1k'],
                'context_window': details['context_window'],
                'max_output_tokens': details['max_output'],
                'last_updated': datetime.utcnow()
            })
        
        logger.info(f"Fetched {len(pricing_data)} OpenAI models")
        return pricing_data
    
    def create_table(self, conn):
        """Create the pricing table if it doesn't exist"""
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS model_pricing (
                    id SERIAL PRIMARY KEY,
                    provider VARCHAR(50) NOT NULL,
                    model_name VARCHAR(100) NOT NULL,
                    input_price_per_1k_tokens DECIMAL(10, 6),
                    output_price_per_1k_tokens DECIMAL(10, 6),
                    context_window INTEGER,
                    max_output_tokens INTEGER,
                    last_updated TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(provider, model_name)
                )
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_provider ON model_pricing(provider);
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_model_name ON model_pricing(model_name);
            """)
            
            conn.commit()
            logger.info("Database table created/verified")
    
    def upsert_pricing_data(self, conn, pricing_data: List[Dict[str, Any]]):
        """Insert or update pricing data in the database"""
        with conn.cursor() as cursor:
            for item in pricing_data:
                cursor.execute("""
                    INSERT INTO model_pricing (
                        provider, model_name, input_price_per_1k_tokens,
                        output_price_per_1k_tokens, context_window,
                        max_output_tokens, last_updated
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (provider, model_name)
                    DO UPDATE SET
                        input_price_per_1k_tokens = EXCLUDED.input_price_per_1k_tokens,
                        output_price_per_1k_tokens = EXCLUDED.output_price_per_1k_tokens,
                        context_window = EXCLUDED.context_window,
                        max_output_tokens = EXCLUDED.max_output_tokens,
                        last_updated = EXCLUDED.last_updated
                """, (
                    item['provider'],
                    item['model_name'],
                    item['input_price_per_1k_tokens'],
                    item['output_price_per_1k_tokens'],
                    item['context_window'],
                    item['max_output_tokens'],
                    item['last_updated']
                ))
            
            conn.commit()
            logger.info(f"Upserted {len(pricing_data)} records to database")
    
    def run(self):
        """Main execution function"""
        try:
            logger.info("Starting pricing data fetch and load process")
            
            logger.info(f"Connecting to database at {self.db_config['host']}:{self.db_config['port']}")
            conn = psycopg2.connect(**self.db_config)
            
            self.create_table(conn)
            
            all_pricing_data = []
            
            anthropic_data = self.get_anthropic_pricing()
            all_pricing_data.extend(anthropic_data)
            
            openai_data = self.get_openai_pricing()
            all_pricing_data.extend(openai_data)
            
            self.upsert_pricing_data(conn, all_pricing_data)
            
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT provider, COUNT(*) as model_count,
                           MIN(input_price_per_1k_tokens) as min_input_price,
                           MAX(input_price_per_1k_tokens) as max_input_price
                    FROM model_pricing
                    GROUP BY provider
                    ORDER BY provider
                """)
                summary = cursor.fetchall()
                
                logger.info("Summary of loaded data:")
                for row in summary:
                    logger.info(f"  {row['provider']}: {row['model_count']} models, "
                              f"Input price range: ${row['min_input_price']:.6f} - ${row['max_input_price']:.6f}")
            
            conn.close()
            logger.info("Process completed successfully")
            
        except Exception as e:
            logger.error(f"Error during execution: {str(e)}", exc_info=True)
            raise


if __name__ == "__main__":
    fetcher = PricingFetcher()
    fetcher.run()