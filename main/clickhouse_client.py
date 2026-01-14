import logging

import clickhouse_connect

logger = logging.getLogger(__name__)

class ClickHouseClient:
    """
    Клиент для работы с ClickHouse.
    Используется для аналитических запросов и ETL операций.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.client = clickhouse_connect.get_client(
            host='localhost',
            port=8123,
            username='default',
            password='clickhouse123',
            database='analytics'
        )
        self._initialized = True
        logger.info("ClickHouse client initialized")
    
    def insert_wines(self, wines_data):
        """Вставка данных о винах в ClickHouse"""
        if not wines_data:
            return 0
        
        self.client.insert(
            'analytics.wines',
            wines_data,
            column_names=[
                'wine_id', 'name', 'wine_type', 'country_id', 'country_name',
                'region', 'year', 'price', 'volume', 'alcohol',
                'grape_variety', 'created_at'
            ]
        )
        logger.info(f"Inserted {len(wines_data)} wines into ClickHouse")
        return len(wines_data)
    
    def insert_sales(self, sales_data):
        """Вставка данных о продажах в ClickHouse"""
        if not sales_data:
            return 0
        
        self.client.insert(
            'analytics.sales',
            sales_data,
            column_names=[
                'sale_id', 'wine_id', 'wine_name', 'wine_type', 'country_name',
                'quantity', 'price', 'total_amount', 'sale_date',
                'year', 'month', 'day', 'hour', 'day_of_week'
            ]
        )
        logger.info(f"Inserted {len(sales_data)} sales into ClickHouse")
        return len(sales_data)
    
    def get_daily_sales(self, start_date, end_date):
        """Получить статистику продаж по дням"""
        query = """
        SELECT 
            sale_date,
            wine_type,
            sum(total_quantity) as quantity,
            sum(total_revenue) as revenue,
            sum(order_count) as orders,
            avg(avg_price) as avg_price
        FROM analytics.daily_sales_mv
        WHERE sale_date BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY sale_date, wine_type
        ORDER BY sale_date DESC, revenue DESC
        """
        
        result = self.client.query(
            query,
            parameters={'start_date': start_date, 'end_date': end_date}
        )
        return result.result_rows
    
    def get_country_sales(self, start_date, end_date):
        """Получить статистику продаж по странам"""
        query = """
        SELECT 
            country_name,
            sum(total_quantity) as quantity,
            sum(total_revenue) as revenue,
            sum(order_count) as orders
        FROM analytics.country_sales_mv
        WHERE sale_date BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY country_name
        ORDER BY revenue DESC
        """
        
        result = self.client.query(
            query,
            parameters={'start_date': start_date, 'end_date': end_date}
        )
        return result.result_rows
    
    def get_top_wines(self, limit=10, start_date=None, end_date=None):
        """Получить топ продаваемых вин"""
        query = """
        SELECT 
            wine_name,
            wine_type,
            country_name,
            sum(quantity) as total_quantity,
            sum(total_amount) as total_revenue,
            count() as order_count,
            avg(price) as avg_price
        FROM analytics.sales
        WHERE 1=1
        """
        
        params = {}
        if start_date and end_date:
            query += " AND sale_date BETWEEN %(start_date)s AND %(end_date)s"
            params = {'start_date': start_date, 'end_date': end_date}
        
        query += """
        GROUP BY wine_name, wine_type, country_name
        ORDER BY total_revenue DESC
        LIMIT %(limit)s
        """
        params['limit'] = limit
        
        result = self.client.query(query, parameters=params)
        return result.result_rows
    
    def get_sales_metrics(self, start_date, end_date):
        """Получить общие метрики продаж"""
        query = """
        SELECT 
            count(DISTINCT sale_id) as total_orders,
            sum(total_amount) as total_revenue,
            avg(total_amount) as avg_order_value,
            sum(quantity) as total_items_sold,
            count(DISTINCT wine_id) as unique_wines_sold
        FROM analytics.sales
        WHERE sale_date BETWEEN %(start_date)s AND %(end_date)s
        """
        
        result = self.client.query(
            query,
            parameters={'start_date': start_date, 'end_date': end_date}
        )
        return result.result_rows[0] if result.result_rows else None
    
    def get_hourly_sales(self, date):
        """Получить статистику продаж по часам для конкретного дня"""
        query = """
        SELECT 
            hour,
            count() as orders,
            sum(total_amount) as revenue,
            sum(quantity) as items_sold
        FROM analytics.sales
        WHERE toDate(sale_date) = %(date)s
        GROUP BY hour
        ORDER BY hour
        """
        
        result = self.client.query(query, parameters={'date': date})
        return result.result_rows
    
    def log_sync(self, table_name, records_synced, sync_start, status, error_message=''):
        """Логирование синхронизации данных"""
        from datetime import datetime
        
        self.client.insert(
            'analytics.sync_log',
            [[
                0,  # sync_id (auto)
                table_name,
                records_synced,
                sync_start,
                datetime.now(),
                status,
                error_message
            ]],
            column_names=[
                'sync_id', 'table_name', 'records_synced',
                'sync_start', 'sync_end', 'status', 'error_message'
            ]
        )
    
    def execute_query(self, query, parameters=None):
        """Выполнить произвольный запрос"""
        result = self.client.query(query, parameters=parameters)
        return result.result_rows
    
    def close(self):
        """Закрыть соединение"""
        if hasattr(self, 'client'):
            self.client.close()
            logger.info("ClickHouse client closed")


# Singleton instance
clickhouse_client = ClickHouseClient()
